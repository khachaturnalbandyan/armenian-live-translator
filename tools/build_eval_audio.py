"""Build a small Armenian evaluation set with a local Piper voice (hy_AM-gor-medium).

Synthetic speech is not a substitute for real recordings - it is too clean and its
prosody is flat - but it makes latency and wiring measurable from the first commit and
catches regressions. Real recordings should carry the accuracy numbers; see TESTS.md.

Requires: pip install piper-tts, and ffmpeg on PATH.
The voice (63 MB) is downloaded once into eval/voices/ and is git-ignored.

Usage: python tools/build_eval_audio.py
"""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

SENTENCES = [
    "Բարև, ինչպես ես։",
    "Լավ եմ, շնորհիվ աստծո։",
    "Այսօր եղանակը շատ լավ է, արի գնանք զբոսնելու։",
    "Ժողովը սկսվում է ժամը երեքին, մի ուշացիր։",
    "Ես կարծում եմ, որ այս լուծումը ավելի արագ կաշխատի։",
]

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "eval" / "audio"
VOICE = ROOT / "eval" / "voices" / "hy_AM-gor-medium.onnx"
SAMPLE_RATE = 16_000


def synth(sentence: str, target: Path) -> None:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        subprocess.run(
            [str(ROOT / ".venv/bin/piper"), "-m", str(VOICE), "-f", str(tmp_path), "--sentence-silence", "0.3"],
            input=sentence.encode("utf-8"),
            check=True,
            stdout=subprocess.DEVNULL,
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp_path),
                "-af", "adelay=500:all=1,apad=pad_dur=0.5",
                "-ar", str(SAMPLE_RATE), "-ac", "1", str(target),
            ],
            check=True,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


def main() -> None:
    if not VOICE.exists():
        raise SystemExit(
            f"missing voice: {VOICE}\n"
            "download hy_AM-gor-medium.onnx (+ .json) from rhasspy/piper-voices into eval/voices/"
        )
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    for i, sentence in enumerate(SENTENCES, start=1):
        name = f"tts_{i:02d}.wav"
        path = OUT_DIR / name
        synth(sentence, path)
        duration = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        manifest.append(
            {"file": name, "reference": sentence, "seconds": round(float(duration), 2),
             "source": "piper hy_AM-gor-medium"}
        )
        print(f"{name}: {float(duration):.1f}s - {sentence}")

    (OUT_DIR.parent / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nwrote {len(manifest)} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
