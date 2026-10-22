"""Armenian speech recognition with faster-whisper (CTranslate2, local)."""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from faster_whisper import WhisperModel


@dataclass
class Transcript:
    text: str
    audio_seconds: float
    elapsed: float


class Transcriber:
    def __init__(
        self,
        model_name: str = "large-v3",
        device: str = "cuda",
        compute_type: str = "float16",
        language: str = "hy",
        beam_size: int = 5,
        initial_prompt: str = "Բարև ձեզ։ Սա հայերեն խոսակցություն է։",
    ):
        self.language = language
        self.beam_size = beam_size
        self.initial_prompt = initial_prompt
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio: np.ndarray) -> Transcript:
        started = time.monotonic()
        if len(audio) == 0:
            return Transcript(text="", audio_seconds=0.0, elapsed=0.0)

        # Normalize volume to help whisper with quiet microphones
        peak = float(np.max(np.abs(audio)))
        if peak > 1e-4:
            audio = audio / max(peak, 0.1) * 0.95

        segments, _info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=self.beam_size,
            initial_prompt=self.initial_prompt,
            repetition_penalty=1.1,
            condition_on_previous_text=False,
            without_timestamps=True,
        )
        # faster-whisper returns a lazy generator: all the work happens here, so the
        # timer has to wrap the consumption of it, not the call above.
        text = " ".join(seg.text.strip() for seg in segments).strip()
        elapsed = time.monotonic() - started
        return Transcript(text=text, audio_seconds=len(audio) / 16_000, elapsed=elapsed)
