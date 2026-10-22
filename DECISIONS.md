# DECISIONS

Short log of choices that were not obvious, with the reason they were made.
Numbers come from `tools/eval_offline.py` on the synthetic Armenian set in `eval/audio`
(5 phrases, Piper `hy_AM-gor-medium`), CUDA float16 on an RTX 4060 Laptop.

## D1 - Speech recognition: faster-whisper `large-v3`

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
