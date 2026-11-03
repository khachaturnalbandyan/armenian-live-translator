# ASR comparison, real recordings (2026-10-30)

20 sentences from tools/record_eval.py, one speaker (xachatur), laptop digital microphone, normal speed.

## Whole recordings

20 recordings, 75 s of audio, from eval/real/manifest.json (whole recordings)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 0.7% | 11.5% | 0.44s | 0.52s | 0.52s | 0.12 | 11s |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 2.4% | 20.2% | 0.08s | 0.18s | 0.18s | 0.02 | 8s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 2.6% | 17.0% | 0.36s | 0.44s | 0.44s | 0.10 | 2s |
| `mms:facebook/mms-1b-all` | 8.3% | 39.8% | 0.09s | 0.15s | 0.15s | 0.03 | 8s |
| `faster-whisper:large-v3` | 13.1% | 41.2% | 0.77s | 1.21s | 1.21s | 0.21 | 2s |

CER by speaker:

| backend | xachatur |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 2.6% |
| `faster-whisper:large-v3` | 13.1% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 2.4% |
| `mms:facebook/mms-1b-all` | 8.3% |
| `seamless:facebook/seamless-m4t-v2-large` | 0.7% |

CER by source:

| backend | mic |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 2.6% |
| `faster-whisper:large-v3` | 13.1% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 2.4% |
| `mms:facebook/mms-1b-all` | 8.3% |
| `seamless:facebook/seamless-m4t-v2-large` | 0.7% |

**xachatur_mic_001.wav** — ref: Բարև, ինչպե՞ս ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Բարև, ինչպես ես
- `faster-whisper:large-v3` (8%): Վարև ինչպես ես։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): բարև ինչպես ես
- `mms:facebook/mms-1b-all` (8%): բարև ինչպես եզ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Բարեւ, ինչպես ես։

**xachatur_mic_002.wav** — ref: Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Ես լավ եմ շնորհագալություն, իսկ դու
- `faster-whisper:large-v3` (7%): ես լավ եմ շնորակ ալություննիսկ դու։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ես լավ եմ շնորհակալություն իսկ դու
- `mms:facebook/mms-1b-all` (7%): ես լավ եմ շնորա կարությունիսկ դու
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես լավ եմ, շնորհակալություն, իսկ դու։

**xachatur_mic_003.wav** — ref: Վաղը ժամը տասին հանդիպում ունենք։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (11%): Վաղը ժամը քանիսին հանդիպում ունենք։
- `faster-whisper:large-v3` (14%): Վառը ժամը քանիսին հանդիպում ունենք։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (11%): վաղը ժամը քանիսին հանդիպում ունենք
- `mms:facebook/mms-1b-all` (14%): վաղէժամը քանիսին հանդիպում ունենք
- `seamless:facebook/seamless-m4t-v2-large` (11%): Վաղը ժամը քանի՞սին հանդիպում ունենք։

**xachatur_mic_004.wav** — ref: Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Կարող ես կրկնել, լավ չլսեցի.
- `faster-whisper:large-v3` (14%): Քարող ես կրկնել, լավ չէ լսեցիմ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): կարող ես կրկնել լավ չլսեցի
- `mms:facebook/mms-1b-all` (0%): կարող ես կրկնել լավ չլսեցի
- `seamless:facebook/seamless-m4t-v2-large` (0%): Կարող ես կրկնել, լավ չլսեցի։

