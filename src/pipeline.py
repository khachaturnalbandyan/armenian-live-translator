"""Wire capture -> segmentation -> speaker ID -> transcription -> translation -> terminal.

Every source (microphone, system audio) gets its own capture thread and segmenter, so
a pause on one side of the call never delays the other. The segments they produce are
handed to a single worker thread, because the recogniser owns the GPU and running two
copies of it would make both slower.
"""

from __future__ import annotations

import queue
import statistics
import threading
import time
from dataclasses import dataclass

from .asr import Transcriber
from .capture import CaptureError, EndOfStream
from .display import Printer
from .fillers import filler_translation
from .recorder import SegmentRecorder
from .segmenter import Segment, Segmenter
from .speakers import SpeakerIdentifier
from .translate import Translator

READ_CHUNK = 4096  # 256 ms at 16 kHz: frequent enough for low end-to-end latency
# A looped transcript can run to a hundred words; this many are enough to show what
# it was without flooding the terminal.
UNCLEAR_PREVIEW_WORDS = 6


def unclear_preview(text: str, words: int = UNCLEAR_PREVIEW_WORDS) -> str:
    parts = text.split()
    return " ".join(parts[:words]) + (" …" if len(parts) > words else "")


@dataclass
class Source:
    """One capture stream, with the speaker policy that applies to it."""

    label: str  # "mic" / "system audio", for diagnostics
    capture: object  # ParecCapture or WavFileSource
    segmenter: Segmenter
    speaker: str | None  # fixed label, or None to identify speakers from the voice


class Pipeline:
    def __init__(
        self,
        sources: list[Source],
        transcriber: Transcriber,
        translator: Translator | None,
        printer: Printer,
        identifier: SpeakerIdentifier | None = None,
        show_stats: bool = False,
        recorder: SegmentRecorder | None = None,
    ):
        self.sources = sources
        self.recorder = recorder
        self.transcriber = transcriber
        self.translator = translator
        self.printer = printer
        self.identifier = identifier
        self.show_stats = show_stats

        self._segments: queue.Queue[tuple[Segment, Source] | None] = queue.Queue(maxsize=64)
        self._stop = threading.Event()
        self._started_at = time.monotonic()
        self._latencies: list[float] = []
        self._failures = 0
        self._retries = 0
        self._unclear = 0
        self._counts: dict[str, int] = {}

    def run(self) -> None:
        worker = threading.Thread(target=self._process_loop, daemon=True)
        worker.start()
        readers = [
            threading.Thread(target=self._read_loop, args=(source,), daemon=True)
            for source in self.sources
        ]
        self._started_at = time.monotonic()
        for reader in readers:
            reader.start()

        try:
            while any(reader.is_alive() for reader in readers):
                for reader in readers:
                    reader.join(timeout=0.2)
        except KeyboardInterrupt:
            self._stop.set()
            for source in self.sources:
                source.capture.close()  # type: ignore[attr-defined]
            for reader in readers:
                reader.join(timeout=5)

        finally:
            for source in self.sources:
                for segment in source.segmenter.flush():
                    self._segments.put((segment, source))
            self._segments.put(None)
            worker.join(timeout=60)
            self._print_summary()

    # -- capture ------------------------------------------------------------

    def _read_loop(self, source: Source) -> None:
        try:
            with source.capture:  # type: ignore[attr-defined]
                while not self._stop.is_set():
                    chunk = source.capture.read(READ_CHUNK)  # type: ignore[attr-defined]
                    for segment in source.segmenter.push(chunk):
                        self._segments.put((segment, source))
        except (EndOfStream, KeyboardInterrupt):
            pass
        except CaptureError as exc:
            if not self._stop.is_set():
                print(f"! {source.label}: {exc}", flush=True)
        except Exception as exc:  # a dead capture thread must not look like silence
            if not self._stop.is_set():
                print(f"! {source.label} failed: {exc.__class__.__name__}: {exc}", flush=True)

    # -- processing ---------------------------------------------------------

    def _process_loop(self) -> None:
        while True:
            item = self._segments.get()
            if item is None:
                return
            segment, source = item
            try:
                self._handle(segment, source)
            except Exception as exc:  # keep the session alive, but say what broke
                self._failures += 1
                print(f"! segment failed: {exc.__class__.__name__}: {exc}", flush=True)

    def _handle(self, segment: Segment, source: Source) -> None:
        speaker = source.speaker
        speaker_time = 0.0
        if speaker is None:
            if self.identifier is not None:  # identify before ASR: it is cheap
                speaker = self.identifier.identify(segment.audio)
                speaker_time = self.identifier.last_embed_seconds
            else:
                speaker = "Speaker 1"

        transcript = self.transcriber.transcribe(segment.audio)
        if not transcript.text:
            return
        self._retries += transcript.retried

        armenian = transcript.text
        english, translate_time = "", 0.0
        # Interjections first: "դե, դե, դե" is how people talk, not a decoding loop.
        if (filler := filler_translation(transcript.text)) is not None:
            english = filler  # NLLB turns a lone "հա" into a made-up sentence
        elif transcript.unclear:
            # A looped transcript translates into "this this this ..."; say it is
            # unusable instead of presenting it as what was said.
            self._unclear += 1
            armenian, english = f"[unclear] {unclear_preview(transcript.text)}", "[unclear]"
        elif self.translator is not None:
            english, translate_time = self.translator.translate(transcript.text)

        latency = time.monotonic() - segment.t_finalized
        self._latencies.append(latency)
        self._counts[speaker] = self._counts.get(speaker, 0) + 1

        stats = ""
        if self.show_stats:
            speaker_part = f"spk {speaker_time:.2f}s, " if source.speaker is None else ""
            retry_part = " incl. loop retry" if transcript.retried else ""
            stats = (
                f"({speaker_part}asr {transcript.elapsed:.2f}s{retry_part} + mt {translate_time:.2f}s, "
                f"latency {latency:.2f}s)"
            )
        self.printer.segment(
            started_at=self._started_at,
            # End of speech, not start: lines appear as phrases end, so a long phrase
            # from one side would otherwise look out of order next to the other side.
            timestamp=self._started_at + segment.end,
            speaker=speaker,
            armenian=armenian,
            english=english,
            stats=stats,
        )
        if self.recorder is not None:
            self.recorder.save(
                segment.audio,
                source=source.label,
                speaker=speaker,
                at=segment.start,
                armenian=armenian,
                english=english,
            )

    def _print_summary(self) -> None:
        if not self._latencies:
            print("\nNo speech detected.", flush=True)
            return
        lat = sorted(self._latencies)
        p50 = statistics.median(lat)
        p95 = lat[min(len(lat) - 1, int(len(lat) * 0.95))]
        slowest = lat[-1]
        over = sum(1 for x in lat if x > 5.0)
        by_speaker = ", ".join(f"{name} {count}" for name, count in sorted(self._counts.items()))
        print(
            f"\n{len(lat)} segments · latency p50 {p50:.2f}s, p95 {p95:.2f}s, "
            f"max {slowest:.2f}s · over 5s: {over} · by speaker: {by_speaker}"
            + (f" · loops retried: {self._retries}, unclear: {self._unclear}" if self._retries else "")
            + (f" · failures: {self._failures}" if self._failures else ""),
            flush=True,
        )
