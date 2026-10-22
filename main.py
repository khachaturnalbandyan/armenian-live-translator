"""Live Armenian speech -> English translation in the terminal."""

from __future__ import annotations

import argparse
import os
import sys

# Keep the terminal clean: model downloads and transformers chatter are noise next
# to the transcript.
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")

from src.asr import Transcriber
from src.capture import (
    CaptureError,
    ParecCapture,
    WavFileSource,
    default_monitor,
    list_devices,
)
from src.display import Printer
from src.pipeline import Pipeline, Source
from src.segmenter import Segmenter
from src.speakers import SpeakerIdentifier
from src.translate import Translator


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe live Armenian speech and print English translation."
    )
    parser.add_argument("--list-devices", action="store_true", help="list capture devices and exit")
    parser.add_argument("--device", help="microphone name, as shown by --list-devices")
    parser.add_argument(
        "--system-audio",
        nargs="?",
        const="auto",
        metavar="DEVICE",
        help="also listen to system audio (the other call participants); "
        "DEVICE defaults to the monitor of the default output",
    )
    parser.add_argument("--input", help="process a 16 kHz mono WAV file instead of the microphone")
    parser.add_argument(
        "--input-system", help="second WAV file, standing in for the system audio stream"
    )
    parser.add_argument("--fast", action="store_true", help="read WAV files as fast as possible")
    parser.add_argument(
        "--diarize",
        action="store_true",
        help="identify speakers on the microphone stream too (default: it is 'Me')",
    )
    parser.add_argument(
        "--speaker-threshold",
        type=float,
        default=0.55,
        help="cosine similarity above which a segment belongs to a known speaker (default: 0.55)",
    )
    parser.add_argument("--model", default="large-v3", help="faster-whisper model (default: large-v3)")
    parser.add_argument("--compute-type", default="float16", help="CTranslate2 compute type")
    parser.add_argument("--cpu", action="store_true", help="run on CPU instead of CUDA")
    parser.add_argument(
        "--mt-model", default="facebook/nllb-200-distilled-600M", help="NLLB translation model"
    )
    parser.add_argument("--no-translate", action="store_true", help="transcribe only (debugging)")
    parser.add_argument(
        "--min-silence-ms", type=int, default=450, help="pause that ends a segment (default: 450)"
    )
    parser.add_argument(
        "--max-segment-s", type=float, default=6.0, help="hard cut for long monologues (default: 6.0)"
    )
    parser.add_argument("--threshold", type=float, default=0.5, help="VAD speech threshold")
    parser.add_argument("--stats", action="store_true", help="print timing next to each line")
    parser.add_argument("--output", help="optional file path to save live transcripts")
    return parser.parse_args(argv)


def build_sources(args: argparse.Namespace) -> tuple[list[Source], list[str]]:
    """Create one `Source` per stream, with its own segmenter and speaker policy."""

    def new_segmenter() -> Segmenter:
        return Segmenter(
            min_silence_ms=args.min_silence_ms,
            max_segment_s=args.max_segment_s,
            threshold=args.threshold,
        )

    available_devices: list[dict] | None = None

    def check_device(dev_name: str, kind: str) -> None:
        nonlocal available_devices
        if available_devices is None:
            available_devices = list_devices()
        known = {d["name"] for d in available_devices}
        if dev_name not in known:
            raise CaptureError(
                f"{kind} device '{dev_name}' not found. "
                f"Run with --list-devices to see available devices."
            )

    sources: list[Source] = []
    where: list[str] = []

    # The microphone is always one of them: it carries the local participant.
    if args.input:
        if not os.path.isfile(args.input):
            raise CaptureError(f"Input file not found: {args.input}")
        mic: object = WavFileSource(args.input, realtime=not args.fast)
        where.append(f"mic: file {args.input}")
    else:
        if args.device:
            check_device(args.device, "Microphone")
        mic = ParecCapture(args.device)
        where.append(f"mic: {args.device or 'system default'}")
    sources.append(
        Source(
            label="mic",
            capture=mic,
            segmenter=new_segmenter(),
            speaker=None if args.diarize else "Me",
        )
    )

    # The far side of the call: the system audio output, whose speakers all have to
    # be separated from each other by voice.
    if args.input_system:
        if not os.path.isfile(args.input_system):
            raise CaptureError(f"System audio input file not found: {args.input_system}")
        sources.append(
            Source(
                label="system audio",
                capture=WavFileSource(args.input_system, realtime=not args.fast),
                segmenter=new_segmenter(),
                speaker=None,
            )
        )
        where.append(f"system audio: file {args.input_system}")
    elif args.system_audio is not None:
        device = default_monitor() if args.system_audio == "auto" else args.system_audio
        check_device(device, "System audio")
        sources.append(
            Source(
                label="system audio",
                capture=ParecCapture(device),
                segmenter=new_segmenter(),
                speaker=None,
            )
        )
        where.append(f"system audio: {device}")

    return sources, where


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.list_devices:
        for dev in list_devices():
            kind = "system audio" if dev["monitor"] else "microphone"
            print(f"{dev['name']}\n    {dev.get('description', '')} [{kind}]")
        return 0

    compute_type = args.compute_type
    run_device = "cpu" if args.cpu else "cuda"
    if args.cpu and compute_type == "float16":
        compute_type = "int8"

    try:
        sources, where = build_sources(args)
    except CaptureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        needs_identification = any(source.speaker is None for source in sources)
        identifier = None
        if needs_identification:
            print("Loading speaker embedding model...", flush=True)
            identifier = SpeakerIdentifier(threshold=args.speaker_threshold)

        print(f"Loading models on {run_device} (this takes a few seconds)...", flush=True)
        transcriber = Transcriber(
            model_name=args.model, device=run_device, compute_type=compute_type
        )
        translator = None if args.no_translate else Translator(args.mt_model, device=run_device)
    except Exception as exc:
        print(f"error loading models: {exc}", file=sys.stderr)
        return 1

    pipeline = Pipeline(
        sources=sources,
        transcriber=transcriber,
        translator=translator,
        printer=Printer(output_file=args.output),
        identifier=identifier,
        show_stats=args.stats,
    )

    print("Listening:\n  " + "\n  ".join(where), flush=True)
    print("Armenian in, English out. Ctrl+C to stop.\n", flush=True)
    try:
        pipeline.run()
    except CaptureError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
