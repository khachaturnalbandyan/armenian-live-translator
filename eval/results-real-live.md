40 recordings, 132 s of audio, from eval/real/manifest.json (cut by the live Segmenter)
Latency = recognition time per recording; the 5 s budget also includes translation.

| backend | CER | WER | latency p50 | p95 | max | RTF | load |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 2.9% | 13.7% | 0.44s | 0.63s | 0.71s | 0.14 | 7s |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.9% | 28.5% | 0.37s | 0.45s | 0.62s | 0.11 | 2s |

CER by speaker:

| backend | xachatur | xachatur-fast |
| --- | --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 0.9% | 4.9% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 5.1% | 8.6% |

CER by source:

| backend | mic |
| --- | --- |
| `seamless:facebook/seamless-m4t-v2-large` | 2.9% |
| `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` | 6.9% |

**xachatur_mic_001.wav** — ref: Բարև, ինչպե՞ս ես։
- `seamless:facebook/seamless-m4t-v2-large` (0%): բարեւ, ինչպես ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Բարև, ինչպես ես

**xachatur_mic_002.wav** — ref: Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես լավ եմ, շնորհակալություն, իսկ դու։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ես լավ եմ շնորհակալություն, իսկ դու

**xachatur_mic_003.wav** — ref: Վաղը ժամը տասին հանդիպում ունենք։
- `seamless:facebook/seamless-m4t-v2-large` (11%): Վաղը ժամը քանի՞սին հանդիպում ունենք։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (11%): Վաղը ժամը քանիսին հանդիպում ունենք։

**xachatur_mic_004.wav** — ref: Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Կարող ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): կարող ես կրկնել, լավ չլսեցի

**xachatur_mic_005.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Այս շաբաթ շատ աշխատանք ունեմ։

**xachatur_mic_006.wav** — ref: Երևանում այսօր շատ շոգ է։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Երեւանում այսօր շատ շոգ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Երևանում այսօր շատ շոգ է։

**xachatur_mic_007.wav** — ref: Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Մենք պետք է ավարտենք նախագիտը մինչև ուրբաթ։

**xachatur_mic_008.wav** — ref: Ո՞վ է պատասխանատու այս հարցի համար։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ով է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Ո՞վ է պատասհանատու այս հարցի համար։

**xachatur_mic_009.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես համաձայն չեմ, կարծում եմ կա ավելի լավ տարբերակ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Ես համաձայն չեմ, կարծում եմ կա ավելիավ տարբերակ։

**xachatur_mic_010.wav** — ref: Զանգիր ինձ, երբ տուն հասնես։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Զանգիր ինձ, երբ տուն հասնես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Զանգիր ինձ, երբ տուն հասնես

**xachatur_mic_011.wav** — ref: Գինը հազար հինգ հարյուր դրամ է։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Գինը հազար հինգ հարյուր դրամ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (12%): Կինը հազար հին քարյուր դրամ է։

**xachatur_mic_012.wav** — ref: Արամը և Անին երեկ գնացին Գյումրի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Արամը եւ Անին երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Արամը և անին երեք գնացին գյումրի։

**xachatur_mic_013.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Ինտերնետը նորից դանդաղ է աշխատում։

**xachatur_mic_014.wav** — ref: Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Խնդրում եմ ուղարկիր ինձ այդ ֆայլը։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը

**xachatur_mic_015.wav** — ref: Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (2%): Մենք օգտագործում ենք արհեստակաբանականություն թարգմանության համար։

**xachatur_mic_016.wav** — ref: Ներողություն, ուշացա, խցանում էր։
- `seamless:facebook/seamless-m4t-v2-large` (7%): ներողություն, ուշացա։ խաչանում էր
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (44%): Ուշացա։ Խցանում էր։

**xachatur_mic_017.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինչ ես կարծում, սա կաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Ի՞նչ ես կարծում, սա կա աշխատի՞

**xachatur_mic_018.wav** — ref: Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Հաջորդ ամիս պատրաստվում է մեկն էլ թբիլիսի։

**xachatur_mic_019.wav** — ref: Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Այո՛, ամենինչ պարզ է, շնորհկալ եմ

**xachatur_mic_020.wav** — ref: Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Լավ, ուրեմն մինչեւ վաղը, հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Լավ, ուրեմն մինչև վաղ է, հաջողություն

**xachatur-fast_mic_021.wav** — ref: Բարև, ինչպե՞ս ես։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Բարեւ, ինչպես ես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Բարև, ինչպես ես

**xachatur-fast_mic_022.wav** — ref: Ես լավ եմ, շնորհակալություն, իսկ դո՞ւ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ես լավ եմ, շնորհակալություն, իսկ դու։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Ես լավ եմ շնորհակալություն, իսկ դո

**xachatur-fast_mic_023.wav** — ref: Վաղը ժամը տասին հանդիպում ունենք։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Վաղը ժամը տասին հանդիպում ունենք։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Վաղը ժամը տասին հանդիպում ունենք։

