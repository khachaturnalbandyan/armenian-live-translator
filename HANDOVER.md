# HANDOVER

Summary of the second working session (Claude Code, Oct 29-30, 2026): what was done,
what was measured, where the project stands now and what comes next. This is a short
summary for starting a new chat. It is **not** the chat transcript: the full session
still has to be exported, unedited, into `chats/` (see "Open items").

## Where the project stands now

- The live program works: microphone (`Me`) + system audio (`Speaker 1..N`), Armenian
  text, English translation, about 1 s per line. Tested live on the microphone by the
  user; a real call with other people is still to do.
- Speech recognition is still faster-whisper `large-v3`. Its weak points, measured:
  - fast speech: CER rises from 6.5% (normal) to 10.1% (1.3x) and 12.2% (1.6x);
  - it sometimes gets stuck repeating one word ("այդ այդ այդ ..."); this is now
    handled (see step 6), but the change is **not committed yet**.
- The comparison tools exist, but there are **no real recordings yet**: every number
  below comes from 5 synthetic Piper phrases, one voice.

### Commits made in this session

| commit | what |
| --- | --- |
| `c3e77d3` | fix: remove `repetition_penalty` from ASR decoding (CER 17.7% -> 13.5%) |
| `0ffe631` | feat: model comparison and real-recording tools |
| `ed70b59` | fix: keep comparison results when one backend fails; add `sentencepiece` |

### Not committed yet

`src/asr.py`, `src/pipeline.py`, `tests/test_asr_loop.py`, `README.md`, `TESTS.md`:
the word-loop fix (step 6) and its documentation. This file (`HANDOVER.md`) is new too.

## What was done in this session, step by step

### 1. Read the brief and the tips

Read `Mathrix_AI_Coding_Challenge.docx` and `Mathrix_AI_Vibe_Coding_Tips.docx` and
summarised the requirements: two audio sources, Armenian ASR, English translation,
`Me` / `Speaker N` labels, at most 5 s latency, local models only, README with model
choices, and every AI chat exported to `chats/`.

### 2. Checked the repo against the brief

All required features are present. Problems found:

- no Git remote: the repo cannot be submitted as a link yet;
- `chats/` has only one session, and it starts after the code already existed: the
  sessions that built the project are missing;
- signs of AI tools other than Claude Cowork (`.freebuff/` folder, the style of
  `chat_session_01.md`, and this session is Claude Code), while the brief allows only
  Claude Cowork;
