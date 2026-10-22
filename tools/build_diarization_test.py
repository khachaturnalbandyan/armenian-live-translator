"""Build a two-voice conversation for testing speaker identification.

Piper ships only one Armenian voice (hy_AM-gor), so the second speaker is an English
voice from the same toolkit. That is legitimate for this test: speaker embeddings
describe the voice, not the language. What we check here is that the pipeline puts
stable, *different* labels on two different voices and does not invent new speakers
when the first one comes back - the wiring, in other words, not Armenian accuracy.

Expected pattern: A, B, A, B.

Usage: python tools/build_diarization_test.py
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOICES = ROOT / "eval" / "voices"
OUT = ROOT / "eval" / "audio" / "two_voices.wav"
SAMPLE_RATE = 16_000

# (voice, text) - alternating so the pipeline has to switch back and forth.
TURNS = [
    ("hy_AM-gor-medium.onnx", "Բարև, սա առաջին խոսողն է։"),
    ("en_US-lessac-medium.onnx", "And this is the second person speaking now."),
    ("hy_AM-gor-medium.onnx", "Ես նորից առաջին խոսողն եմ։"),
    ("en_US-lessac-medium.onnx", "Speaking again, as the second speaker."),
]


def synth(voice: str, text: str, target: Path) -> None:
    subprocess.run(
        [
            str(ROOT / ".venv/bin/piper"),
            "-m", str(VOICES / voice),
            "-f", str(target),
            "--sentence-silence", "0.3",
        ],
        input=text.encode("utf-8"),
        check=True,
        stdout=subprocess.DEVNULL,
    )


def main() -> None:
    missing = [v for v, _ in TURNS if not (VOICES / v).exists()]
    if missing:
        raise SystemExit(f"missing voices in eval/voices: {', '.join(sorted(set(missing)))}")

    clips: list[Path] = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (voice, text) in enumerate(TURNS):
            clip = Path(tmp) / f"turn_{i}.wav"
            synth(voice, text, clip)
            clips.append(clip)

        # Concatenate with silence between turns so the VAD closes each phrase.
        filter_graph = "".join(
            f"[{i}:a]aresample={SAMPLE_RATE},aformat=channel_layouts=mono,"
            f"apad=pad_dur=0.7[a{i}];"
            for i in range(len(clips))
        )
        inputs = "".join(f"[a{i}]" for i in range(len(clips)))
        filter_graph += f"{inputs}concat=n={len(clips)}:v=0:a=1[out]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error"]
        for clip in clips:
            cmd += ["-i", str(clip)]
        cmd += [
            "-filter_complex", filter_graph,
            "-map", "[out]",
            "-ar", str(SAMPLE_RATE), "-ac", "1",
            str(OUT),
        ]
        subprocess.run(cmd, check=True)

    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    print("expected labels: Speaker 1, Speaker 2, Speaker 1, Speaker 2")


if __name__ == "__main__":
    main()
