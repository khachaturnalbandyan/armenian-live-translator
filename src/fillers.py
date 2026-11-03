"""Fixed English for short Armenian interjections ("հա", "դե", "խո" ...).

Given a lone interjection, NLLB invents a sentence: in a live call "հա" came out as
"I'm not going to" and "դե" as "Well, what is it?". A segment made only of these words
gets the gloss below instead of going to the translator.
"""

from __future__ import annotations

import re

# "" means the word carries no meaning of its own in English (a particle).
FILLERS = {
    "հա": "yeah",
    "հաա": "yeah",
    "այո": "yes",
    "չէ": "no",
    "ոչ": "no",
    "դե": "well",
    "հը": "huh",
    "հե": "hey",
    "ըհը": "uh-huh",
    "էհ": "eh",
    "էէ": "uh",
    "ըը": "uh",
    "մմ": "mm",
    "հմ": "hmm",
    "ահ": "ah",
    "ախ": "ah",
    "օհ": "oh",
    "վայ": "oh",
    "խո": "",
    "բա": "",
    # Colloquial words NLLB does not know ("ախպեր" came out as "The scalp").
    "ախպեր": "bro",
    "ապեր": "bro",
    "հլը": "hold on",
}


def _words(text: str) -> list[str]:
    words = ["".join(ch for ch in word if ch.isalnum()).lower() for word in text.split()]
    return [word for word in words if word]


def _collapse(word: str, keep: int) -> str:
    """Shorten every run of one letter to `keep` letters: "հմմմ" -> "հմմ" / "հմ"."""
    return re.sub(r"(.)\1+", lambda run: run.group(1) * keep, word)


def _gloss(word: str) -> str | None:
    # Hesitations are written with the sound held ("հմմ", "հաաա", "ըըը"), so a word
    # also matches with its repeated letters shortened to two, then to one.
    for form in (word, _collapse(word, 2), _collapse(word, 1)):
        if form in FILLERS:
            return FILLERS[form]
    return None


def filler_translation(text: str) -> str | None:
    """The English for a segment made only of interjections, else None."""
    glosses = [_gloss(word) for word in _words(text)]
    if not glosses or None in glosses:
        return None
    return ", ".join(gloss for gloss in glosses if gloss)