- README says segments close after 350 ms of silence; the code uses 500 ms;
- README has a duplicated ```` ```bash ```` line;
- live tests with a real call, real recordings and the offline check are still open.

### 3. Built the model comparison tools (commit `0ffe631`)

- `tools/record_eval.py`: shows 20 Armenian sentences one by one, records them (Enter to
  start / stop), saves WAVs to `eval/real/` (git-ignored) and the correct text to
  `eval/real/manifest.json`. Rejects silent or too-short takes. `--source call` records
  the other side of a call.
- `tools/compare_asr.py`: runs several recognisers on the same recordings, one model at
  a time (fits an 8 GB GPU). Reports CER, WER, latency, and CER by speaker and by source;
  `--show` prints every transcript, `--report` writes Markdown, `--segment` cuts audio
  with the live segmenter first.
- `tools/asr_backends.py`: `faster-whisper:<name>`, `hf-whisper:<repo>`, `mms:<repo>`,
  `seamless:<repo>`.
- `tools/scoring.py`: one shared CER/WER. Fixed a scoring bug: Armenian punctuation
  (`։ ՞ ՝`) used to count as errors. Now `և` and `եւ` also count as the same.
- 10 tests in `tests/test_scoring.py`.

### 4. Found and fixed an accuracy regression (commit `c3e77d3`)

The earlier commit "Improve Armenian ASR accuracy" (8fed087) made accuracy worse. Each of
its settings was measured separately:

| setting | CER |
| --- | --- |
| original code | 13.5% |
| code at that time | 17.7% |
| without `repetition_penalty=1.1` | 13.5% |

`repetition_penalty` was removed. Volume normalisation had no effect and was kept.

### 5. Compared four recognisers (synthetic set, 5 phrases)

| model | CER | WER | time per phrase |
| --- | --- | --- | --- |
| MMS-1B-all | 6.9% | 45.2% | 0.09 s |
| SeamlessM4T v2 large | 10.6% | 10.0% | 0.46 s |
| Whisper large-v3 (current) | 13.5% | 45.4% | 0.93 s |
| Whisper large-v3-turbo | 32.8% | 58.3% | 0.42 s |

- MMS: best letters, but joins words together and has no punctuation.
- SeamlessM4T: best words and punctuation on short phrases, but once replaced a phrase
  with a more common one ("շնորհիվ աստծո" -> "շնորհակալություն").
- Turbo sometimes answers in Latin letters.
- SeamlessM4T needed `sentencepiece` (added to `requirements.txt`). Its missing-package
  error first crashed the whole comparison, so `compare_asr.py` now keeps the other
  models' results and reports the failed one (commit `ed70b59`).

### 6. Live test and the word-loop fix (not committed yet)

The user ran the program live on the microphone. Speed was fine (under 1 s per line),
but one line came out as `Հայց այդ այդ այդ այդ այդ`. Measured fixes:

| fix | result |
| --- | --- |
| retry with temperature | still loops or garbage, up to 3 s: rejected |
| `no_repeat_ngram_size=3` on every segment | stops loops, but CER 13.5% -> 16.0%: rejected |
| `no_repeat_ngram_size` 4 / 5 on every segment | CER 14.0% / 14.5%: rejected |

Implemented instead: detect a loop (the same word 3+ times in a row), decode **only that
segment** again with `no_repeat_ngram_size=3`, and show `[unclear]` without translation
if it still loops. Normal segments are untouched (CER stays 13.5%). On the replay that
looped before, both loops were fixed, with +0.5-0.9 s and a maximum of 1.75 s per line.
5 tests in `tests/test_asr_loop.py`; 28 tests pass in total.

### 7. Fast speech

The user reported that fast speech is recognised badly. Simulated with the synthetic
phrases sped up (1.3x, 1.6x) and joined into one stream without pauses:

| CER, continuous speech | normal | 1.3x | 1.6x |
| --- | --- | --- | --- |
| Whisper large-v3 | 6.5% | 10.1% | 12.2% |
| MMS-1B-all | 5.0% | 7.9% | 6.5% |
| SeamlessM4T v2 | 23.7% | 33.8% | 20.1% |

- The segmenter is not the cause: changing the segment length moved CER by only 1-2
  points.
- Whisper gets worse with speed; MMS stays almost flat.
- SeamlessM4T rewrites longer, fast speech: it dropped "մի ուշացիր" and invented
  "Բարեւ ձեզ, բարի օր". The output looks fluent, so the errors cannot be seen live.
  Not suitable.
- Found on the way: the 6 s "hard cut" (`src/segmenter.py:113`) is only checked on a
  silent frame, so someone who never pauses produces one long segment, and their line
  appears only after they stop. The README describes this wrongly ("can split a sentence
  mid-word").
- Caveat: sped-up synthetic speech is not real fast speech (swallowed syllables, words
  run together). Real fast recordings are needed before switching models.

## Open items, in order

1. Commit the word-loop fix (step 6) and this file.
2. Record real speech, normal and fast, and include at least one other person over a call:
   ```bash
   python tools/record_eval.py --speaker <name>
   python tools/record_eval.py --speaker <name>-fast
   python tools/compare_asr.py faster-whisper:large-v3 mms:facebook/mms-1b-all --show --report eval/results.md
   ```
3. If MMS wins on real speech: check whether NLLB still translates MMS output (words
   joined, no punctuation) well, then add it to the live program as `--asr mms`.
   Write the decision and the numbers into `DECISIONS.md`.
4. Fix the README: 350 ms -> 500 ms, the duplicated ```` ```bash ````, and the wrong
   description of the 6 s cut.
5. Live checks before the interview: a real call with 2+ Armenian speakers (speaker
   labels, `--speaker-threshold`), a 10-minute session (0 lines over 5 s), and one run
   with Wi-Fi off.
6. Submission: create a Git remote and push, export **every** AI chat session (including
   this one) in full into `chats/`, one `.md` file each, and decide how to explain the
   tools used, since the brief allows only Claude Cowork.
