# DECISIONS

Short log of choices that were not obvious, with the reason they were made.
Numbers come from `tools/eval_offline.py` on the synthetic Armenian set in `eval/audio`
(5 phrases, Piper `hy_AM-gor-medium`), CUDA float16 on an RTX 4060 Laptop.

## D1 - Speech recognition: SeamlessM4T v2, Armenian Whisper turbo as fallback

Updated 2026-11-03: the default is SeamlessM4T v2 large (`--asr seamless`), chosen on
real recordings; see "Real recordings" below. `--asr whisper` runs the Apache-2.0 model
described next, which was the default from 2026-10-30 to 2026-11-03.

### Armenian fine-tune of Whisper large-v3-turbo (`--asr whisper`)

Since 2026-10-30 `--asr whisper` uses `hurricup/whisper-large-v3-turbo-armenian-ct2`
(Apache-2.0, already in CTranslate2 format, so it runs in the same faster-whisper code).
Measured with `tools/compare_asr.py`; full output in `eval/results-synthetic.md`.

| model | CER | WER | s / phrase | CER 1.0x / 1.3x / 1.6x, continuous |
| --- | --- | --- | --- | --- |
| `hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.0% | 24.0% | 0.33 | 5.8% / 7.9% / **7.9%** |
| `ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (CTC) | **4.9%** | 21.1% | 0.05 | 3.6% / 6.5% / 17.3% |
| `facebook/mms-1b-all` (CTC) | 6.9% | 45.2% | 0.07 | 7.9% / 9.4% / 10.1% |
| `large-v3` (previous default) | 13.5% | 45.4% | 0.82 | 10.8% / 15.8% / 18.7% |

