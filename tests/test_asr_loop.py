"""Word-loop handling of the transcriber, with the Whisper model stubbed out.

Whisper can get stuck repeating one word ("այդ այդ այդ ..."). Pinned down here: a loop
is detected, only a looped segment is decoded a second time, and a segment that still
loops is marked unclear instead of being passed on as a transcript.
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pytest

from src.asr import RETRY_NO_REPEAT_NGRAM, Transcriber, has_word_loop


class FakeWhisper:
    """Returns the queued texts in order and records the options of every call."""

    def __init__(self, *texts: str):
        self.texts = list(texts)
        self.calls: list[dict] = []

    def transcribe(self, audio, **options):
        self.calls.append(options)
        return [SimpleNamespace(text=self.texts.pop(0))], None


def make_transcriber(fake: FakeWhisper) -> Transcriber:
    transcriber = Transcriber.__new__(Transcriber)
    transcriber.language = "hy"
    transcriber.beam_size = 5
    transcriber.model = fake
    return transcriber


SPEECH = np.full(16_000, 0.2, dtype=np.float32)


@pytest.mark.parametrize(
    "text",
    ["Հայց այդ այդ այդ այդ այդ։", "այդ այդ այդ։", "ԱՅԴ այդ, այդ"],
)
def test_loop_is_detected_despite_punctuation_and_case(text):
    assert has_word_loop(text)


@pytest.mark.parametrize(
    "text",
    ["Բարև, ինչպե՞ս ես։", "շատ շատ լավ է", "", "այդ, այդ"],
)
def test_normal_speech_and_double_words_are_not_loops(text):
    assert not has_word_loop(text)


def test_normal_segment_is_decoded_once_without_the_repeat_blocker():
    fake = FakeWhisper("Բարև, ինչպե՞ս ես։")

    result = make_transcriber(fake).transcribe(SPEECH)

    assert result.text == "Բարև, ինչպե՞ս ես։"
    assert not result.retried and not result.unclear
    assert len(fake.calls) == 1
    assert "no_repeat_ngram_size" not in fake.calls[0]


def test_looped_segment_is_retried_with_the_repeat_blocker():
    fake = FakeWhisper("այդ այդ այդ այդ", "Հայերեն եմ խոսում։")

    result = make_transcriber(fake).transcribe(SPEECH)

    assert result.text == "Հայերեն եմ խոսում։"
    assert result.retried and not result.unclear
    assert fake.calls[1]["no_repeat_ngram_size"] == RETRY_NO_REPEAT_NGRAM


def test_segment_that_still_loops_is_marked_unclear():
    fake = FakeWhisper("այդ այդ այդ այդ", "այս այս այս")

    result = make_transcriber(fake).transcribe(SPEECH)

    assert result.retried and result.unclear
    assert len(fake.calls) == 2