**xachatur_mic_005.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:large-v3` (25%): Հայց շապատ շատ աշխատանք ունում։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): այս շաբաթ շատ աշխատանք ունեմ
- `mms:facebook/mms-1b-all` (0%): այս շաբաթ շատ աշխատանք ունեմ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այս շաբաթ շատ աշխատանք ունեմ։

**xachatur_mic_006.wav** — ref: Երևանում այսօր շատ շոգ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Երևանում այսօր շատ շոգ է։
- `faster-whisper:large-v3` (14%): Յերևանում այսոր շատ շոք է։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): երևանում այսօր շատ շոգ է
- `mms:facebook/mms-1b-all` (5%): երևանում այսօր շատ շոք է
- `seamless:facebook/seamless-m4t-v2-large` (0%): Երեւանում այսօր շատ շոգ է։

**xachatur_mic_007.wav** — ref: Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `faster-whisper:large-v3` (8%): Մենք պետք է ավարտենք նախագիցը մինչև ուրպատ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ
- `mms:facebook/mms-1b-all` (3%): մենք պետք է ավարտենք նախագիցը մինչև ուրբաթ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ։

**xachatur_mic_008.wav** — ref: Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:large-v3` (14%): Ով է պատասանդում այս հարցի համար։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ով է պատասխանատու այս հարցի համար
- `mms:facebook/mms-1b-all` (14%): ովե պատասխանատուվ այ սարձի համար
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ով է պատասխանատու այս հարցի համար։

**xachatur_mic_009.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ես համաձայն չեմ, կարծում եմ կա ավելի լավ տարբերակ։
- `faster-whisper:large-v3` (10%): ես համաձենչ եմ, կարծում եմ կա ավելի լավ տարբեր եկա։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (2%): ես համաձայն չեմ կարծում եմ կա ավելլավ տարբերակ
- `mms:facebook/mms-1b-all` (12%): ես համաձային չեմ գարծում եմ կա վելյավ տարբերակ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես համաձայն չեմ, կարծում եմ կա ավելի լավ տարբերակ։

**xachatur_mic_010.wav** — ref: Զանգիր ինձ, երբ տուն հասնես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Զանգիր ինձ երբ տուն հասնես
- `faster-whisper:large-v3` (0%): զանգիր ինձ երբ տուն հասնես։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (5%): զանգիրն ինձ երբ տուն հասնես
- `mms:facebook/mms-1b-all` (0%): զանգիրինձ երբ տուն հասնես
- `seamless:facebook/seamless-m4t-v2-large` (0%): Զանգիր ինձ, երբ տուն հասնես։

**xachatur_mic_011.wav** — ref: Գինը հազար հինգ հարյուր դրամ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (12%): Կինը հազար հին քարյուր դրամ է։
- `faster-whisper:large-v3` (84%): 9500 դրամը
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (4%): կինը հազար հինգ հարյուր դրամ է
- `mms:facebook/mms-1b-all` (56%): կինը 1ազր 500 դրամ է
- `seamless:facebook/seamless-m4t-v2-large` (0%): Գինը հազար հինգ հարյուր դրամ է։

**xachatur_mic_012.wav** — ref: Արամը և Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Արամը և անին երեք գնացին գյումրի։
- `faster-whisper:large-v3` (4%): առամը և անին երեկ գնացին գյումրի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (7%): առամը և անին երեք գնացին գյումրի
- `mms:facebook/mms-1b-all` (4%): արամը և անին երեք գնացին գյումրի
- `seamless:facebook/seamless-m4t-v2-large` (4%): Արամը եւ Անիը երեկ գնացին Գյումրի։

