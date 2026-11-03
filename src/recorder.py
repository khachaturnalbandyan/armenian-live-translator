"""--save-audio: keep every live segment as a WAV, next to what was shown for it.

The files are what a later evaluation needs: the exact audio each line came from (as
the live segmenter cut it), the source and speaker label, and the Armenian and English
the program printed. `session.jsonl` gets one JSON object per segment, in the order
the segments were shown.
"""

from __future__ import annotations

import json
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 16_000
INT16_MAX = 32767


class SegmentRecorder:
    def __init__(self, directory: Path | str):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self._index = 0

    def save(
        self,
        audio: np.ndarray,
        *,
        source: str,
        speaker: str,
        at: float,
        armenian: str,
        english: str,
    ) -> None:
        self._index += 1
        name = f"{self._index:04d}_{source.replace(' ', '-')}.wav"
        pcm = (np.clip(audio, -1.0, 1.0) * INT16_MAX).astype(np.int16)
        with wave.open(str(self.directory / name), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(pcm.tobytes())

        entry = {
            "file": name,
            "source": source,
            "speaker": speaker,
            "at": round(at, 2),
            "seconds": round(len(audio) / SAMPLE_RATE, 2),
            "armenian": armenian,
            "english": english,
        }
        with open(self.directory / "session.jsonl", "a", encoding="utf-8") as log:
            log.write(json.dumps(entry, ensure_ascii=False) + "\n")
