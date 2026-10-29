"""Clean-up of the subtitle marks the Armenian Whisper fine-tune writes."""

from __future__ import annotations

import pytest

from src.asr import clean_text


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("- Բարև ինչպես ես…", "Բարև ինչպես ես"),
        ("– Լավ եմ, շնորհիվ աստծո։", "Լավ եմ, շնորհիվ աստծո։"),
        ("Այսօր եղանակը լավ է… Արի գնանք։", "Այսօր եղանակը լավ է Արի գնանք։"),
        ("  Ժողովը սկսվում է ժամը երեքին։  ", "Ժողովը սկսվում է ժամը երեքին։"),
    ],
)
def test_removes_dialogue_dash_and_ellipsis(raw, expected):
    assert clean_text(raw) == expected


def test_keeps_hyphen_inside_text():
    assert clean_text("Երևան-Գյումրի ճանապարհը") == "Երևան-Գյումրի ճանապարհը"


def test_dash_only_becomes_empty():
    assert clean_text("- …") == ""
