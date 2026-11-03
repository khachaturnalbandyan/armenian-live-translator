"""Who is talking: one stable label per person, built up as the session runs.

pyannote's offline diarization pipeline needs the *whole* recording before it can
label anything, which is incompatible with a 5 second latency budget. What it uses
internally, though, is a speaker embedding model that maps a few seconds of speech
to a 256-dimensional voice vector. We run that model on every closed segment and
cluster the vectors online: if a vector is close enough to a speaker we have already
heard, it is that speaker; otherwise it is a new one.

The model is `pyannote/wespeaker-voxceleb-resnet34-LM`, the same embedding model the
pyannote 3.1 diarization pipeline uses. It is small (ResNet34) and runs on the CPU in
about 40 ms per segment, so it neither competes with the recogniser for the GPU nor
shows up in the latency budget.
"""

from __future__ import annotations

import time
import warnings

import numpy as np
import torch

EMBEDDING_MODEL = "pyannote/wespeaker-voxceleb-resnet34-LM"


class SpeakerIdentifier:
    """Assigns "Speaker 1", "Speaker 2", ... to segments, consistently per session."""

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        threshold: float = 0.55,
        min_speech_s: float = 0.4,
        min_new_speaker_s: float = 1.5,
        device: str = "cpu",
        sample_rate: int = 16_000,
    ):
        # pyannote warns about torchcodec's ffmpeg bindings on import; we pass
        # waveforms as tensors, so its file loader is never used.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from pyannote.audio import Inference, Model

            model = Model.from_pretrained(model_name)
            self._inference = Inference(model, window="whole", device=torch.device(device))

        self.threshold = threshold
        self.sample_rate = sample_rate
        self.min_samples = int(min_speech_s * sample_rate)
        # Below this a voice vector is too noisy to found a speaker or to refine one:
        # live, every short reply ("հա", "ախպեր") became a new speaker, 31 in 3 minutes.
        # Such a segment is given the closest speaker already known.
        self.min_new_speaker_samples = int(min_new_speaker_s * sample_rate)
        self._sums: list[np.ndarray] = []
        self._counts: list[int] = []
        self.last_embed_seconds = 0.0

    @property
    def speaker_count(self) -> int:
        return len(self._sums)

    def identify(self, audio: np.ndarray) -> str:
        """Return the label for one segment, learning a new speaker if needed."""
        start = time.monotonic()
        vector = None if len(audio) < self.min_samples else self._embed(audio)
        self.last_embed_seconds = time.monotonic() - start

        if vector is None:
            # Too short to describe a voice: say so rather than guess from a
            # vector that would be mostly noise.
            return "Speaker ?"

        short = len(audio) < self.min_new_speaker_samples
        if not self._sums:
            if short:
                return "Speaker ?"
            self._add(vector)
            return self._label(0)

        similarities = self._similarities(vector)
        best = int(np.argmax(similarities))
        if short:
            return self._label(best)
        if similarities[best] >= self.threshold:
            self._sums[best] = self._sums[best] + vector
            self._counts[best] += 1
            return self._label(best)

        self._add(vector)
        return self._label(len(self._sums) - 1)

    # -- internals ----------------------------------------------------------

    def _label(self, index: int) -> str:
        return f"Speaker {index + 1}"

    def _add(self, vector: np.ndarray) -> None:
        self._sums.append(vector.copy())
        self._counts.append(1)

    def _similarities(self, vector: np.ndarray) -> np.ndarray:
        centroids = np.stack([s / (np.linalg.norm(s) + 1e-9) for s in self._sums])
        return centroids @ vector

    def _embed(self, audio: np.ndarray) -> np.ndarray | None:
        waveform = torch.from_numpy(np.ascontiguousarray(audio, dtype=np.float32))[None, :]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw = self._inference({"waveform": waveform, "sample_rate": self.sample_rate})
        vector = np.asarray(raw, dtype=np.float32).reshape(-1)
        norm = np.linalg.norm(vector)
        if not np.isfinite(norm) or norm == 0:
            return None
        return vector / norm
