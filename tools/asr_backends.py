"""Speech recognisers that can be compared on the same Armenian recordings.

A backend is named "<kind>:<model>", for example:

    faster-whisper:large-v3                  the recogniser the live program uses
    hf-whisper:<hugging face repo>           any Whisper fine-tune in transformers format
    mms:facebook/mms-1b-all                  Meta MMS, CTC with the Armenian ("hye") adapter
    ctc:<hugging face repo>                  any Armenian CTC fine-tune (wav2vec2, w2v-BERT)
    seamless:facebook/seamless-m4t-v2-large  Meta SeamlessM4T v2, speech -> Armenian text

Every backend exposes `transcribe(audio) -> str` and `close()`. Models are loaded one at
a time and freed before the next one, so an 8 GB GPU can compare all of them.

These run locally once downloaded; only the first load fetches weights from Hugging Face.
"""

from __future__ import annotations

import gc
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.asr import Transcriber  # noqa: E402
from src.asr_seamless import SeamlessTranscriber  # noqa: E402

SAMPLE_RATE = 16_000


def _device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def _dtype(device: str) -> torch.dtype:
    return torch.float16 if device == "cuda" else torch.float32


class FasterWhisperBackend:
    """The live program's own Transcriber, so its numbers match what the app does."""

    def __init__(self, model: str):
        device = _device()
        compute_type = "float16" if device == "cuda" else "int8"
        self._transcriber = Transcriber(model_name=model, device=device, compute_type=compute_type)

    def transcribe(self, audio: np.ndarray) -> str:
        return self._transcriber.transcribe(audio).text

    def close(self) -> None:
        del self._transcriber


class HfWhisperBackend:
    """A Whisper checkpoint in transformers format, e.g. an Armenian fine-tune."""

    def __init__(self, model: str):
        from transformers import WhisperForConditionalGeneration, WhisperProcessor

        self._device = _device()
        self._processor = WhisperProcessor.from_pretrained(model)
        self._model = (
            WhisperForConditionalGeneration.from_pretrained(model, dtype=_dtype(self._device))
            .to(self._device)
            .eval()
        )

    def transcribe(self, audio: np.ndarray) -> str:
        features = self._processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt").input_features
        features = features.to(self._device, dtype=self._model.dtype)
        with torch.inference_mode():
            ids = self._model.generate(features, language="hy", task="transcribe", num_beams=5)
        return self._processor.batch_decode(ids, skip_special_tokens=True)[0].strip()

    def close(self) -> None:
        del self._model


class MmsBackend:
    """Meta MMS: one wav2vec2 CTC model with a small adapter per language."""

    LANGUAGE = "hye"

    def __init__(self, model: str):
        from transformers import AutoProcessor, Wav2Vec2ForCTC

        self._device = _device()
        self._processor = AutoProcessor.from_pretrained(model, target_lang=self.LANGUAGE)
        if self.LANGUAGE not in self._processor.tokenizer.vocab:
            raise ValueError(f"{model} has no '{self.LANGUAGE}' (Armenian) vocabulary")
        self._model = (
            Wav2Vec2ForCTC.from_pretrained(
                model, target_lang=self.LANGUAGE, ignore_mismatched_sizes=True
            )
            .to(self._device)
            .eval()
        )

    def transcribe(self, audio: np.ndarray) -> str:
        inputs = self._processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
        with torch.inference_mode():
            logits = self._model(inputs.input_values.to(self._device)).logits
        ids = torch.argmax(logits, dim=-1)[0]
        return self._processor.decode(ids).strip()

    def close(self) -> None:
        del self._model


class CtcBackend:
    """Any CTC checkpoint already fine-tuned for Armenian, e.g. a wav2vec2 or w2v-BERT model."""

    def __init__(self, model: str):
        from transformers import AutoModelForCTC, AutoProcessor

        self._device = _device()
        self._processor = AutoProcessor.from_pretrained(model)
        self._model = AutoModelForCTC.from_pretrained(model).to(self._device).eval()

    def transcribe(self, audio: np.ndarray) -> str:
        inputs = self._processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt")
        inputs = {name: value.to(self._device) for name, value in inputs.items()}
        with torch.inference_mode():
            logits = self._model(**inputs).logits
        ids = torch.argmax(logits, dim=-1)[0]
        return self._processor.decode(ids).strip()

    def close(self) -> None:
        del self._model


class SeamlessBackend:
    """The live program's SeamlessTranscriber, so its numbers match what the app does."""

    def __init__(self, model: str):
        self._transcriber = SeamlessTranscriber(model_name=model, device=_device())

    def transcribe(self, audio: np.ndarray) -> str:
        return self._transcriber.transcribe(audio).text

    def close(self) -> None:
        del self._transcriber


BACKENDS = {
    "faster-whisper": FasterWhisperBackend,
    "hf-whisper": HfWhisperBackend,
    "mms": MmsBackend,
    "ctc": CtcBackend,
    "seamless": SeamlessBackend,
}


def load_backend(spec: str):
    kind, sep, model = spec.partition(":")
    if not sep or not model:
        raise ValueError(f"backend must look like '<kind>:<model>', got '{spec}'")
    if kind not in BACKENDS:
        raise ValueError(f"unknown backend kind '{kind}'; choose from {', '.join(BACKENDS)}")
    return BACKENDS[kind](model)


def release(backend) -> None:
    """Free the backend's GPU memory before the next model is loaded."""
    backend.close()
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
