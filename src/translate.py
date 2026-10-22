"""Armenian -> English translation with NLLB-200 (local, no cloud APIs)."""

from __future__ import annotations

import time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


class Translator:
    def __init__(
        self,
        model_name: str = "facebook/nllb-200-distilled-600M",
        src_lang: str = "hye_Armn",
        tgt_lang: str = "eng_Latn",
        device: str | None = None,
    ):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=src_lang)
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.model = (
            AutoModelForSeq2SeqLM.from_pretrained(model_name, dtype=dtype)
            .to(self.device)
            .eval()
        )
        self.tgt_token_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)

    def translate(self, text: str) -> tuple[str, float]:
        """Returns (english text, elapsed seconds)."""
        text = text.strip()
        if not text:
            return "", 0.0

        started = time.monotonic()
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(self.device)
        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tgt_token_id,
                max_new_tokens=256,
                num_beams=1,  # greedy: translation quality of a 600M model barely moves
            )
        english = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0].strip()
        return english, time.monotonic() - started
