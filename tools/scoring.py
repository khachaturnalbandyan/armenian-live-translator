"""Scoring shared by the evaluation tools: text normalisation, CER, WER, manifests.

Normalisation decides what counts as an error, so it lives in one place:
- NFKC folds the "և" ligature into "եւ", so either spelling of the same word matches;
- punctuation (Armenian "։ ՝ ՞" and Latin ". , ?") is dropped, because the brief is about
  recognising words, and models disagree on punctuation more than on words;
- case is folded.
"""

from __future__ import annotations

import json
import unicodedata
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np

SAMPLE_RATE = 16_000


def normalize_words(text: str) -> list[str]:
    folded = unicodedata.normalize("NFKC", text).lower()
    cleaned = "".join(ch if ch.isalnum() else " " for ch in folded)
    return cleaned.split()


def edit_distance(reference: list, hypothesis: list) -> int:
    prev = list(range(len(hypothesis) + 1))
    for i, ref_item in enumerate(reference, start=1):
        cur = [i]
        for j, hyp_item in enumerate(hypothesis, start=1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ref_item != hyp_item)))
        prev = cur
    return prev[-1]


def cer(reference: str, hypothesis: str) -> float:
    """Character error rate, ignoring spaces, punctuation and case."""
    ref = list("".join(normalize_words(reference)))
    hyp = list("".join(normalize_words(hypothesis)))
    if not ref:
        return 0.0 if not hyp else 1.0
    return edit_distance(ref, hyp) / len(ref)


def wer(reference: str, hypothesis: str) -> float:
    """Word error rate, ignoring punctuation and case."""
    ref, hyp = normalize_words(reference), normalize_words(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    return edit_distance(ref, hyp) / len(ref)


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * q))]


@dataclass(frozen=True)
class EvalItem:
    path: Path
    reference: str
    speaker: str
    source: str


def load_manifest(manifest: Path) -> list[EvalItem]:
    """Read a manifest; `file` entries are relative to the manifest's own folder."""
    if not manifest.is_file():
        raise FileNotFoundError(f"manifest not found: {manifest}")
    entries = json.loads(manifest.read_text("utf-8"))
    items = []
    for entry in entries:
        path = manifest.parent / entry["file"]
        if not path.is_file():
            raise FileNotFoundError(f"{manifest}: audio file missing: {path}")
        items.append(
            EvalItem(
                path=path,
                reference=entry["reference"],
                speaker=entry.get("speaker", "unknown"),
                source=entry.get("source", "unknown"),
            )
        )
    return items


def load_wav(path: Path) -> np.ndarray:
    """16 kHz mono 16-bit WAV -> float32 in [-1, 1]. Anything else is an error."""
    with wave.open(str(path), "rb") as wav:
        if wav.getframerate() != SAMPLE_RATE or wav.getnchannels() != 1 or wav.getsampwidth() != 2:
            raise ValueError(f"{path}: expected 16 kHz mono 16-bit PCM")
        raw = wav.readframes(wav.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
