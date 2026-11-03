"""--save-audio: every live segment is kept as a WAV next to what was shown for it."""

from __future__ import annotations

import json
import wave

import numpy as np

from src.recorder import SegmentRecorder


def test_saves_segment_wav_and_its_transcript(tmp_path):
    recorder = SegmentRecorder(tmp_path)
    audio = np.linspace(-0.5, 0.5, 16_000, dtype=np.float32)

    recorder.save(audio, source="system audio", speaker="Speaker 1", at=12.3,
                  armenian="Բարև", english="Hello")
    recorder.save(audio[:8000], source="mic", speaker="Me", at=14.0,
                  armenian="հա", english="yeah")

    lines = [json.loads(line) for line in (tmp_path / "session.jsonl").read_text("utf-8").splitlines()]
    assert [line["speaker"] for line in lines] == ["Speaker 1", "Me"]
    assert lines[0] == {
        "file": "0001_system-audio.wav",
        "source": "system audio",
        "speaker": "Speaker 1",
        "at": 12.3,
        "seconds": 1.0,
        "armenian": "Բարև",
        "english": "Hello",
    }
    with wave.open(str(tmp_path / lines[1]["file"])) as wav:
        assert (wav.getframerate(), wav.getnchannels(), wav.getsampwidth()) == (16_000, 1, 2)
        assert wav.getnframes() == 8000


def test_loud_audio_is_clipped_not_wrapped(tmp_path):
    recorder = SegmentRecorder(tmp_path)
    recorder.save(np.array([2.0, -2.0], dtype=np.float32), source="mic", speaker="Me",
                  at=0.0, armenian="x", english="x")

    with wave.open(str(tmp_path / "0001_mic.wav")) as wav:
        samples = np.frombuffer(wav.readframes(2), dtype=np.int16)
    assert samples.tolist() == [32767, -32767]
