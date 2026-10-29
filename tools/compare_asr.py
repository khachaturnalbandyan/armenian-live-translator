"""Compare speech recognisers on the same Armenian recordings: accuracy and speed.

Usage:
    python tools/compare_asr.py faster-whisper:large-v3 faster-whisper:large-v3-turbo
    python tools/compare_asr.py faster-whisper:large-v3 mms:facebook/mms-1b-all \\
        seamless:facebook/seamless-m4t-v2-large --show --report eval/results.md
    python tools/compare_asr.py faster-whisper:large-v3 --manifest eval/manifest.json  # synthetic set

By default it reads the real recordings made with tools/record_eval.py. `--segment`
first cuts each recording with the live program's Segmenter, so pauses are handled the
way they are during a call. See tools/asr_backends.py for the backend names.
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.segmenter import Segmenter  # noqa: E402
from tools.asr_backends import load_backend, release  # noqa: E402
from tools.scoring import SAMPLE_RATE, EvalItem, cer, load_manifest, load_wav, percentile, wer  # noqa: E402

DEFAULT_MANIFEST = ROOT / "eval" / "real" / "manifest.json"


@dataclass
class ItemResult:
    item: EvalItem
    hypothesis: str
    cer: float
    wer: float
    seconds: float  # recognition time for the whole item
    audio_seconds: float


@dataclass
class BackendResult:
    spec: str
    load_seconds: float
    items: list[ItemResult] = field(default_factory=list)

    def summary(self) -> dict:
        latencies = [r.seconds for r in self.items]
        audio = sum(r.audio_seconds for r in self.items)
        return {
            "cer": statistics.mean(r.cer for r in self.items) * 100,
            "wer": statistics.mean(r.wer for r in self.items) * 100,
            "p50": percentile(latencies, 0.50),
            "p95": percentile(latencies, 0.95),
            "max": max(latencies),
            "rtf": sum(latencies) / audio if audio else 0.0,
        }


def pieces_of(audio, segment: bool) -> list:
    if not segment:
        return [audio]
    segmenter = Segmenter()
    return [s.audio for s in segmenter.push(audio) + segmenter.flush()]


def run_backend(spec: str, items: list[EvalItem], segment: bool) -> BackendResult:
    print(f"\n== {spec}: loading...", flush=True)
    started = time.monotonic()
    backend = load_backend(spec)
    result = BackendResult(spec=spec, load_seconds=time.monotonic() - started)
    try:
        backend.transcribe(load_wav(items[0].path))  # warm-up: first call pays CUDA set-up
        for item in items:
            audio = load_wav(item.path)
            started = time.monotonic()
            texts = [backend.transcribe(piece) for piece in pieces_of(audio, segment)]
            elapsed = time.monotonic() - started
            hypothesis = " ".join(t for t in texts if t)
            result.items.append(
                ItemResult(
                    item=item,
                    hypothesis=hypothesis,
                    cer=cer(item.reference, hypothesis),
                    wer=wer(item.reference, hypothesis),
                    seconds=elapsed,
                    audio_seconds=len(audio) / SAMPLE_RATE,
                )
            )
            print(f"   {item.path.name}: CER {result.items[-1].cer * 100:5.1f}%  {elapsed:.2f}s", flush=True)
    finally:
        release(backend)
    return result


def summary_table(results: list[BackendResult]) -> str:
    lines = [
        "| backend | CER | WER | latency p50 | p95 | max | RTF | load |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in sorted(results, key=lambda r: r.summary()["cer"]):
        s = r.summary()
        lines.append(
            f"| `{r.spec}` | {s['cer']:.1f}% | {s['wer']:.1f}% | {s['p50']:.2f}s | "
            f"{s['p95']:.2f}s | {s['max']:.2f}s | {s['rtf']:.2f} | {r.load_seconds:.0f}s |"
        )
    return "\n".join(lines)


def breakdown_table(results: list[BackendResult], key: str) -> str:
    """CER per speaker or per source (mic / call), to see where a model breaks down."""
    groups = sorted({getattr(r.item, key) for r in results[0].items})
    lines = [
        f"| backend | {' | '.join(groups)} |",
        "| --- |" + " --- |" * len(groups),
    ]
    for r in results:
        cells = []
        for group in groups:
            errors = [i.cer for i in r.items if getattr(i.item, key) == group]
            cells.append(f"{statistics.mean(errors) * 100:.1f}%")
        lines.append(f"| `{r.spec}` | {' | '.join(cells)} |")
    return "\n".join(lines)


def hypotheses_table(results: list[BackendResult]) -> str:
    lines = []
    for index, item_result in enumerate(results[0].items):
        lines.append(f"**{item_result.item.path.name}** — ref: {item_result.item.reference}")
        for r in results:
            hyp = r.items[index]
            lines.append(f"- `{r.spec}` ({hyp.cer * 100:.0f}%): {hyp.hypothesis or '∅'}")
        lines.append("")
    return "\n".join(lines)


def build_report(results: list[BackendResult], manifests: list[Path], segment: bool, show: bool) -> str:
    count = len(results[0].items)
    audio = sum(r.audio_seconds for r in results[0].items)
    parts = [
        f"{count} recordings, {audio:.0f} s of audio, from "
        + ", ".join(str(m.relative_to(ROOT)) if m.is_relative_to(ROOT) else str(m) for m in manifests)
        + (" (cut by the live Segmenter)" if segment else " (whole recordings)"),
        "Latency = recognition time per recording; the 5 s budget also includes translation.",
        "",
        summary_table(results),
        "",
        "CER by speaker:",
        "",
        breakdown_table(results, "speaker"),
        "",
        "CER by source:",
        "",
        breakdown_table(results, "source"),
    ]
    if show:
        parts += ["", hypotheses_table(results)]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("backends", nargs="+", help="e.g. faster-whisper:large-v3 mms:facebook/mms-1b-all")
    parser.add_argument(
        "--manifest", type=Path, action="append",
        help=f"eval manifest (repeatable; default {DEFAULT_MANIFEST.relative_to(ROOT)})",
    )
    parser.add_argument("--segment", action="store_true", help="cut audio with the live Segmenter first")
    parser.add_argument("--show", action="store_true", help="print every model's transcript per recording")
    parser.add_argument("--report", type=Path, help="also write the results as Markdown to this file")
    args = parser.parse_args()

    manifests = args.manifest or [DEFAULT_MANIFEST]
    try:
        items = [item for manifest in manifests for item in load_manifest(manifest)]
    except (FileNotFoundError, ValueError) as exc:
        print(f"error: {exc}\nrecord real phrases first: python tools/record_eval.py --speaker <name>",
              file=sys.stderr)
        return 1
    if not items:
        print("error: the manifest has no recordings", file=sys.stderr)
        return 1

    results = [run_backend(spec, items, args.segment) for spec in args.backends]
    report = build_report(results, manifests, args.segment, args.show)
    print("\n" + report)
    if args.report:
        args.report.write_text(report + "\n", encoding="utf-8")
        print(f"\nwrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
