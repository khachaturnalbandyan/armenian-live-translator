# PLAN

Goal: a Python program that listens to a live Armenian conversation, captures **both**
the microphone and the system audio output, and prints each spoken phrase in the
terminal as Armenian text plus English translation, labelled by speaker, **within 5 s**
of the phrase ending. Everything runs locally; no cloud speech or translation APIs.

This file started as the plan before any code was written; it is kept up to date with
what was built. Why things changed is in [DECISIONS.md](DECISIONS.md), the measurements
are in [TESTS.md](TESTS.md) and `eval/`.

## Non-goals (per the brief)

GUI, installer, echo cancellation, named/remembered speakers, saving transcripts,
languages other than Armenian input. (`--save-audio` exists only for debugging and
evaluation; it is off by default.)

## Modules

| Module | Input | Output | Notes |
| --- | --- | --- | --- |
| `src/capture.py` | device name or WAV path | 16 kHz mono float32 chunks | `parec` for live sources; PipeWire `.monitor` sources are the "other side" of a call |
| `src/segmenter.py` | audio chunks | `Segment(audio, start, end)` per spoken phrase | Silero VAD; closes on a 500 ms pause, or at 6 s on the next silent frame |
| `src/speakers.py` | segment audio | `Speaker 1..N`, stable per session | pyannote WeSpeaker embeddings + online clustering; a new speaker needs ≥ 1.5 s of speech |
| `src/asr_seamless.py` | segment audio | Armenian text | SeamlessM4T v2 large, CUDA float16 (default) |
| `src/asr.py` | segment audio | Armenian text | faster-whisper, Armenian fine-tune of large-v3 turbo (`--asr whisper`); shared text cleanup and loop check |
| `src/fillers.py` | Armenian text | fixed English gloss or nothing | short interjections (հա, դե, հմ …) skip the translator |
| `src/translate.py` | Armenian text | English text | NLLB-200 distilled 600M |
| `src/display.py` | result | one formatted terminal line | `[hh:mm:ss] Speaker  HY: …  EN: …`, stamped with the end of speech |
| `src/recorder.py` | segments | WAV per phrase + `session.jsonl` | only with `--save-audio` |
| `src/pipeline.py` | one or two sources | stdout stream, latency stats | capture thread per source + single GPU worker thread |
| `main.py` | CLI args | process | device listing, file input for eval, model and tuning flags |

## Milestones

1. **Walking skeleton**: mic → Armenian → English → terminal, measured latency. *(done)*
2. **Second source**: mic and system audio captured simultaneously, prefixed `Me` / `Speaker`. *(done)*
3. **Speaker identification**: pyannote embeddings on the remote stream, stable labels across the session. *(done)*
4. **Hardening and measurement**: real recordings in the eval set, ASR model comparison
   and switch to SeamlessM4T, VAD tuning, fillers, offline loading. *(done)*
5. **Deliverables**: README, decisions, test log, final QA pass. *(done)*

## Risks

- **Armenian ASR quality.** Low-resource language. Measured on 40 real recordings of one
  speaker: SeamlessM4T v2 2.9% CER, the Armenian whisper turbo 6.9%, whisper large-v3
  ~13%. Other voices, accents and call audio are not measured yet. Mitigation: keep the
  model choice measured, keep a fallback (`--asr whisper`), document limits honestly.
- **Translation of colloquial Armenian.** NLLB is trained on written language and
  misreads spoken forms. This is now the weakest step. Open: normalise colloquial forms
  before translation, or hide low-confidence lines.
- **Speaker diarization on short turns.** Phrases under ~0.4 s are labelled `Speaker ?`;
  phrases under 1.5 s can only join a known speaker, never create a new one. Very
  similar voices can still be merged. Mitigation: `--speaker-threshold`.
- **Latency with two streams.** One GPU worker serves both sources, so one slow call
  holds up the queue. Measured over 10 minutes: p50 0.36 s, max 2.74 s, 0 lines over
  5 s (an earlier run had one 16 s stall, most likely memory swapping).
- **Model downloads at first run** (several GB for SeamlessM4T and NLLB). After that the
  models load from the local cache and the program runs offline (`HF_HUB_OFFLINE=1`).