**xachatur_mic_013.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:large-v3` (0%): ինտերնետը նորից դանդաղ է աշխատում։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ինտերնետը նորից դանդաղ է աշխատում
- `mms:facebook/mms-1b-all` (0%): ինտերնետը նորից դանդաղ է աշխատում
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում։

**xachatur_mic_014.wav** — ref: Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը
- `faster-whisper:large-v3` (7%): Հնդրում եմ ուղարկիր ինձ այդ վայլը։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): խնդրում եմ ուղարկիր ինձ այդ ֆայլը
- `mms:facebook/mms-1b-all` (11%): խնդրում եմ ուղղարկիր ինձայթ վայլը
- `seamless:facebook/seamless-m4t-v2-large` (0%): Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։

**xachatur_mic_015.wav** — ref: Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Մենք օգտագործում ենք արհեստակաբանականություն թարգմանության համար։
- `faster-whisper:large-v3` (7%): Մենք ոգտագործում ենք արեստակը բանականություն թարգմանության համար։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (2%): մենք օգտագործում ենք արհեստակա բանականություն թարգմանության համար
- `mms:facebook/mms-1b-all` (3%): մենք օգտագործում ենք արեստակա բանականություն թարգմանության համար
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։

**xachatur_mic_016.wav** — ref: Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ներողություն, ուշացա, խցանում էր.
- `faster-whisper:large-v3` (4%): Ներողություն ուշացա խթանում էր։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (4%): ներողություն ուշացավ խցանում էր
- `mms:facebook/mms-1b-all` (4%): ներողություն ուշացահ խցանում էր
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ներողություն, ուշացա, խցանում էր։

**xachatur_mic_017.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ի՞նչ ես կարծում, սա կաշխատի՞
- `faster-whisper:large-v3` (0%): ինչ ես կարծում սա կաշխատի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ինչ ես կարծում սակ աշխատի
- `mms:facebook/mms-1b-all` (5%): ինչ էս կարծում սակ աշխատի
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինչ ես կարծում, սա կաշխատի։

**xachatur_mic_018.wav** — ref: Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (6%): Հաջորդ ամիս պատրաստվում է մեկնել Թբիլիսի։
- `faster-whisper:large-v3` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել թբիլիսի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (6%): հաջորդ ամիս պատրաստվում է մեկնել թբիլիսի
- `mms:facebook/mms-1b-all` (3%): հաջորդ ամիս պատրաստվում ե մեկնել թբիլիսի
- `seamless:facebook/seamless-m4t-v2-large` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։

**xachatur_mic_019.wav** — ref: Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Այո, ամենինչ պարզ է, շնորհկել եմ
- `faster-whisper:large-v3` (19%): Հայո, ամենիշ պարզ է, շնորը կալեմ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (8%): այո ամեն ինչ պարզ է շնորհը կելեմ
- `mms:facebook/mms-1b-all` (15%): այո ամենինչ պարզ է շնորըկալիւմ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այո, ամեն ինչ պարզ է, շնորհակալ եմ։

**xachatur_mic_020.wav** — ref: Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (6%): Լավ, ուրեմն մինչև վաղ եմ, հաջողություն
- `faster-whisper:large-v3` (23%): լավ, ուրեմը մինչև վաղը, աջողջում։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): լավ ուրեմն մինչև վաղը հաջողություն
- `mms:facebook/mms-1b-all` (3%): լավ ուրեմը մինչև վաղը հաջողություն
- `seamless:facebook/seamless-m4t-v2-large` (0%): Լավ, ուրեմն մինչեւ վաղը, հաջողություն։


## Cut by the live Segmenter

20 recordings, 75 s of audio, from eval/real/manifest.json (cut by the live Segmenter)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 3.5% | 23.2% | 0.39s | 0.46s | 0.46s | 0.10 | 2s |
| `faster-whisper:large-v3` | 11.7% | 38.9% | 0.79s | 1.24s | 1.24s | 0.22 | 3s |

CER by speaker:

| backend | xachatur |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 3.5% |
| `faster-whisper:large-v3` | 11.7% |

CER by source:

| backend | mic |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 3.5% |
| `faster-whisper:large-v3` | 11.7% |

**xachatur_mic_001.wav** — ref: Բարև, ինչպե՞ս ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Բարև, ինչպես ես
- `faster-whisper:large-v3` (0%): բարև ինչպես ես։

**xachatur_mic_002.wav** — ref: Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ես լավ եմ շնորհակալություն, իսկ դու
- `faster-whisper:large-v3` (3%): ես լավ եմ շնորակ ալություն իսկ դու։

**xachatur_mic_003.wav** — ref: Վաղը ժամը տասին հանդիպում ունենք։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (11%): Վաղը ժամը քանիսին հանդիպում ունենք։
- `faster-whisper:large-v3` (7%): Վաղը ժամը քանսին հանդիպում ունենք։

**xachatur_mic_004.wav** — ref: Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): կարող ես կրկնել, լավ չլսեցի
- `faster-whisper:large-v3` (14%): Քարող ես կրկնել, լավ չէ լսեցիմ։

**xachatur_mic_005.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Այս շաբաթ շատ աշխատանք ունում։
- `faster-whisper:large-v3` (25%): Հայց շապատ շատ աշխատանք ունում։

**xachatur_mic_006.wav** — ref: Երևանում այսօր շատ շոգ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Երևանում այսօր շատ շոգ է։
- `faster-whisper:large-v3` (10%): Յերևանում այսօր շատ շոք է։

**xachatur_mic_007.wav** — ref: Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Մենք պետք է ավարտենք նախագիտը մինչև ուրբաթ։
- `faster-whisper:large-v3` (8%): Մենք պետք է ավարտենք նախագիցը մինչև ուրպատ։

**xachatur_mic_008.wav** — ref: Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Ո՞վ է պատասհանատու այս հարցի համար։
- `faster-whisper:large-v3` (14%): ով է պատասհանդում այս հարցի համար։

**xachatur_mic_009.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Ես համաձայն չեմ, կարծում եմ կա ավելիավ տարբերակ։
- `faster-whisper:large-v3` (10%): ես համաձենչ եմ, կարծում եմ, կա ավելի լավ տարբեր եկա։

**xachatur_mic_010.wav** — ref: Զանգիր ինձ, երբ տուն հասնես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Զանգիր ինձ, երբ տուն հասնես
- `faster-whisper:large-v3` (0%): զանգիր ինձ երբ տուն հասնես։

**xachatur_mic_011.wav** — ref: Գինը հազար հինգ հարյուր դրամ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (12%): Կինը հազար հին քարյուր դրամ է։
- `faster-whisper:large-v3` (72%): Վինը 1500 դրամը։

**xachatur_mic_012.wav** — ref: Արամը և Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Արամը և անին երեք գնացին գյումրի։
- `faster-whisper:large-v3` (4%): առամը և անին երեկ գնացին գյումրի։

**xachatur_mic_013.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:large-v3` (3%): ինտերնետը նորից դանդաղ է հաշխատում։

