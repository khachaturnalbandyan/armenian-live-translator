# ASR comparison, synthetic set (2026-10-30)

Piper `hy_AM-gor-medium`, one voice, RTX 4060 Laptop, float16. Not real speech: confirm with `eval/real/` recordings.

## Normal speech, one phrase per file

```bash
python tools/compare_asr.py <backends> --manifest eval/manifest.json --show
```

5 recordings, 17 s of audio, from eval/manifest.json (whole recordings)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 4.9% | 21.1% | 0.05s | 0.07s | 0.07s | 0.02 | 302s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.0% | 24.0% | 0.33s | 0.34s | 0.34s | 0.09 | 282s |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 6.0% | 24.0% | 0.43s | 0.47s | 0.47s | 0.11 | 165s |
| `mms:facebook/mms-1b-all` | 6.9% | 45.2% | 0.07s | 0.09s | 0.09s | 0.02 | 14s |
| `faster-whisper:large-v3` | 13.5% | 45.4% | 0.82s | 0.92s | 0.92s | 0.22 | 4s |

CER by speaker:

| backend | piper-gor |
| --- | --- |
| `faster-whisper:large-v3` | 13.5% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.0% |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 6.0% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 4.9% |
| `mms:facebook/mms-1b-all` | 6.9% |

CER by source:

| backend | piper hy_AM-gor-medium |
| --- | --- |
| `faster-whisper:large-v3` | 13.5% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.0% |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 6.0% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 4.9% |
| `mms:facebook/mms-1b-all` | 6.9% |

**tts_01.wav** — ref: Բարև, ինչպես ես։
- `faster-whisper:large-v3` (23%): Պարև ինչպստ ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): - Բարև ինչպես տես…
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (8%): - Բարև ինչպես տես…
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (8%): բարև ինչպես դես
- `mms:facebook/mms-1b-all` (15%): պարեւ ինչպես տես

**tts_02.wav** — ref: Լավ եմ, շնորհիվ աստծո։
- `faster-whisper:large-v3` (18%): լավ եմ շնորի վասսո։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (12%): Լավ եմ, շնորհիվ ասո.
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (12%): Լավ եմ, շնորհիվ ասո.
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (12%): լավ եմ շնորհիվ ասո
- `mms:facebook/mms-1b-all` (12%): լավ եմ շնորհի վասո

**tts_03.wav** — ref: Այսօր եղանակը շատ լավ է, արի գնանք զբոսնելու։
- `faster-whisper:large-v3` (8%): Հեսոր եղանակը շատ լավ է արիգնանք զբոսնելու։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Այսօր եղանակը շատ լավ է արիգնանք զբոսնելու։
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (0%): Այսօր եղանակը շատ լավ է արիգնանք զբոսնելու։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): այսօր եղանակը շատ լավ է արիգնանք զբոսնելու
- `mms:facebook/mms-1b-all` (0%): այսօր եղանակը շատ լավ է արիգնանք զբոսնելու

**tts_04.wav** — ref: Ժողովը սկսվում է ժամը երեքին, մի ուշացիր։
- `faster-whisper:large-v3` (6%): ժողովը սկսվում է ժամայերեքին մի ուշացիր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Ժողովը սկսվում է ժամը երեքին ի ուշացիր։
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (3%): Ժողովը սկսվում է ժամը երեքին ի ուշացիր։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ժողովը սկսվում է ժամը երեքին մի ուշացիր
- `mms:facebook/mms-1b-all` (0%): ժողովը սկսվում է ժամը երեքին միուշացիր

**tts_05.wav** — ref: Ես կարծում եմ, որ այս լուծումը ավելի արագ կաշխատի։
- `faster-whisper:large-v3` (12%): ես կարծում եմ, որ այսի լուծում ավերի առակ կաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Ես կարծում եմ, որ այս լծումը ավերի արագ կաշխատի։
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (8%): Ես կարծում եմ, որ այս լծումը ավերի արագ կաշխատի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (5%): ես կարծում եմ որ այս լուցումը ավելրի արագ կաշխատի
- `mms:facebook/mms-1b-all` (8%): ես կարծում եմ որ այսիլուծումը ավերի արակկաշխատի


