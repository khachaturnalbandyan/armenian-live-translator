"""Turns a continuous audio stream into speech segments, using Silero VAD.

Segmentation is what makes the 5 second latency budget achievable: we do not wait
for a fixed window to fill up. As soon as the speaker pauses for `min_silence_ms`,
the segment is closed and sent to the recogniser, so the clock starts at the end of
the *phrase*, not at the end of a fixed chunk.
"""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field

import numpy as np

from faster_whisper.vad import get_vad_model

FRAME_SAMPLES = 512  # Silero works on 32 ms windows at 16 kHz


@dataclass
class Segment:
    audio: np.ndarray
    start: float  # seconds since the stream started
    end: float  # seconds since the stream started, end of speech (not of padding)
    t_finalized: float = field(default_factory=time.monotonic)


class Segmenter:
    """Accumulates frames and yields one `Segment` per spoken phrase."""

    def __init__(
        self,
        sample_rate: int = 16_000,
        threshold: float = 0.5,
        min_silence_ms: int = 350,
        min_speech_ms: int = 200,
        max_segment_s: float = 6.0,
        pad_ms: int = 200,
        pre_roll_ms: int = 160,
    ):
        self.sample_rate = sample_rate
        self.threshold = threshold
        self.min_silence = int(sample_rate * min_silence_ms / 1000)
        self.min_speech = int(sample_rate * min_speech_ms / 1000)
        self.max_segment = int(sample_rate * max_segment_s)
        self.pad = int(sample_rate * pad_ms / 1000)
        self.pre_roll_frames = max(1, int(sample_rate * pre_roll_ms / 1000) // FRAME_SAMPLES)

        self._vad = get_vad_model()
        self._leftover = np.zeros(0, dtype=np.float32)
        self._pre = deque(maxlen=self.pre_roll_frames + 1)
        self._pos = 0  # samples consumed so far
        self._reset_state()

    # -- public API ---------------------------------------------------------

    def push(self, chunk: np.ndarray) -> list[Segment]:
        """Feed captured audio; returns segments that were closed by this chunk."""
        if chunk.size == 0:
            return []

        buf = np.concatenate([self._leftover, chunk])
        n_frames = len(buf) // FRAME_SAMPLES
        self._leftover = buf[n_frames * FRAME_SAMPLES :]
        if n_frames == 0:
            return []

        frames = buf[: n_frames * FRAME_SAMPLES].reshape(n_frames, FRAME_SAMPLES)
        probs = self._vad(frames.reshape(-1))
        return [seg for seg in (self._step(f, float(p)) for f, p in zip(frames, probs)) if seg]

    def flush(self) -> list[Segment]:
        """Close a segment that is still open, e.g. when the stream stops."""
        return [seg] if (seg := self._close()) else []

    # -- internals ----------------------------------------------------------

    def _reset_state(self) -> None:
        self._in_speech = False
        self._frames: list[np.ndarray] = []
        self._seg_start = 0
        self._last_speech_end = 0
        self._silence_run = 0

    def _step(self, frame: np.ndarray, prob: float) -> Segment | None:
        frame_start = self._pos
        self._pos += FRAME_SAMPLES
        speech = prob >= self.threshold

        if not self._in_speech:
            self._pre.append(frame)
            if not speech:
                return None
            # Speech just started: include the frames captured before the onset.
            self._in_speech = True
            self._frames = list(self._pre)
            self._seg_start = frame_start - (len(self._pre) - 1) * FRAME_SAMPLES
            self._last_speech_end = self._pos
            self._silence_run = 0
            return None

        self._frames.append(frame)
        if speech:
            self._last_speech_end = self._pos
            self._silence_run = 0
            return None

        self._silence_run += FRAME_SAMPLES
        length = self._pos - self._seg_start

        if length >= self.max_segment:
            return self._close()
        if self._silence_run >= self.min_silence:
            return self._close()
        return None

    def _close(self) -> Segment | None:
        if not self._in_speech or not self._frames:
            self._reset_state()
            return None

        audio = np.concatenate(self._frames)
        keep = self._last_speech_end + self.pad - self._seg_start
        keep = int(min(max(keep, 0), len(audio)))
        audio = audio[:keep]

        segment = None
        if len(audio) >= self.min_speech:
            segment = Segment(
                audio=audio,
                start=self._seg_start / self.sample_rate,
                end=self._last_speech_end / self.sample_rate,
            )

        self._reset_state()
        self._pre.clear()
        return segment
