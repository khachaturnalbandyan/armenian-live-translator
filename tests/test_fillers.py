"""Short interjections get a fixed English gloss instead of an NLLB guess."""

from __future__ import annotations

import pytest

from src.fillers import filler_translation


@pytest.mark.parametrize(
    ("armenian", "english"),
    [
        ("հա։", "yeah"),
        ("Դե։", "well"),
        ("հա՞", "yeah"),
        ("դե հա", "well, yeah"),
        ("խո։", ""),
        ("հմմ", "hmm"),
        ("հաաա", "yeah"),
        ("ըըը", "uh"),
        ("մմմմ", "mm"),
        ("Դե, դե, դե։", "well, well, well"),
        ("ախպեր,", "bro"),
        ("հլը։", "hold on"),
    ],
)
def test_known_interjections_get_a_fixed_gloss(armenian, english):
    assert filler_translation(armenian) == english


@pytest.mark.parametrize("armenian", ["լավ է։", "Կապի ստուգում։", "հա, գնացինք", ""])
def test_anything_else_goes_to_the_translator(armenian):
    assert filler_translation(armenian) is None


def test_unclear_preview_keeps_the_first_words():
    from src.pipeline import unclear_preview

    assert unclear_preview("չի " * 100) == "չի չի չի չի չի չի …"
    assert unclear_preview("այդ այդ այդ") == "այդ այդ այդ"


def test_repeated_interjection_is_glossed_not_marked_unclear():
    from types import SimpleNamespace

    from src.asr import Transcript
    from src.pipeline import Pipeline

    printed = []
    pipeline = Pipeline.__new__(Pipeline)
    pipeline.transcriber = SimpleNamespace(
        transcribe=lambda audio: Transcript("Դե, դե, դե։", 1.0, 0.1, unclear=True)
    )
    pipeline.translator = SimpleNamespace(translate=lambda text: ("should not be used", 0.0))
    pipeline.printer = SimpleNamespace(segment=lambda **line: printed.append(line))
    pipeline.identifier = None
    pipeline.show_stats = False
    pipeline._started_at = 0.0
    pipeline._retries = pipeline._unclear = 0
    pipeline._latencies, pipeline._counts = [], {}

    segment = SimpleNamespace(audio=None, t_finalized=0.0, start=0.0)
    pipeline._handle(segment, SimpleNamespace(speaker="Me"))

    assert printed[0]["armenian"] == "Դե, դե, դե։"
    assert printed[0]["english"] == "well, well, well"
