# PLAN

Goal: a Python program that listens to a live Armenian conversation, captures **both**
the microphone and the system audio output, and prints each spoken phrase in the
terminal as Armenian text plus English translation, labelled by speaker, **within 5 s**
of the phrase ending. Everything runs locally; no cloud speech or translation APIs.

## Non-goals (per the brief)

GUI, installer, echo cancellation, named/remembered speakers, saving transcripts,
languages other than Armenian input.

## Modules

| Module | Input | Output | Notes |
| --- | --- | --- | --- |
| `src/capture.py` | device name or WAV path | 16 kHz mono float32 frames (256 ms) | `parec` for live sources; PipeWire `.monitor` sources are the "other side" of a call |
| `src/segmenter.py` | audio frames | `Segment(audio, start, end)` per spoken phrase | Silero VAD; closes on 350 ms pause or 6 s hard cut |
| `src/speakers.py` | segment audio | `Speaker 1..N`, stable per session | pyannote WeSpeaker embeddings + online clustering, CPU |
| `src/asr.py` | segment audio | Armenian text | faster-whisper `large-v3`, CUDA float16 |
| `src/translate.py` | Armenian text | English text | NLLB-200 distilled 600M |
| `src/display.py` | result | one formatted terminal line | `[hh:mm:ss] Speaker  HY: …  EN: …` |
| `src/pipeline.py` | one or two sources | stdout stream, latency stats | capture thread per source + single worker thread |
| `main.py` | CLI args | process | device listing, file input for eval, tuning flags |

## Milestones

1. **Walking skeleton** — mic → Armenian → English → terminal, measured latency. *(done)*
2. **Second source** — mic and system audio captured simultaneously, prefixed `Me` / `Speaker`. *(done)*
3. **Speaker identification** — pyannote embeddings on the remote stream, stable labels across the session. *(done)*
4. **Hardening and measurement** — real recordings in the eval set, tuning of VAD and models, failure paths. *(in progress)*
5. **Deliverables** — README, chats export, final QA pass.

## Risks

- **Armenian ASR quality.** Low-resource language; whisper large-v3 is the strongest
  local option we measured, but it still makes mistakes (13% CER on the synthetic set).
  Mitigation: keep the model choice measured, document limits honestly.
- **Speaker diarization on short turns.** Phrases under ~0.4 s are labelled `Speaker ?`
  rather than guessed; very similar voices can still be merged. Mitigation: exposed
  `--speaker-threshold`, and the uncertainty is visible in the output.
- **Latency with two streams.** One GPU, two concurrent recognition jobs. Mitigation:
  diarization only on the remote stream, and segments from the mic already labelled `Me`.
- **Model downloads at first run** (~3 GB whisper + ~2.4 GB NLLB) — document it.
