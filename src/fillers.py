"""Fixed English for short Armenian interjections ("հա", "դե", "խո" ...).

Given a lone interjection, NLLB invents a sentence: in a live call "հա" came out as
"I'm not going to" and "դե" as "Well, what is it?". A segment made only of these words
gets the gloss below instead of going to the translator.
"""

from __future__ import annotations

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
}


def _words(text: str) -> list[str]:
    words = ["".join(ch for ch in word if ch.isalnum()).lower() for word in text.split()]
    return [word for word in words if word]


def filler_translation(text: str) -> str | None:
    """The English for a segment made only of interjections, else None."""
    words = _words(text)
    if not words or any(word not in FILLERS for word in words):
        return None
    return ", ".join(gloss for gloss in (FILLERS[word] for word in words) if gloss)
