"""SeamlessTranscriber's contract with the pipeline, with the model stubbed out."""

from __future__ import annotations

import numpy as np

from src.asr_seamless import SeamlessTranscriber


def make_transcriber(text: str) -> SeamlessTranscriber:
    transcriber = SeamlessTranscriber.__new__(SeamlessTranscriber)
    transcriber._decode = lambda audio: text
    return transcriber


SPEECH = np.full(16_000, 0.2, dtype=np.float32)


def test_returns_text_and_audio_length():
    transcript = make_transcriber("Բարև, ինչպես ես։").transcribe(SPEECH)
    assert transcript.text == "Բարև, ինչպես ես։"
    assert transcript.audio_seconds == 1.0
    assert not transcript.unclear


def test_word_loop_is_marked_unclear():
    transcript = make_transcriber("այդ այդ այդ այդ").transcribe(SPEECH)
    assert transcript.unclear


def test_empty_audio_is_not_decoded():
    transcript = make_transcriber("should not appear").transcribe(np.array([], dtype=np.float32))
    assert transcript.text == ""