**xachatur_mic_014.wav** — ref: Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը
- `faster-whisper:large-v3` (7%): Հնդրում եմ ուղարկիր ինձ այդ վայլը։

**xachatur_mic_015.wav** — ref: Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Մենք օգտագործում ենք արհեստակաբանականություն թարգմանության համար։
- `faster-whisper:large-v3` (7%): Մենք ոգտագործում ենք արեստակը բանականություն թարգմանության համար։

**xachatur_mic_016.wav** — ref: Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ներողություն, ուշացա, խցանում էր.
- `faster-whisper:large-v3` (4%): Ներողություն, ուշացա, խթանում էր։

**xachatur_mic_017.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Ի՞նչ ես կարծում, սա կա աշխատի՞
- `faster-whisper:large-v3` (0%): ինչ ես կարծում սա կաշխատի։

**xachatur_mic_018.wav** — ref: Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Հաջորդ ամիս պատրաստվում է մեկն էլ թբիլիսի։
- `faster-whisper:large-v3` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել թբիլիսի։

**xachatur_mic_019.wav** — ref: Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Այո՛, ամենինչ պարզ է, շնորհկել եմ
- `faster-whisper:large-v3` (23%): Հայո, ամենիշ պարզ է, շնորը կալմ։

**xachatur_mic_020.wav** — ref: Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Լավ, ուրեմն մինչև վաղ է, հաջողություն
- `faster-whisper:large-v3` (23%): լավ, ուրեմը մինչև վաղը, աջողջում։


