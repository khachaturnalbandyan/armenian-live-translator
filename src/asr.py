"""Armenian speech recognition with faster-whisper (CTranslate2, local)."""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from faster_whisper import WhisperModel

# Whisper sometimes gets stuck repeating one word ("այդ այդ այդ այդ ..."). The same
# word this many times in a row is treated as such a loop.
LOOP_RUN = 3
# Used only to re-decode a looped segment. Always on, it raises CER on normal Armenian
# (13.5% -> 16.0% on the eval set), so normal segments are never decoded with it.
RETRY_NO_REPEAT_NGRAM = 3


@dataclass
class Transcript:
    text: str
    audio_seconds: float
    elapsed: float
    retried: bool = False  # the first decode looped and the segment was decoded again
    unclear: bool = False  # it still looped after the retry: the text is not usable


def has_word_loop(text: str, run: int = LOOP_RUN) -> bool:
    """True if one word repeats `run` or more times in a row, ignoring punctuation."""
    words = ["".join(ch for ch in word if ch.isalnum()).lower() for word in text.split()]
    words = [word for word in words if word]
    return any(len(set(words[i : i + run])) == 1 for i in range(len(words) - run + 1))



class Transcriber:
    def __init__(
        self,
        model_name: str = "large-v3",
        device: str = "cuda",
        compute_type: str = "float16",
        language: str = "hy",
        beam_size: int = 5,
    ):
        self.language = language
        self.beam_size = beam_size
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio: np.ndarray) -> Transcript:
        started = time.monotonic()
        if len(audio) == 0:
            return Transcript(text="", audio_seconds=0.0, elapsed=0.0)

        # Normalize volume to help whisper with quiet microphones
        peak = float(np.max(np.abs(audio)))
        if peak > 1e-4:
            audio = audio / max(peak, 0.1) * 0.95

        text = self._decode(audio)
        retried = unclear = False
        if has_word_loop(text):
            retried = True
            text = self._decode(audio, no_repeat_ngram_size=RETRY_NO_REPEAT_NGRAM)
            unclear = has_word_loop(text)

        elapsed = time.monotonic() - started
        return Transcript(
            text=text,
            audio_seconds=len(audio) / 16_000,
            elapsed=elapsed,
            retried=retried,
            unclear=unclear,
        )

    def _decode(self, audio: np.ndarray, **options) -> str:
        segments, _info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=self.beam_size,
            no_speech_threshold=0.6,
            # No repetition_penalty: 1.1 raised CER from 13.5% to 17.7% on the eval set,
            # because Armenian legitimately repeats the same tokens.
            condition_on_previous_text=False,
            without_timestamps=True,
            **options,
        )
        # faster-whisper returns a lazy generator: all the work happens here, so the
        # timer in transcribe() has to wrap the consumption of it, not the call above.
        return " ".join(seg.text.strip() for seg in segments).strip()
