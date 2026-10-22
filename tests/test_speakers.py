"""Clustering logic of the speaker identifier, without loading any model.

The embedding call is stubbed out, so this runs in milliseconds and pins down the
behaviour that matters: the same voice keeps its label, a different voice gets a new
one, and too-short segments are labelled "Speaker ?" instead of inventing a speaker.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.speakers import SpeakerIdentifier


def make_identifier(threshold: float = 0.55) -> SpeakerIdentifier:
    """A real identifier with the model and the audio path taken out."""
    identifier = SpeakerIdentifier.__new__(SpeakerIdentifier)
    identifier.threshold = threshold
    identifier.sample_rate = 16_000
    identifier.min_samples = int(0.4 * 16_000)
    identifier._sums = []
    identifier._counts = []
    identifier.last_embed_seconds = 0.0
    return identifier


def unit(*values: float) -> np.ndarray:
    vector = np.asarray(values, dtype=np.float32)
    return vector / np.linalg.norm(vector)


def feed(identifier: SpeakerIdentifier, vector: np.ndarray | None, seconds: float = 2.0) -> str:
    """Run one segment of `seconds` through `identify`, returning the given vector."""
    audio = np.zeros(int(seconds * identifier.sample_rate), dtype=np.float32)
    identifier._embed = lambda _audio: vector  # type: ignore[method-assign]
    return identifier.identify(audio)


def test_same_voice_keeps_its_label() -> None:
    identifier = make_identifier()
    voice = unit(1.0, 0.2, 0.0, 0.1)

    first = feed(identifier, voice)
    second = feed(identifier, unit(1.0, 0.25, 0.05, 0.1))  # same speaker, slightly different

    assert first == "Speaker 1"
    assert second == "Speaker 1"
    assert identifier.speaker_count == 1


def test_different_voice_gets_a_new_label() -> None:
    identifier = make_identifier()
    first = feed(identifier, unit(1.0, 0.0, 0.0, 0.0))
    second = feed(identifier, unit(0.0, 0.0, 1.0, 0.0))

    assert (first, second) == ("Speaker 1", "Speaker 2")
    assert identifier.speaker_count == 2


def test_returning_speaker_is_recognised() -> None:
    identifier = make_identifier()
    a = unit(1.0, 0.0, 0.0, 0.0)
    b = unit(0.0, 1.0, 0.0, 0.0)

    labels = [feed(identifier, a), feed(identifier, b), feed(identifier, a), feed(identifier, b)]

    assert labels == ["Speaker 1", "Speaker 2", "Speaker 1", "Speaker 2"]
    assert identifier.speaker_count == 2


def test_short_segment_is_not_given_a_speaker() -> None:
    identifier = make_identifier()
    label = feed(identifier, unit(1.0, 0.0, 0.0, 0.0), seconds=0.2)

    assert label == "Speaker ?"
    assert identifier.speaker_count == 0


def test_threshold_decides_how_willingly_a_new_speaker_appears() -> None:
    strict = make_identifier(threshold=0.99)
    similar = unit(1.0, 0.6, 0.0, 0.0)

    feed(strict, unit(1.0, 0.0, 0.0, 0.0))
    label = feed(strict, similar)

    assert label == "Speaker 2"  # cosine ~0.86 < 0.99


@pytest.mark.parametrize("threshold", [0.3, 0.55, 0.8])
def test_identical_voice_never_creates_a_second_speaker(threshold: float) -> None:
    identifier = make_identifier(threshold=threshold)
    voice = unit(0.3, -0.4, 0.5, 0.7)

    assert {feed(identifier, voice) for _ in range(5)} == {"Speaker 1"}
