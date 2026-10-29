"""Scoring rules of the evaluation tools: what counts as a recognition error."""

from __future__ import annotations

import json
import wave

import numpy as np
import pytest

from tools.scoring import cer, load_manifest, load_wav, normalize_words, percentile, wer


def test_armenian_punctuation_is_not_an_error():
    assert cer("Բարև, ինչպե՞ս ես։", "Բարև ինչպես ես") == 0.0


def test_ligature_and_two_letter_spelling_match():
    assert cer("և", "եւ") == 0.0


def test_case_is_ignored():
    assert normalize_words("ԲԱՐԵՎ Hello") == ["բարեվ", "hello"]


def test_one_wrong_letter_in_ten():
    assert cer("աբգդեզէըթժ", "աբգդեզէըթի") == pytest.approx(0.1)


def test_wer_counts_whole_words():
    assert wer("ես լավ եմ", "ես վատ եմ") == pytest.approx(1 / 3)


def test_empty_hypothesis_is_a_full_miss():
    assert cer("բարև", "") == 1.0
    assert wer("բարև", "") == 1.0


def test_percentile_of_empty_list_is_zero():
    assert percentile([], 0.5) == 0.0


def test_manifest_paths_are_relative_to_the_manifest(tmp_path):
    audio = tmp_path / "a.wav"
    with wave.open(str(audio), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(16_000)
        wav.writeframes(np.zeros(160, dtype=np.int16).tobytes())
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([{"file": "a.wav", "reference": "բարև"}]), "utf-8")

    items = load_manifest(manifest)

    assert items[0].path == audio
    assert items[0].speaker == "unknown"
    assert load_wav(items[0].path).shape == (160,)


def test_missing_audio_fails_loudly(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps([{"file": "gone.wav", "reference": "x"}]), "utf-8")
    with pytest.raises(FileNotFoundError, match="gone.wav"):
        load_manifest(manifest)


def test_wrong_sample_rate_fails_loudly(tmp_path):
    audio = tmp_path / "a.wav"
    with wave.open(str(audio), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(44_100)
        wav.writeframes(np.zeros(10, dtype=np.int16).tobytes())
    with pytest.raises(ValueError, match="16 kHz"):
        load_wav(audio)