Failed backends:

- `hf-whisper:arampacha/whisper-large-hy-2` failed: ValueError: The generation config is outdated and is thus not compatible with the `language` argument to `generate`. Please update the generation config as per the instructions https://github.com/huggingface/transformers/issues/25084#issuecomment-1664398224

## Fast speech: the 5 phrases joined without pauses, sped up 1.0x / 1.3x / 1.6x (ffmpeg atempo), cut by the live Segmenter

3 recordings, 40 s of audio, from the joined set (cut by the live Segmenter)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 7.0% | 20.4% | 1.91s | 1.91s | 1.91s | 0.14 | 9s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 7.2% | 21.5% | 1.58s | 1.59s | 1.59s | 0.12 | 2s |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 9.1% | 37.6% | 0.20s | 0.25s | 0.25s | 0.02 | 6s |
| `mms:facebook/mms-1b-all` | 9.1% | 46.2% | 0.28s | 0.33s | 0.33s | 0.02 | 8s |
| `faster-whisper:large-v3` | 15.1% | 48.4% | 3.55s | 3.76s | 3.76s | 0.27 | 3s |

CER by speaker:

| backend | piper-1.0x | piper-1.3x | piper-1.6x |
| --- | --- | --- | --- |
| `faster-whisper:large-v3` | 10.8% | 15.8% | 18.7% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 5.8% | 7.9% | 7.9% |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 5.0% | 7.9% | 7.9% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 3.6% | 6.5% | 17.3% |
| `mms:facebook/mms-1b-all` | 7.9% | 9.4% | 10.1% |

CER by source:

| backend | piper joined |
| --- | --- |
| `faster-whisper:large-v3` | 15.1% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 7.2% |
| `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` | 7.0% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 9.1% |
| `mms:facebook/mms-1b-all` | 9.1% |

**joined_1.0.wav** — ref: Բարև, ինչպես ես։ Լավ եմ, շնորհիվ աստծո։ Այսօր եղանակը շատ լավ է, արի գնանք զբոսնելու։ Ժողովը սկսվում է ժամը երեքին, մի ուշացիր։ Ես կարծում եմ, որ այս լուծումը ավելի արագ կաշխատի։
- `faster-whisper:large-v3` (11%): Վարև ինչպես տես։ լավ եմ շնորի վասսո։ Հայցոր եղանակը շատ լավ է արիգնանք զբոսնելու։ ժողովը սկսվում է ժամայերեքին մի ուշացիր։ ես կարծում եմ, որ այսի լուծում ավերի առակ կաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (6%): Բարև ինչպես տես… - Լավ եմ, շնորհիվ ասո… Այսօր եղանակը շատ լավ է, արիգնանք զբոսնելու… Ժողովը սկսվում է ժամը երեքի մի ուշացիր։ Ես կարծում եմ, որ այս լծումը հավերի արագ կաշխատի…
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (5%): - Բարև ինչպես տես… - Լավ եմ, շնորհիվ ասո… Այսօր եղանակը շատ լավ է, արիգնանք զբոսնելու։ Ժողովը սկսվում է ժամը երեքին մի ուշացիր։ Ես կարծում եմ, որ այս լծումը հավերի արագ կաշխատի…
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (4%): բարև ինչպես դես լավ եմ շնորհիվ ասո այսօր եղանակը շատ լավ է արգնանք զբոսնելու ժողովն սկսվում է ժամը երեքին միուշացիր ես կարծում եմ որ այս լուծումը ավելի արագ կաշխատի
- `mms:facebook/mms-1b-all` (8%): պարեւ ինչպէս տես լավ եմ շնորհի վասո այսօր եղանակը շատ լավ է արիգնանգ զբոսնելոււ ժողովը սկսվում է ժամը երեքին իուշացիր ես կարծում եմ որ այսիլուծումը ավերի արակկաշխատի

