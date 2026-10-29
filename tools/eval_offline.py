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
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.asr import Transcriber  # noqa: E402
from src.segmenter import Segmenter  # noqa: E402
from src.translate import Translator  # noqa: E402
from tools.scoring import cer, load_manifest, load_wav, percentile  # noqa: E402

MANIFEST = ROOT / "eval" / "manifest.json"


def evaluate(model_name: str, mode: str, translate: bool, compute_type: str) -> dict:
    items = load_manifest(MANIFEST)
    transcriber = Transcriber(model_name=model_name, device="cuda", compute_type=compute_type)
    translator = Translator(device="cuda") if translate else None

    errors, latencies = [], []
    for item in items:
        audio = load_wav(item.path)

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

        errors.append(cer(item.reference, " ".join(texts)))

    return {
        "model": model_name,
        "mode": mode,
        "cer": statistics.mean(errors) * 100,
        "p50": percentile(latencies, 0.50),
        "p95": percentile(latencies, 0.95),
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
