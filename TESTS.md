# TESTS

Acceptance checks derived from the brief, not from the code. Run this list before the
interview; update the status column instead of trusting memory.

## Functional

| # | Check | How | Status |
| --- | --- | --- | --- |
| F1 | Lists capture devices, marks microphones and system audio | `./run.sh --list-devices` | ✅ |
| F2 | Captures the microphone continuously | `./run.sh` in silence → exits with "No speech detected" | ✅ |
| F3 | Captures the **system audio output** as a second source | `./run.sh --system-audio` with audio playing | ✅ devices open live; a real call is still unchecked |
| F4 | Both sources captured **at the same time** | `--device <mic> --system-audio` | ✅ both streams open together; interleaved output verified with `--input` + `--input-system` |
| F5 | Armenian speech becomes Armenian text | `./run.sh --input eval/audio/tts_03.wav` | ✅ (13% CER on synthetic) |
| F6 | Each segment gets an English translation | same run, `EN:` column | ✅ |
| F7 | Microphone segments are labelled `Me` | `./run.sh` | ✅ |
| F8 | System-audio speakers are split as `Speaker 1..N`, stable per session | `./run.sh --input eval/audio/two_voices.wav --diarize` | ✅ A,B,A,B pattern on the two-voice test with a real call still needed |
| F9 | Line contains time, speaker, Armenian, English | any run | ✅ |
| F10 | Segments appear while the conversation is still running | any run | ✅ |

## Performance

| # | Check | Target | Status |
| --- | --- | --- | --- |
| P1 | End of phrase → English line | ≤ 5 s | ✅ p50 0.93 s, max 1.12 s with speaker ID on (realtime, `--stats`) |
| P2 | No segment over the budget over a 10-minute session | 0 | ⏳ needs a long session |
| P3 | ASR + MT alone per phrase | ≤ 2 s | ✅ p50 0.90 s |

Measuring latency: run with `--stats`; every line prints ASR/MT time and latency from
the VAD cut, and the session ends with p50/p95/max and the count of segments over 5 s.

## Quality regression

```bash
python tools/build_eval_audio.py     # rebuild the synthetic set (needs piper-tts)
python tools/eval_offline.py --models large-v3 --translate
```

Current numbers (5 synthetic phrases, RTX 4060, float16):

| model | CER | latency p50 (ASR+MT) |
| --- | --- | --- |
| large-v3 | 13.2% | 0.90 s |
| large-v3-turbo | 19.5% | 0.42 s |

Run `tools/eval_offline.py --modes stream` after changing segmentation; it feeds the
output of the real `Segmenter` into the recogniser.

**Rule:** any change to decoding settings is measured before it is committed. The
`repetition_penalty=1.1` added in 8fed087 raised CER from 13.5% to 17.7% on this set and
was removed after measuring each setting separately.

Real recordings: `tools/record_eval.py` + `tools/compare_asr.py` (see README,
"Comparing speech recognisers"). ⏳ no real recordings yet.

### Speaker identification

```bash
python tools/build_diarization_test.py                                    # build the two-voice clip
.venv/bin/python -m pytest tests/ -q                                      # clustering logic
./run.sh --input eval/audio/two_voices.wav --diarize --stats              # end to end
```

Ranked by the embedding model of pyannote 3.1 (WeSpeaker ResNet34, 256 dims, CPU):

| check | result |
| --- | --- |
| Two different voices get different labels | ✅ `Speaker 1, Speaker 2, Speaker 1, Speaker 2` |
| A returning speaker keeps the earlier label | ✅ second and fourth turns matched the first and third |
| Embedding cost per segment | ✅ 0.03-0.07 s (CPU), does not touch the 5 s budget |
| Still one label for one voice over 5 phrases | ✅ (`tts_01`-`tts_05`, cosine 0.63-0.89) |
| Threshold behaviour, short-clip guard | ✅ 8 unit tests in `tests/test_speakers.py` |

The second voice in the test is English (Piper ships one Armenian voice); that is fine
for speaker embeddings, which describe the voice rather than the language.

**TODO before the interview:** repeat this with 10-20 real recordings of 2-3 speakers
(mixed microphone + call quality). The synthetic voice is too clean to predict accuracy.

## Robustness

| # | Check | Status |
| --- | --- | --- |
| R1 | Ctrl+C prints a summary and exits cleanly | ✅ |
| R2 | Missing/bad CUDA libraries give a readable error, not a traceback | ✅ |
| R3 | Choosing a non-existent device fails with a clear message | ✅ |
| R4 | Silence does not produce hallucinated lines | ✅ (VAD gate, "No speech detected") |
| R5 | A failing segment does not kill the session | ✅ (logged, session continues) |
| R6 | Long monologue is cut at 6 s and still transcribed | ⏳ |
| R7 | Fully offline after first download (no network calls while running) | ⏳ verify before interview |
| R8 | Word loops ("այդ այդ այդ ...") are retried, and shown as `[unclear]` if they persist | ✅ 5 unit tests in `tests/test_asr_loop.py`; both loops in the `two_voices.wav` replay fixed by the retry (+0.5-0.9 s), eval CER unchanged at 13.5% |