**xachatur-fast_mic_024.wav** — ref: Կարո՞ղ ես կրկնել, լավ չլսեցի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Կարող ես կրկնել, լավ չլսեցի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (14%): Կարո՞ղ ես գրգնել, լավ չլսեցիմ

**xachatur-fast_mic_025.wav** — ref: Այս շաբաթ շատ աշխատանք ունեմ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): այս շաբաթ շատ աշխատանք ունեմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Այս շաբաթ շատ աշխատանք ունեն։

**xachatur-fast_mic_026.wav** — ref: Երևանում այսօր շատ շոգ է։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Երեւանում այսօր շատ շոգ է։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Երևանում այսօր շատ շոգ է։

**xachatur-fast_mic_027.wav** — ref: Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք պետք է ավարտենք նախագիծը մինչեւ ուրբաթ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Մենք պետք է ավարտենք նախագիծը մինչև ուրբաթ։

**xachatur-fast_mic_028.wav** — ref: Ո՞վ է պատասխանատու այս հարցի համար։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ով է պատասխանատու այս հարցի համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (7%): Ո՞վ է պատասխանալ տու այս հարթի համար։

**xachatur-fast_mic_029.wav** — ref: Ես համաձայն չեմ, կարծում եմ՝ կա ավելի լավ տարբերակ։
- `seamless:facebook/seamless-m4t-v2-large` (10%): Ես համաձայն չեմ, կարծում եմ ավելի լավ տարբերակ կա։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (15%): Ես համաձյն չեմ, կարծում եմ ավել լավ տարբերակ կա

**xachatur-fast_mic_030.wav** — ref: Զանգիր ինձ, երբ տուն հասնես։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Զանգիր ինձ, երբ տուն հասնես։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Զանգիր ինձ, երբ տուն հասնես

**xachatur-fast_mic_031.wav** — ref: Գինը հազար հինգ հարյուր դրամ է։
- `seamless:facebook/seamless-m4t-v2-large` (36%): Գինը հինգ հազար հարյուր դրամ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (56%): Կինը հինգ հազար հարերդ դրամ։

**xachatur-fast_mic_032.wav** — ref: Արամը և Անին երեկ գնացին Գյումրի։
- `seamless:facebook/seamless-m4t-v2-large` (7%): Արամը եւ Աննան երեկ գնացին Գյումրի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Արամը և անին երեք գնացին գյումրի։

**xachatur-fast_mic_033.wav** — ref: Ինտերնետը նորից դանդաղ է աշխատում։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ինտերնետը նորից դանդաղ է աշխատում։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (3%): Ինտերնետը նորից դանդառ է աշխատում։

**xachatur-fast_mic_034.wav** — ref: Խնդրում եմ, ուղարկիր ինձ այդ ֆայլը։
- `seamless:facebook/seamless-m4t-v2-large` (7%): Խնդրում եմ ուղարկեք ինձ այդ ֆայլը։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (14%): Ընդրում եմ ուղղարկիր ինձ այդ վայելը։

**xachatur-fast_mic_035.wav** — ref: Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (0%): Մենք օգտագործում ենք արհեստական բանականություն թարգմանության համար։

**xachatur-fast_mic_036.wav** — ref: Ներողություն, ուշացա, խցանում էր։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Ներողություն, ուշացա, խցանում էր։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (4%): Հերողություն, ուշացա, խցանում էր

**xachatur-fast_mic_037.wav** — ref: Ի՞նչ ես կարծում, սա կաշխատի՞։
- `seamless:facebook/seamless-m4t-v2-large` (0%): ինչ ես կարծում սա կաշխատի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (5%): Ի՞նչ ես կարծում, սակա աշխատի՞

**xachatur-fast_mic_038.wav** — ref: Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `seamless:facebook/seamless-m4t-v2-large` (0%): Հաջորդ ամիս պատրաստվում եմ մեկնել Թբիլիսի։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (8%): Հաջորդ ամիս պատրաստվում է մեկն էլ թբիլիսի։

**xachatur-fast_mic_039.wav** — ref: Այո, ամեն ինչ պարզ է, շնորհակալ եմ։
- `seamless:facebook/seamless-m4t-v2-large` (38%): այո ամեն ինչ պարզ է հիմա այնտեղ եմ։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (19%): Այո, ամենիչ պարզը, շնորհագալը

**xachatur-fast_mic_040.wav** — ref: Լավ, ուրեմն մինչև վաղը, հաջողություն։
- `seamless:facebook/seamless-m4t-v2-large` (0%): լավ ուրեմն մինչեւ վաղը հաջողություն։
- `faster-whisper:hurricup/whisper-large-v3-turbo-armenian-ct2` (16%): Լավ, ուրեմ ու մինչ վաղ է, հաջողություն