## Fast speech, 20 recordings (speaker xachatur-fast)

20 recordings, 57 s of audio, from eval/real/manifest.json, xachatur-fast only (whole recordings)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 2.5% | 13.1% | 0.43s | 0.50s | 0.50s | 0.15 | 13s |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 6.0% | 29.9% | 0.07s | 0.18s | 0.18s | 0.03 | 6s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 8.2% | 30.8% | 0.36s | 0.44s | 0.44s | 0.13 | 2s |
| `faster-whisper:large-v3` | 13.2% | 49.4% | 0.81s | 1.30s | 1.30s | 0.29 | 4s |

CER by speaker:

| backend | xachatur-fast |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 8.2% |
| `seamless:facebook/seamless-m4t-v2-large` | 2.5% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 6.0% |
| `faster-whisper:large-v3` | 13.2% |

CER by source:

| backend | mic |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 8.2% |
| `seamless:facebook/seamless-m4t-v2-large` | 2.5% |
| `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` | 6.0% |
| `faster-whisper:large-v3` | 13.2% |

**xachatur-fast_mic_021.wav** — ref: Բարև, ինչպե՞ս ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Բարև, ինչպես ես
- `seamless:facebook/seamless-m4t-v2-large` (0%): Բարեւ, ինչպես ես։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): բարև ինչպես ես
- `faster-whisper:large-v3` (8%): Վարև ինչպես ես։

**xachatur-fast_mic_022.wav** — ref: Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Ես լավ եմ շնորհակալություն, իսկ դո
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես լավ եմ, շնորհակալություն, իսկ դու։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (3%): ես լավ եմ շնորհակալությունը իսկ դու
- `faster-whisper:large-v3` (24%): ես լավեմ շնորը կալություննեց գդում։

**xachatur-fast_mic_023.wav** — ref: Վաղը ժամը տասին հանդիպում ունենք։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Վաղի ժամը տասին հանդիպում ունենք։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Վաղը ժամը տասին հանդիպում ունենք։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): վաղը ժամը տասին հանդիպում ունենք
- `faster-whisper:large-v3` (14%): վարհը ժամը տասին հանդի պմունենք։

**xachatur-fast_mic_024.wav** — ref: Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (14%): կարո՞ղ ես գրգնել, լավ չլսեցիմ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Կարող ես կրկնել, լավ չլսեցի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): կարող ես կրկնել լավ չլսեցի
- `faster-whisper:large-v3` (18%): կարող ես գրգնել, լավ չի լսեցիմ։

**xachatur-fast_mic_025.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Այս շաբաթ շատ աշխատանք ունում։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այս շաբաթ շատ աշխատանք ունեմ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): այս շաբաթ շատ աշխատանք ունեմ
- `faster-whisper:large-v3` (25%): այս շապատ շատ աշրատ անքում նում։

**xachatur-fast_mic_026.wav** — ref: Երևանում այսօր շատ շոգ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Երևանում այսօր շատ շոգ է։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Երեւանում այսօր շատ շոգ է։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): երևանում այսօր շատ շոգ է
- `faster-whisper:large-v3` (14%): երևանում այսօր շատ շոք եմ։

**xachatur-fast_mic_027.wav** — ref: Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (5%): մենք պետք է աւարտենք նախագիծը մինչևւուրբաթ
- `faster-whisper:large-v3` (14%): Մենք պետք է ավարտենք նախագիծը մինշավուր պատ։

**xachatur-fast_mic_028.wav** — ref: Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (11%): Ո՞վ է պատասխան դու այս հարթի համար
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ով է պատասխանատու այս հարցի համար։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ով է պատասխանատու այս հարցի համար
- `faster-whisper:large-v3` (14%): Ով է պատսխանատու այս հարցի անվար։

