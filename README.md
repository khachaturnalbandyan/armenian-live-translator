# Live Armenian → English transcription

Listens to a live conversation, transcribes spoken Armenian locally and prints the
English translation in the terminal, labelled by speaker, while the conversation is
still running. No cloud speech or translation APIs.

```
[00:01:12] Speaker 1  HY: Բարև, ինչպե՞ս ես։  EN: Hi, how are you?
[00:01:15] Me         HY: Լավ եմ, շնորհակալություն։  EN: I'm fine, thank you.
```

**Status:** all four stages work: both audio sources at once, Armenian transcription,
English translation, and per-person speaker labels. Measured end to end at ~1 s per
phrase against a 5 s budget; see [TESTS.md](TESTS.md) for what has and has not been
checked with real speech.

## How it works

```
microphone ─┐                    ┌── Silero VAD ──> phrases ──> speaker ID ──> faster-whisper ──> NLLB ──> terminal
            ├─ 16 kHz mono ──────┤                                  (embeddings)     (large-v3)      (hy→en)
system out ─┘                    └── each source has its own VAD and capture thread
```

Each source runs in its own thread so audio keeps flowing while the recogniser works.
Segments close on a 350 ms pause rather than on a fixed window, which is what keeps the
latency budget: the clock starts when the phrase ends. The microphone is labelled `Me`;
voices on the system-audio stream are clustered online and labelled `Speaker 1..N`,
keeping the same label for the same person for the whole session.

## Setup

Requirements: Linux with PipeWire or PulseAudio (`pactl`, `parec`), Python 3.10+,
ffmpeg, and a CUDA GPU (CPU works with `--cpu`, slower).

```bash
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
```

`--system-site-packages` reuses an existing PyTorch install; without it, `pip` pulls in
its own torch wheel (a few GB). First run downloads the models: whisper `large-v3`
(~3 GB) and NLLB-200 600M (~2.4 GB). They are cached afterwards and the program works
offline.

## Running

```bash
```bash
./run.sh --list-devices          # microphones and system-audio (monitor) sources
./run.sh                         # system default microphone only
./run.sh --system-audio          # microphone + monitor of the default output
./run.sh --device <mic> --system-audio <monitor>   # explicit devices
./run.sh --input some.wav --stats                  # replay a 16 kHz mono WAV (evaluation)
./run.sh --input mic.wav --input-system call.wav   # replay both streams
```

Useful flags: `--stats` (timing per line), `--output <file>` (save transcript lines to a text file), `--speaker-threshold` (how similar two
segments must sound to be the same person, default 0.55; raise it if one person is
split into two labels, lower it if two people get merged), `--diarize` (split speakers
on the microphone stream too), `--min-silence-ms`, `--max-segment-s`, `--threshold`
(VAD), `--model`, `--cpu`, `--no-translate`.

`run.sh` only exists to put the CUDA 12 libraries that CTranslate2 needs on
`LD_LIBRARY_PATH`; plain `python main.py` works if they are already visible.

### Capturing the other side of a call

On PipeWire/PulseAudio every playback device has a `.monitor` source, so the call audio
is captured like any other input — the user still hears it normally. `--system-audio`
with no argument picks the monitor of the current default output; to choose another,
take its name from `--list-devices` and pass it as `--system-audio <name>`. No virtual
driver (BlackHole, Soundflower) is needed on Linux.

## Models and why

| Stage | Choice | Why |
| --- | --- | --- |
| ASR | faster-whisper `large-v3`, CUDA float16 | Best measured Armenian quality of the local options; 13.2% CER vs 19.5% for `large-v3-turbo`, at 0.9 s per phrase — far inside the 5 s budget |
| Translation | NLLB-200 distilled 600M, greedy | Trained on Armenian→English directly, 0.1–0.45 s per phrase |
| VAD | Silero (bundled with faster-whisper) | Reliable on short phrases, cheap on CPU |
| Speaker ID | pyannote `wespeaker-voxceleb-resnet34-LM` embeddings + online clustering | The embedding model behind the pyannote 3.1 pipeline, run per segment and clustered as the call goes on: 0.03–0.07 s per segment on CPU, no GPU contention, and it works streaming, which the offline 3.1 pipeline cannot. The embedding model is not gated, so no Hugging Face token is needed |

Details and the alternatives that were rejected are in [DECISIONS.md](DECISIONS.md).

## Known limitations

- Armenian ASR is the weak link: 13% character error rate on the synthetic eval set;
  expect proper nouns and fast speech to be worse. Real-recording numbers are pending.
- Speaker labels come from voice clustering, so two people with very similar voices can
  be merged, and a speaker who only ever says one short word starts a new label. Tune
  with `--speaker-threshold`.
- Segments from both sources are transcribed by one worker, so if both sides of the call
  speak at length at the same time the GPU queues them and latency grows past what the
  `--stats` numbers show for a single stream.
- No echo handling: if the call audio plays through speakers, the microphone will pick
  it up twice (the brief puts echo handling out of scope; use headphones).
- Whisper sometimes gets stuck repeating one word ("այդ այդ այդ ..."). Such a segment is
  decoded once more with repeats blocked (about +1 s); if it still loops it is shown as
  `[unclear]` rather than translated. Blocking repeats on every segment would avoid the
  retry but raised CER from 13.5% to 16.0%, so it is used only after a loop.
- Long monologues are hard-cut at 6 s, which can split a sentence mid-word.
- Linux/PipeWire only for live capture; macOS would need a different capture backend
  (`capture.py` is the single place to change).
- The 5 s budget assumes a CUDA GPU; on CPU `large-v3` will exceed it.

## Development

```bash
python tools/build_eval_audio.py            # synthetic Armenian eval set (needs piper-tts)
python tools/eval_offline.py --translate    # CER + latency of the real components
python tools/build_diarization_test.py      # two-voice clip for speaker identification
.venv/bin/python -m pytest tests/ -q        # clustering + scoring logic, model-free, ~1 s
```

### Comparing speech recognisers on real recordings

```bash
python tools/record_eval.py --speaker aram                 # read 20 Armenian sentences into the mic
python tools/record_eval.py --speaker ani --device <sink>.monitor --source call   # call side
python tools/compare_asr.py faster-whisper:large-v3 faster-whisper:large-v3-turbo \
    mms:facebook/mms-1b-all seamless:facebook/seamless-m4t-v2-large \
    --show --report eval/results.md
```

`record_eval.py` saves 16 kHz WAVs to `eval/real/` (git-ignored) and the correct text
to `eval/real/manifest.json`. `compare_asr.py` loads one model at a time and reports
CER, WER and recognition time, broken down by speaker and by source (mic vs call);
`--segment` cuts audio with the live segmenter first, `--manifest eval/manifest.json`
uses the synthetic set. Backends: `faster-whisper:<name>`, `hf-whisper:<repo>` (any
Whisper fine-tune), `mms:<repo>`, `seamless:<repo>` (see `tools/asr_backends.py`).
CER ignores punctuation and case, and treats `և` and `եւ` as the same.
