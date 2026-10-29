"""Record real Armenian phrases for the evaluation set, with the correct text attached.

Shows one sentence at a time; press Enter to start recording, Enter again to stop.
Each take is saved as a 16 kHz mono WAV in eval/real/ and added to
eval/real/manifest.json right away, so a crash or Ctrl+C loses nothing.
Recordings are git-ignored (the brief forbids committing audio); the manifest is not.

Usage:
    python tools/record_eval.py --speaker aram                       # default microphone
    python tools/record_eval.py --speaker aram --device <mic name>   # from --list-devices
    python tools/record_eval.py --speaker ani --device <x>.monitor --source call
        # the other person reads the sentences over a call; their side is recorded
    python tools/record_eval.py --speaker aram --sentences my_lines.txt   # one per line

Speak naturally, the way you would in a call: reading slowly and clearly gives
optimistic numbers.
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.capture import SAMPLE_RATE, CaptureError, ParecCapture, list_devices  # noqa: E402

OUT_DIR = ROOT / "eval" / "real"
MANIFEST = OUT_DIR / "manifest.json"
CHUNK = 1600  # 100 ms
MIN_SECONDS = 0.5

SENTENCES = [
    "Բարև, ինչպե՞ս ես։",
    "Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։",
    "Վաղը ժամը տասին հանդիպում ունենք։",
    "Կարո՞ղ ես կրկնել, լավ չլսեցի։",
    "Այս շաբաթ շատ աշխատանք ունեմ։",
    "Երևանում այսօր շատ շոգ է։",
    "Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։",
    "Ո՞վ է պատասխանատու այս հարցի համար։",
    "Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։",
    "Զանգիր ինձ, երբ տուն հասնես։",
    "Գինը հազար հինգ հարյուր դրամ է։",
    "Արամը և Անին երեկ գնացին Գյումրի։",
    "Ինտերնետը նորից դանդաղ է աշխատում։",
    "Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։",
    "Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։",
    "Ներողություն, ուշացա, խցանում էր։",
    "Ի՞նչ ես կարծում, սա կաշխատի՞։",
    "Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։",
    "Այո, ամեն ինչ պարզ է, շնորհակալ եմ։",
    "Լավ, ուրեմն մինչև վաղը, հաջողություն։",
]


def record_until_enter(device: str | None) -> np.ndarray:
    chunks: list[np.ndarray] = []
    stop = threading.Event()
    failure: list[Exception] = []

    def reader() -> None:
        try:
            with ParecCapture(device) as capture:
                while not stop.is_set():
                    chunks.append(capture.read(CHUNK))
        except CaptureError as exc:
            failure.append(exc)

    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    input("  ● recording... Enter to stop ")
    stop.set()
    thread.join(timeout=2)
    if failure:
        raise failure[0]
    return np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.float32)


def save_wav(path: Path, audio: np.ndarray) -> None:
    pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm.tobytes())


def load_entries() -> list[dict]:
    return json.loads(MANIFEST.read_text("utf-8")) if MANIFEST.is_file() else []


def write_entries(entries: list[dict]) -> None:
    MANIFEST.write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_sentences(path: Path | None) -> list[str]:
    if path is None:
        return SENTENCES
    lines = [line.strip() for line in path.read_text("utf-8").splitlines()]
    return [line for line in lines if line]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--speaker", required=True, help="who is speaking (used in file names and CER by speaker)")
    parser.add_argument("--device", help="capture device; default is the system microphone")
    parser.add_argument("--source", default="mic", choices=["mic", "call"], help="mic, or the call side")
    parser.add_argument("--sentences", type=Path, help="text file, one sentence per line")
    args = parser.parse_args()

    if args.device and args.device not in {d["name"] for d in list_devices()}:
        print(f"error: unknown device '{args.device}'; see ./run.sh --list-devices", file=sys.stderr)
        return 1
    if not args.speaker.replace("-", "").replace("_", "").isalnum():
        print("error: --speaker must be letters, digits, '-' or '_'", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    entries = load_entries()
    done = {(e["speaker"], e["source"], e["reference"]) for e in entries}
    todo = [s for s in read_sentences(args.sentences) if (args.speaker, args.source, s) not in done]
    print(f"{len(todo)} sentences to record for {args.speaker} ({args.source}). "
          "Enter = record, s = skip, q = quit.\n")

    for number, sentence in enumerate(todo, start=1):
        print(f"[{number}/{len(todo)}] {sentence}")
        while True:
            choice = input("  Enter to record > ").strip().lower()
            if choice == "q":
                return 0
            if choice == "s":
                break
            try:
                audio = record_until_enter(args.device)
            except CaptureError as exc:
                print(f"error: {exc}", file=sys.stderr)
                return 1
            seconds = len(audio) / SAMPLE_RATE
            peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
            if seconds < MIN_SECONDS or peak < 0.01:
                print(f"  too short or silent ({seconds:.1f}s, peak {peak:.3f}); check the device, try again")
                continue

            name = f"{args.speaker}_{args.source}_{len(entries) + 1:03d}.wav"
            save_wav(OUT_DIR / name, audio)
            entries = entries + [{
                "file": name, "reference": sentence, "speaker": args.speaker,
                "source": args.source, "seconds": round(seconds, 2),
            }]
            write_entries(entries)
            print(f"  saved {name} ({seconds:.1f}s, peak {peak:.2f})\n")
            break

    print(f"done: {len(entries)} recordings in {MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nstopped; everything recorded so far is saved")