**joined_1.3.wav** — ref: Բարև, ինչպես ես։ Լավ եմ, շնորհիվ աստծո։ Այսօր եղանակը շատ լավ է, արի գնանք զբոսնելու։ Ժողովը սկսվում է ժամը երեքին, մի ուշացիր։ Ես կարծում եմ, որ այս լուծումը ավելի արագ կաշխատի։
- `faster-whisper:large-v3` (16%): Վարև ինչպես ես։ լավանդ շնորի վասո։ Հեսոր եղանակը շատ լավ է արգնանք զբոսնելու։ ժողովը սկսվում է ժամայերեկին իվ շացիր։ ես կարծում եմ, որ այսի լուծում ավերի առակ կաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): - բարև ինչպես տես… Լավ եմ, շնորհիվ ասով. Այսօր եղանակը շատ լավ է, այդ գնանք զբոսնելու… Ժողովը սկսվում է ժամը երեքին ի ուշացիր։ Ես կարծում եմ, որ այս լծում ավերի արագ կաշխատի…
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (8%): - Բարև ինչպես տես… Լավ եմ, շնորհիվ ասով. Այսօր եղանակը շատ լավ է, այդ գնանք զբոսնելու։ Ժողովը սկսվում է ժամը երեքին ի ուշացիր։ Ես կարծում եմ, որ այս լծում ավերի արագ կաշխատի…
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (6%): բարև ինչպես ես լավ եմ շնորհիվ ասո այսօր եղանակը շատ լավ է այգնանք զբոսնելու ժողովն սկսվում է ժամը երեքին նիուշացիր ես կարծում եմ որ յս լծումը ավելի արագ կաշխատի
- `mms:facebook/mms-1b-all` (9%): վարեև ինչպես եզ լավ եմ շնորի վասը այսօր եղանակը շատ լավ է արգնանք զբոսնելու ժողովը սկսվում է ժամը երեքին իուշացիր ես կարծում եմ որ այսոծում ավերի արագկաշխատի

**joined_1.6.wav** — ref: Բարև, ինչպես ես։ Լավ եմ, շնորհիվ աստծո։ Այսօր եղանակը շատ լավ է, արի գնանք զբոսնելու։ Ժողովը սկսվում է ժամը երեքին, մի ուշացիր։ Ես կարծում եմ, որ այս լուծումը ավելի արագ կաշխատի։
- `faster-whisper:large-v3` (19%): Վարև ինչպես ես։ լավ եմ չնորի վասո։ Հեսոր եղանակը շատ լավ է այդ ինանք զբոսնելու։ ժողը սկսվում է ժամայերիքին լիվ շացիր։ ես կարծում եմ, որ էս լուծում ավեր առակաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Բարև ինչպես տես… - Լավ եմ, շնորհիվ ասո… Այսօր եղանակը շատ լավ է, այդ նանք զբոսնելու… Ժողովը սկսվում է ժամը երեքին ի ուշացիր։ Ես կարծում եմ, որ այս լծում ավելի արագ աշխատի…
- `hf-whisper:Chillarmo/whisper-large-v3-turbo-armenian` (8%): - Բարև ինչպես տես… Լավ եմ, շնորհիվ ասո. Այսօր եղանակը շատ լավ է, այդ նանք զբոսնելու… Ժողովը սկսվում է ժամը երեքին ի ուշացիր։ Ես կարծում եմ, որ այս լծում ավելի արագ աշխատի.
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (17%): բարև ինչպես ես լավ եմ շնորի ասո այսօր եղնակ շատլւ է արյգոնաք զբոներու ժողով սկսվումէ ժամը երեքին նիուշացիր ես կարծւմ եմոր ե լուծու ավեր արագ աշխատի
- `mms:facebook/mms-1b-all` (10%): բարև ինչբա տեզ լավեմ շնորի վասո այսօր եղանակը շատ լավ է այրգնանք զբոսնելու ժողովը սկսվում է ժամը երեքին նիուշացիր ես կարծում եմ որ այսլուծում ավերի արակաշխաբի


Failed backends:

- `hf-whisper:arampacha/whisper-large-hy-2` failed: ValueError: The generation config is outdated and is thus not compatible with the `language` argument to `generate`. Please update the generation config as per the instructions https://github.com/huggingface/transformers/issues/25084#issuecomment-1664398224
