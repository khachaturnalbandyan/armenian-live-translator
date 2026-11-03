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


def test_loads_from_cached_snapshot_folder(monkeypatch):
    import huggingface_hub

    from src.asr_seamless import _local_snapshot

    monkeypatch.setattr(
        huggingface_hub, "try_to_load_from_cache", lambda repo, name: f"/cache/{repo}/snap/{name}"
    )
    assert _local_snapshot("facebook/x") == "/cache/facebook/x/snap"


def test_falls_back_to_repo_id_before_first_download(monkeypatch):
    import huggingface_hub

    from src.asr_seamless import _local_snapshot

    monkeypatch.setattr(huggingface_hub, "try_to_load_from_cache", lambda repo, name: None)
    assert _local_snapshot("facebook/x") == "facebook/x"
