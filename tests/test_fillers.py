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