**xachatur-fast_mic_029.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (12%): Ես համաձայն չեմ, կարծում եմ ավել լավ տարբերակ կա։
- `seamless:facebook/seamless-m4t-v2-large` (10%): Ես համաձայն չեմ, կարծում եմ ավելի լավ տարբերակ կա։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (15%): ես համաձայն չեմ կարծում եմ ավեյլ լավ տարբերակ կա
- `faster-whisper:large-v3` (18%): ես համաձենչ եմ, կարծում եմ ավել լավ տարբերակ կա։

**xachatur-fast_mic_030.wav** — ref: Զանգիր ինձ, երբ տուն հասնես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Զագիր ինձ, երբ տուն հասնես
- `seamless:facebook/seamless-m4t-v2-large` (0%): Զանգիր ինձ, երբ տուն հասնես։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (5%): զանգին ինձ երբ տուն հասնես
- `faster-whisper:large-v3` (0%): զանգիր ինձ երբ տուն հասնես։

**xachatur-fast_mic_031.wav** — ref: Գինը հազար հինգ հարյուր դրամ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (52%): Կինը հինգ հազար հարև դրամ։
- `seamless:facebook/seamless-m4t-v2-large` (36%): Գինը հինգ հազար հարյուր դրամ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (48%): կինըէ հինգ հազար հարյուրդ դրամ
- `faster-whisper:large-v3` (48%): Քինը հինքազար հորդրամ։

**xachatur-fast_mic_032.wav** — ref: Արամը և Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Արամը և անին երեք գնացին գյումրի։
- `seamless:facebook/seamless-m4t-v2-large` (4%): Արամը եւ Աննին երեկ գնացին Գյումրի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (7%): առամը և անին երեք գնացին գյումրի
- `faster-whisper:large-v3` (11%): Հառամը եվանին երեկ գնացին գյումրի։

**xachatur-fast_mic_033.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ինտերնետը նորից դանդաղ է աշխատում
- `faster-whisper:large-v3` (3%): ինտերնետը նորից դանտաղ է աշխատում։

**xachatur-fast_mic_034.wav** — ref: Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (7%): Խնդրում եմ ուղղարկիր ինձ այդ վայլը։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Խնդրում եմ ուղարկիր ինձ այդ ֆայլը։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): խնդրում եմ ուղարկիր ինձ այդ ֆայլը
- `faster-whisper:large-v3` (7%): խնդրում եմ ուղարգիր ինձ այդ վայլը։

**xachatur-fast_mic_035.wav** — ref: Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար
- `faster-whisper:large-v3` (2%): Մենք օգտագործում ենք արեստական բանականություն թարգմանության համար։

**xachatur-fast_mic_036.wav** — ref: Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Հերողություն, ուշացա, խցանում էր.
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ներողություն, ուշացա, խցանում էր։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (4%): ներողություն ուշացավ խցանում էր
- `faster-whisper:large-v3` (4%): Ներողություն, ուշացա, խթանում էր։

**xachatur-fast_mic_037.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Ի՞նչ ես կարծում, սակ աշխատի՞ն
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինչ ես կարծում, սա կաշխատի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (0%): ինչ ես կարծում սակ աշխատի
- `faster-whisper:large-v3` (5%): ինչ ես կարծում սակաշխատին։

**xachatur-fast_mic_038.wav** — ref: Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (6%): Հաջորդ ամիս պատրաստվում են մեկն էլ թբիլիսի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (8%): հաջորդ ամիս պատրաստվում է մեկն էլ թբիլիսի
- `faster-whisper:large-v3` (3%): Հաջորդ ամիս պատրաստվում եմ մեկնել թբիլիցի։

**xachatur-fast_mic_039.wav** — ref: Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (15%): Այո, ամեն ինչ պարձը, շնորհը գալ եմ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (12%): այո ամեն ինչ պարզ է շնորակալը
- `faster-whisper:large-v3` (19%): այու ամեն ինչ պարձ է, շնորը կալմ։