Why the Armenian turbo: half the CER of `large-v3`, it barely degrades on fast speech
(the user's main complaint), it keeps punctuation and word boundaries (NLLB needs them),
and it is about twice as fast. w2v-BERT has the lowest CER on normal speech, but it
collapses at 1.6x, joins words and has no punctuation. `arampacha/whisper-large-hy-2`
could not be run (its generation config is too old for current transformers).

The fine-tune writes subtitle marks ("- " at the start, "…" for a sentence end);
`src/asr.py:clean_text` removes them before translation.

Caveat: the same 5 synthetic phrases, one voice. Confirm on real recordings
(`tools/record_eval.py`) before the interview; `--model large-v3` restores the old model.

### Original choice: `large-v3`

Measured, transcription only plus NLLB:

| model | CER | latency p50 (ASR+MT) |
| --- | --- | --- |
| `large-v3` | **13.2%** | 0.90 s |
| `large-v3-turbo` | 19.5% | 0.42 s |

Turbo is twice as fast but roughly 6 points worse on Armenian, and `large-v3` already
fits the 5 s budget with a wide margin. Alternatives considered: a wav2vec2/XLSR
Armenian fine-tune (no punctuation or casing, usually trained on read speech, weaker on
conversational audio), and Vosk (small models, clearly weaker). Cloud APIs are out of
scope by rule.

Rejected on evidence: `large-v3-turbo`. Revisit if the real-recording eval shows the
gap closes.

### Real recordings: SeamlessM4T becomes the default (2026-10-30, 2026-11-03)

20 sentences, one speaker, laptop microphone; full output in `eval/results-real.md`.

| CER | normal | fast | joined 10-16 s, normal | joined 10-16 s, fast |
| --- | --- | --- | --- | --- |
| `seamless-m4t-v2-large` | **0.7%** | **2.5%** | **0.7%** | **2.3%** |
| Armenian turbo (`--asr whisper`) | 2.6% | 8.2% | 2.4% | 6.5% |
| w2v-BERT | 2.4% | 6.0% | - | - |
| `large-v3` | 13.1% | 13.2% | - | - |

`src/asr_seamless.py`; about 4.6 GB of GPU memory together with NLLB.

The risk was that it replaces unusual phrases with common ones, as it did on the
synthetic set. A live test on 2026-11-03 with 12 hard sentences (court, hospital,
Amsterdam, AI terms, prices, a date and time, a phone number, questions, two long fast
sentences) did not show it: 9 of 12 came out word for word, the other 3 differed in one
word form (e.g. "գտնվում է" -> "գտնվող") with the meaning kept. 0.25-0.97 s per line
including translation. The only wrong English was NLLB turning "Գյումրի" into "Guam".
By the same lines, the previous live test with the Whisper turbo turned this kind of
sentence into nonsense.

Fed through the live segmenter in the live read size (`compare_asr.py --segment`,
`eval/results-real-live.md`, 2026-11-03), the 40 recordings give CER 2.9% for Seamless
(0.9% normal, 4.9% fast) and 6.9% for the turbo. Earlier `--segment` numbers pushed the
whole file at once; segment edges then differ by tens of milliseconds, and that alone
changed one Seamless transcript ("շնորհակալ եմ" -> "հիմա այնտեղ եմ"). Its errors are
fluent substitutions like that one, which read as correct text.

Made the default on that evidence. Trade-offs:
- License CC-BY-NC-4.0, non-commercial use only. Fine for this challenge; a commercial
  build would use `--asr whisper` (Apache-2.0).
- Still one speaker, one microphone, no call audio. The live test was compared by text
  only (live audio is not saved).

## D2 - Translation: NLLB-200-distilled-600M, greedy decoding

Armenian → English (`hye_Armn` → `eng_Latn`). NLLB is trained on this pair directly and
handles punctuation and sentence case. Greedy (`num_beams=1`) because beam search added
latency without a visible quality gain at this size. Measured: 0.1-0.45 s per phrase;
"S" in the eval output shows translations are sane ("The weather … is very good").

Alternatives considered: `Helsinki-NLP/opus-mt-hy-en` (smaller, faster, but noisier and
trained on old parallel data), Argos Translate (very fast, but its hy→en package quality
is below NLLB), and the full 1.3B/3.3B NLLB variants (better, but ~4x slower and heavier
for a 5 s budget).

## D3 - Segmentation: Silero VAD endpointing, not fixed windows

Latency must be measured from the end of the phrase, so the program cannot wait for a
fixed-size window to fill. Segments close after 350 ms of silence (configurable), which
costs 0.35 s of the budget and keeps phrases intact. Whisper is also given 200 ms of
padding around the cut audio: cutting exactly at the VAD boundary truncates consonants
and measurably hurts the transcript.

## D4 - Capture: PipeWire `.monitor` sources instead of a virtual loopback driver

The brief's macOS setup (BlackHole + Multi-Output) exists because macOS has no way to
record the output device. Linux/PipeWire exposes every sink as a `.monitor` source, so
"the other side of the call" is just another capture device and the user keeps hearing
the call normally. `src/capture.py` talks to `parec`, so the same code path works for
both the microphone and the monitor.

## D5 - CUDA libraries: pip wheels, not a system CUDA install

CTranslate2 (faster-whisper's backend) links against CUDA 12 cuBLAS/cuDNN, while the
installed PyTorch wheel bundles CUDA 13. Installing `nvidia-cublas-cu12` /
`nvidia-cudnn-cu12` into the venv and prepending their `lib` directories in `run.sh`
fixes it without a system package, sudo, or a rebuild. Without them the first CUDA
transcription fails with `libcublas.so.12 is not found`.

## D6 - Speaker identification: pyannote embeddings clustered online, not the 3.1 pipeline

Chosen with the user: pyannote 3.1 is the best local speaker separation available. But
its pipeline is *offline*: it needs the whole recording before it can label a single
segment, which contradicts the 5 s latency budget. So we keep the part of 3.1 that does
the voice work - `pyannote/wespeaker-voxceleb-resnet34-LM`, the embedding model that
pipeline uses internally - and cluster its output online instead:

- every closed segment is embedded into a 256-dimensional voice vector;
- cosine similarity against the running centroid of each known speaker; above 0.55 it is
  that speaker (and the centroid is updated), below it a new `Speaker N` is created.

Measured: 0.03-0.07 s per segment on CPU, so the GPU stays free for the recogniser and
nothing is added to the latency budget. On the two-voice test the pattern came out
exactly right (A, B, A, B with two labels), including both returns of the first speaker.

A side benefit that removed a blocker: the embedding model is **not gated**, unlike the
3.1 and `segmentation-3.0` pipelines. No Hugging Face token and no licence click are
needed, so a fresh clone runs end to end without an account. The trade-off is no
overlap handling (two people talking over each other are one segment) and no
segmentation model for very long turns; both are outside what the brief asks for.

Alternatives considered: the full 3.1 pipeline (offline only), speechbrain ECAPA (works,
but pyannote's WeSpeaker weights are measurably better on short turns), and named
speaker recognition (explicitly out of scope in the brief).

## D7 - Evaluation set: local Piper TTS, replaced by real recordings later

The brief rewards measurement, but there were no Armenian recordings in the project.
`tools/build_eval_audio.py` synthesises five phrases with a local Piper voice so latency
and wiring are measurable from the first day. This is a **smoke/regression set, not an
accuracy benchmark**: synthetic speech is cleaner than a real call and has flat prosody.
Real recordings should replace it before the interview.
