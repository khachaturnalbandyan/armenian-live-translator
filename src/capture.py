"""Audio capture from PulseAudio / PipeWire via the `parec` command-line tool.

The challenge requires capturing the microphone and the system audio output at the
same time. On Linux, PipeWire exposes every playback device as a `.monitor` source,
so both sides of a call are just two capture devices - no virtual loopback driver
(BlackHole on macOS) is needed.
"""

from __future__ import annotations

import re
import subprocess
import time
import wave

import numpy as np

SAMPLE_RATE = 16_000
CHANNELS = 1
BYTES_PER_SAMPLE = 2  # s16le

_NAME_RE = re.compile(r"^\s*Name:\s*(.+)$")
_DESC_RE = re.compile(r"^\s*Description:\s*(.+)$")
_MONITOR_RE = re.compile(r"\.monitor\s*$")


class CaptureError(RuntimeError):
    """Raised when the audio backend cannot be used."""


class EndOfStream(CaptureError):
    """The audio source ran out of data (file input, or a device that went away)."""


def list_devices() -> list[dict]:
    """Return every available capture source, microphone and loopback alike."""
    try:
        out = subprocess.run(
            ["pactl", "list", "sources"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise CaptureError(
            "`pactl` is not available. Install pulseaudio-utils (or run on Linux "
            "with PipeWire/PulseAudio)."
        ) from exc

    devices: list[dict] = []
    current: dict = {}
    for line in out.splitlines():
        if name := _NAME_RE.match(line):
            current = {"name": name.group(1).strip()}
        elif desc := _DESC_RE.match(line):
            current["description"] = desc.group(1).strip()
            current["monitor"] = bool(_MONITOR_RE.search(current["name"]))
            devices.append(current)
            current = {}
    return devices


def default_monitor() -> str:
    """Name of the monitor source for the current default output (the call audio)."""
    try:
        sink = subprocess.run(
            ["pactl", "get-default-sink"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise CaptureError(
            "Cannot determine the default output device; pass a device name from "
            "--list-devices instead."
        ) from exc
    if not sink:
        raise CaptureError("`pactl get-default-sink` returned an empty name.")
    return f"{sink}.monitor"


class ParecCapture:
    """Streams mono float32 audio at 16 kHz from a PulseAudio/PipeWire source."""

    def __init__(self, device: str | None = None, sample_rate: int = SAMPLE_RATE):
        self.device = device
        self.sample_rate = sample_rate
        self._proc: subprocess.Popen | None = None

    def __enter__(self) -> "ParecCapture":
        self.start()
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def start(self) -> None:
        cmd = [
            "parec",
            "--format=s16le",
            f"--rate={self.sample_rate}",
            f"--channels={CHANNELS}",
            "--latency-msec=50",
        ]
        if self.device:
            cmd.append(f"--device={self.device}")
        try:
            self._proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except FileNotFoundError as exc:
            raise CaptureError("`parec` not found. Install pulseaudio-utils.") from exc

    def read(self, n_samples: int) -> np.ndarray:
        """Block until `n_samples` are available and return them as float32 in [-1, 1]."""
        if self._proc is None or self._proc.stdout is None:
            raise CaptureError("Capture is not running; call start() first.")

        want = n_samples * BYTES_PER_SAMPLE
        buf = bytearray(want)
        view = memoryview(buf)
        got = 0
        while got < want:
            n = self._proc.stdout.readinto(view[got:])
            if not n:
                stderr = b""
                if self._proc.stderr is not None:
                    stderr = self._proc.stderr.read()
                raise CaptureError(
                    "Audio stream ended unexpectedly: "
                    + stderr.decode("utf-8", "replace").strip()
                )
            got += n
        return np.frombuffer(buf, dtype=np.int16).astype(np.float32) / 32768.0

    def close(self) -> None:
        if self._proc is None:
            return
        self._proc.terminate()
        try:
            self._proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self._proc.kill()
        self._proc = None


class WavFileSource:
    """Plays a 16-bit PCM WAV file through the same interface as live capture.

    Used for offline evaluation, so a recording can be measured exactly the way the
    live pipeline would see it.
    """

    def __init__(self, path: str, sample_rate: int = SAMPLE_RATE, realtime: bool = True):
        self.path = path
        self.sample_rate = sample_rate
        self.realtime = realtime
        self._wav: wave.Wave_read | None = None
        self._started = 0.0
        self._read_samples = 0

    def __enter__(self) -> "WavFileSource":
        self.start()
        return self

    def __exit__(self, *_exc) -> None:
        self.close()

    def start(self) -> None:
        self._wav = wave.open(self.path, "rb")
        if self._wav.getframerate() != self.sample_rate:
            raise CaptureError(
                f"{self.path}: expected {self.sample_rate} Hz, "
                f"got {self._wav.getframerate()} Hz"
            )
        if self._wav.getnchannels() != 1 or self._wav.getsampwidth() != BYTES_PER_SAMPLE:
            raise CaptureError(f"{self.path}: expected mono 16-bit PCM")
        self._started = time.monotonic()
        self._read_samples = 0

    def read(self, n_samples: int) -> np.ndarray:
        if self._wav is None:
            raise CaptureError("File source is not running; call start() first.")
        raw = self._wav.readframes(n_samples)
        if not raw:
            raise EndOfStream("end of file")
        self._read_samples += len(raw) // BYTES_PER_SAMPLE
        if self.realtime:
            # Pace the file like a live stream so latency numbers stay meaningful.
            target = self._started + self._read_samples / self.sample_rate
            delay = target - time.monotonic()
            if delay > 0:
                time.sleep(delay)
        return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

    def close(self) -> None:
        if self._wav is not None:
            self._wav.close()
            self._wav = None