**xachatur-fast_mic_040.wav** — ref: Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (16%): Լավ, ուրեմու մինչ վաղ է, հաջողություն
- `seamless:facebook/seamless-m4t-v2-large` (0%): Լավ, ուրեմն մինչեւ վաղը, հաջողություն։
- `ctc:ErikMkrtchyan/w2v-bert-2.0-armenian-CV20.0` (13%): լավ ուրեմն մինչ վաղ եմ հաջողություն
- `faster-whisper:large-v3` (13%): լավ, ուրեմում ինչ վաղը, հաջողություն։


## Long continuous speech: recordings joined in fours, silence trimmed (10-16 s)

10 recordings, 130 s of audio, from the joined set (whole recordings)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 1.5% | 11.6% | 0.95s | 1.07s | 1.07s | 0.07 | 14s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 4.5% | 22.6% | 0.64s | 0.73s | 0.73s | 0.05 | 2s |

CER by speaker:

| backend | xachatur | xachatur-fast |
| --- | --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 2.4% | 6.5% |
| `seamless:facebook/seamless-m4t-v2-large` | 0.7% | 2.3% |

CER by source:

| backend | joined |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 4.5% |
| `seamless:facebook/seamless-m4t-v2-large` | 1.5% |

**xachatur_1.wav** — ref: Բարև, ինչպե՞ս ես։ Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։ Վաղը ժամը տասին հանդիպում ունենք։ Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Բարև, ինչպես ես, ես լավ եմ շնորհակալություն, իսկ դու վաղը ժամը քանիսին հանդիպում ունենք, կարող ես կրկնել, լավ չլսեցի
- `seamless:facebook/seamless-m4t-v2-large` (3%): Բարեւ, ինչպես ես, ես լավ եմ, շնորհակալություն, իսկ դու, վաղը ժամը քանի՞սին հանդիպում ունենք, կարող ես կրկնել, լավ չլսեցի։

**xachatur_2.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։ Երևանում այսօր շատ շոգ է։ Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։ Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Այս շաբաթ շատ աշխատանք ունեմ, երևանում այսօր շատ շոգ է, մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ, ո՞վ է պատասխանատու այս հարցի համար
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այս շաբաթ շատ աշխատանք ունեմ, Երեւանում այսօր շատ շոգ է, մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ, ով է պատասխանատու այս հարցի համար։

**xachatur_3.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։ Զանգիր ինձ, երբ տուն հասնես։ Գինը հազար հինգ հարյուր դրամ է։ Արամը և Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Ես համաձայն չեմ, կարծում եմ կա ավելիավ տարբերակ, զանգին ինձ երբ տուն հասնես, գինը հազար հին քարյուր դրամ է, արամը և անին երեք գնացին գյումրի
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես համաձայն չեմ, կարծում եմ կա ավելի լավ տարբերակ, զանգիր ինձ, երբ տուն հասնես, գինը հազար հինգ հարյուր դրամ է, Արամը եւ Անին երեկ գնացին Գյումրի։

**xachatur_4.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։ Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։ Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։ Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (1%): Ինտերնետը նորից դանդաղ է աշխատում, խնդրում եմ, ուղարկիր ինձ այդ ֆայլը, մենք օգտագործում ենք արհեստակաբանականություն, թարգմանության համար, ներողություն, ուշացա, խցանում էր.
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում, խնդրում եմ ուղարկիր ինձ այդ ֆայլը, մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար, ներողություն, ուշացա, խցանում էր։

**xachatur_5.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։ Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։ Այո, ամեն ինչ պարզ է, շնորհակալ եմ։ Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Ի՞նչ ես կարծում, սաք աշխատի՞,- հաջորդ ամիս պատրաստվում եմ մեկնել թբիլիսի,- այո, ամենինչ պարզ է, շնորհկել եմ,- լավ, ուրեմը մինչև վաղը,- հաջողություն.
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինչ ես կարծում, սա կաշխատի, հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի, այո, ամեն ինչ պարզ է, շնորհակալ եմ, լավ, ուրեմն մինչեւ վաղը, հաջողություն։

