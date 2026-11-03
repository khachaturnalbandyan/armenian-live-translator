"""Armenian speech recognition with faster-whisper (CTranslate2, local)."""

from __future__ import annotations

import time
from dataclasses import dataclass

import numpy as np
from faster_whisper import WhisperModel

from .fillers import is_filler

# Whisper large-v3-turbo fine-tuned on Armenian, already converted for faster-whisper.
# On the synthetic eval set: CER 6.0% vs 13.5% for stock large-v3, 7.9% vs 18.7% on
# speech sped up 1.6x, and about twice as fast. See DECISIONS.md (D1).
DEFAULT_MODEL = "hurricup/whisper-large-v3-turbo-armenian-ct2"

# The Armenian fine-tune writes subtitle-style dialogue marks: a leading "- " and "…"
# in place of a sentence end. Neither is speech, and both end up in the translation.
DIALOGUE_DASH = "-–—"
ELLIPSIS = "…"
DISFLUENCY_TAG = "#"
MARKDOWN_BOLD = "*"

# Whisper sometimes gets stuck repeating one word ("այդ այդ այդ այդ ..."). The same
# word this many times in a row is treated as such a loop.
LOOP_RUN = 3
# Used only to re-decode a looped segment. Always on, it raises CER on normal Armenian
# (13.5% -> 16.0% on the eval set), so normal segments are never decoded with it.
RETRY_NO_REPEAT_NGRAM = 3


@dataclass
class Transcript:
    text: str
    audio_seconds: float
    elapsed: float
    retried: bool = False  # the first decode looped and the segment was decoded again
    unclear: bool = False  # it still looped after the retry: the text is not usable


def has_word_loop(text: str, run: int = LOOP_RUN) -> bool:
    """True if one word repeats `run` or more times in a row, ignoring punctuation.

    Interjections do not count: people really say "հա, հա, հա" and "դե դե դե".
    """
    words = ["".join(ch for ch in word if ch.isalnum()).lower() for word in text.split()]
    words = [word for word in words if word]
    return any(
        len(set(words[i : i + run])) == 1 and not is_filler(words[i])
        for i in range(len(words) - run + 1)
    )


def clean_text(text: str) -> str:
    """Drop what is not speech: dialogue dashes, "…" and disfluency tags.

    The dashes and "…" come from the Whisper fine-tune; SeamlessM4T writes hesitations
    as tags ("#err", "#hmm"), sometimes opens a line with Markdown "**", and opens each
    line of a dialogue with "- ".
    """
    words = text.replace(ELLIPSIS, " ").split()
    words = [word for word in words if not word.startswith(DISFLUENCY_TAG)]
    words = [word.strip(MARKDOWN_BOLD) for word in words]
    words = [word for word in words if word]
    words = [word for word in words if word.strip(DIALOGUE_DASH)]
    if words:
        words[0] = words[0].lstrip(DIALOGUE_DASH)
    text = " ".join(words)
    # Whatever is left once the tags are gone may be bare punctuation ("#err ։").
    return text if any(ch.isalnum() for ch in text) else ""


class Transcriber:
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        device: str = "cuda",
        compute_type: str = "float16",
        language: str = "hy",
        beam_size: int = 5,
    ):
        self.language = language
        self.beam_size = beam_size
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio: np.ndarray) -> Transcript:
        started = time.monotonic()
        if len(audio) == 0:
            return Transcript(text="", audio_seconds=0.0, elapsed=0.0)

        # Normalize volume to help whisper with quiet microphones
        peak = float(np.max(np.abs(audio)))
        if peak > 1e-4:
            audio = audio / max(peak, 0.1) * 0.95

        text = self._decode(audio)
        retried = unclear = False
        if has_word_loop(text):
            retried = True
            text = self._decode(audio, no_repeat_ngram_size=RETRY_NO_REPEAT_NGRAM)
            unclear = has_word_loop(text)

        elapsed = time.monotonic() - started
        return Transcript(
            text=text,
            audio_seconds=len(audio) / 16_000,
            elapsed=elapsed,
            retried=retried,
            unclear=unclear,
        )

    def _decode(self, audio: np.ndarray, **options) -> str:
        segments, _info = self.model.transcribe(
            audio,
            language=self.language,
            beam_size=self.beam_size,
            no_speech_threshold=0.6,
            # No repetition_penalty: 1.1 raised CER from 13.5% to 17.7% on the eval set,
            # because Armenian legitimately repeats the same tokens.
            condition_on_previous_text=False,
            without_timestamps=True,
            **options,
        )
        # faster-whisper returns a lazy generator: all the work happens here, so the
        # timer in transcribe() has to wrap the consumption of it, not the call above.
        return " ".join(clean_text(seg.text) for seg in segments).strip()
