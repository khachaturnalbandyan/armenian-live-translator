"""Armenian speech recognition with Meta SeamlessM4T v2 (local), chosen with --asr seamless.

License: CC-BY-NC-4.0, non-commercial use only. See DECISIONS.md (D1).
"""

from __future__ import annotations

import time

import numpy as np
import torch

from src.asr import Transcript, has_word_loop

SEAMLESS_MODEL = "facebook/seamless-m4t-v2-large"
ARMENIAN = "hye"
SAMPLE_RATE = 16_000


class SeamlessTranscriber:
    """Same interface as src.asr.Transcriber: transcribe(audio) -> Transcript."""

    def __init__(self, model_name: str = SEAMLESS_MODEL, device: str = "cuda"):
        from transformers import AutoProcessor, SeamlessM4Tv2ForSpeechToText

        self._device = device
        self._processor = AutoProcessor.from_pretrained(model_name)
        dtype = torch.float16 if device == "cuda" else torch.float32
        self._model = (
            SeamlessM4Tv2ForSpeechToText.from_pretrained(model_name, dtype=dtype).to(device).eval()
        )

    def transcribe(self, audio: np.ndarray) -> Transcript:
        started = time.monotonic()
        if len(audio) == 0:
            return Transcript(text="", audio_seconds=0.0, elapsed=0.0)

        text = self._decode(audio)
        return Transcript(
            text=text,
            audio_seconds=len(audio) / SAMPLE_RATE,
            elapsed=time.monotonic() - started,
            unclear=has_word_loop(text),
        )

    def _decode(self, audio: np.ndarray) -> str:
        inputs = self._processor(audio=audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
        features = inputs["input_features"].to(self._device, dtype=self._model.dtype)
        with torch.inference_mode():
            ids = self._model.generate(
                input_features=features,
                attention_mask=inputs["attention_mask"].to(self._device),
                tgt_lang=ARMENIAN,
            )
        return self._processor.decode(ids[0], skip_special_tokens=True).strip()