**xachatur-fast_1.wav** — ref: Բարև, ինչպե՞ս ես։ Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։ Վաղը ժամը տասին հանդիպում ունենք։ Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Բարև, ինչպես ես, ես լավ եմ շնորհակալություն, իսկ դու՝ վաղի ժամը տասին հանդիպում ունենք, կարո՞ղ ես կրկնել, լավ չլսեցիմ
- `seamless:facebook/seamless-m4t-v2-large` (0%): Բարեւ, ինչպես ես, ես լավ եմ շնորհակալություն, իսկ դու վաղը ժամը տասին հանդիպում ունենք, կարող ես կրկնել, լավ չլսեցի։

**xachatur-fast_2.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։ Երևանում այսօր շատ շոգ է։ Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։ Ո՞վ է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Այս շաբաթ շատ աշխատանք ունում, երևանում այսօր շատ շոգ է, մենք պետք է ավարտենք նախագիծը միշագուրբաթ, ո՞վ է պատասխանատու այս հարցի համար
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այս շաբաթ շատ աշխատանք ունեմ, Երեւանում այսօր շատ շոգ է, մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ, ով է պատասխանատու այս հարցի համար։

**xachatur-fast_3.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։ Զանգիր ինձ, երբ տուն հասնես։ Գինը հազար հինգ հարյուր դրամ է։ Արամը և Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (17%): Ես համաձայն չեմ, կարծում եմ ավել լավ տարբերակ կա, զանգին ինձ, երբ տուն հասնես, գինը հինգ հազար հարեր դրամ, Արամը և անին երեք գնացին գյումրի,
- `seamless:facebook/seamless-m4t-v2-large` (11%): Ես համաձայն չեմ, կարծում եմ ավելի լավ տարբերակ կա, զանգիր ինձ երբ տուն հասնես, գինը հինգ հազար հարյուր դրամ, Արամը եւ Անին երեկ գնացին Գյումրի։

**xachatur-fast_4.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։ Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։ Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։ Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (1%): Ինտերնետը նորից դանդաղ է աշխատում, խնդրում եմ ուղղարկիր ինձ այդ ֆայլը, մենք օգտագործում ենք արհեստական բանականություն, թարգմանության համար, ներողություն, ուշացա, խցանում էր.
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում, խնդրում եմ ուղարկիր ինձ այդ ֆայլը, մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար, ներողություն, ուշացա, խցանում էր։

**xachatur-fast_5.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։ Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։ Այո, ամեն ինչ պարզ է, շնորհակալ եմ։ Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Ի՞նչ ես կարծում, սակա աշխատի՞,- հաջորդ ամիս պատրաստվում եմ մեկն էլ թբիլիսի,- այո, ամենինչ պարզը, շնորհակալը,- լավ, ուրեմը մինչ վաղ է, հաջողություն
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինչ ես կարծում, սա կաշխատի, հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի, այո, ամեն ինչ պարզ է, շնորհակալ եմ, լավ, ուրեմն մինչեւ վաղը հաջողություն։


## Same joined set, cut by the live Segmenter

10 recordings, 130 s of audio, from the joined set (cut by the live Segmenter)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 3.2% | 14.5% | 2.08s | 2.22s | 2.22s | 0.16 | 12s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 5.1% | 25.2% | 1.51s | 1.58s | 1.58s | 0.12 | 2s |

CER by speaker:

| backend | xachatur | xachatur-fast |
| --- | --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 2.4% | 7.9% |
| `seamless:facebook/seamless-m4t-v2-large` | 0.7% | 5.7% |

CER by source:

| backend | joined |
| --- | --- |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 5.1% |
| `seamless:facebook/seamless-m4t-v2-large` | 3.2% |
