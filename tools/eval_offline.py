"""Offline evaluation on eval/audio: character error rate and per-segment latency.

This runs the real components (Segmenter, Transcriber, Translator), not a copy of
them, so the numbers describe what the live program actually does.

Usage:
    python tools/eval_offline.py                       # default models, transcription only
    python tools/eval_offline.py --translate           # include MT latency
    python tools/eval_offline.py --models large-v3 large-v3-turbo
"""

from __future__ import annotations

import argparse
import glob
import json
import statistics
import sys
import time
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.asr import Transcriber  # noqa: E402
from src.segmenter import Segmenter  # noqa: E402
from src.translate import Translator  # noqa: E402
AUDIO_DIR = ROOT / "eval" / "audio"
MANIFEST = ROOT / "eval" / "manifest.json"


def load_wav(path: str) -> np.ndarray:
    with wave.open(path, "rb") as wav:
        assert wav.getframerate() == 16_000, f"{path}: expected 16 kHz"
        raw = wav.readframes(wav.getnframes())
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


def normalize(text: str) -> str:
    return "".join(ch for ch in text.lower() if ch.isalnum() or "\u0530" <= ch <= "\u058f")


def cer(reference: str, hypothesis: str) -> float:
    ref, hyp = normalize(reference), normalize(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    prev = list(range(len(hyp) + 1))
    for i, rc in enumerate(ref, start=1):
        cur = [i]
        for j, hc in enumerate(hyp, start=1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rc != hc)))
        prev = cur
    return prev[-1] / len(ref)


def pct(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(len(ordered) * q))]


def evaluate(model_name: str, mode: str, translate: bool, compute_type: str) -> dict:
    references = {m["file"]: m["reference"] for m in json.loads(MANIFEST.read_text("utf-8"))}
    transcriber = Transcriber(model_name=model_name, device="cuda", compute_type=compute_type)
    translator = Translator(device="cuda") if translate else None

    errors, latencies = [], []
    for path in sorted(glob.glob(str(AUDIO_DIR / "*.wav"))):
        audio = load_wav(path)
        name = Path(path).name

        if mode == "file":
            pieces = [(audio, 0.0)]
        else:
            segmenter = Segmenter()
            pieces = [(s.audio, s.t_finalized) for s in segmenter.push(audio) + segmenter.flush()]

        texts = []
        for piece, _start in pieces:
            started = time.monotonic()
            transcript = transcriber.transcribe(piece)
            if translator is not None and transcript.text:
                translator.translate(transcript.text)
            latencies.append(time.monotonic() - started)
            texts.append(transcript.text)

        errors.append(cer(references[name], " ".join(texts)))

    return {
        "model": model_name,
        "mode": mode,
        "cer": statistics.mean(errors) * 100,
        "p50": pct(latencies, 0.50),
        "p95": pct(latencies, 0.95),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["large-v3"])
    parser.add_argument("--modes", nargs="+", default=["file", "stream"], choices=["file", "stream"])
    parser.add_argument("--translate", action="store_true")
    parser.add_argument("--compute-type", default="float16")
    args = parser.parse_args()

    for model_name in args.models:
        for mode in args.modes:
            r = evaluate(model_name, mode, args.translate, args.compute_type)
            extra = " (incl. MT)" if args.translate else ""
            print(
                f"{r['model']:18s} {r['mode']:7s} CER {r['cer']:5.1f}%  "
                f"latency p50 {r['p50']:.2f}s p95 {r['p95']:.2f}s{extra}",
                flush=True,
            )


if __name__ == "__main__":
    main()
