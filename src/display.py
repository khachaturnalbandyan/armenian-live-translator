"""Terminal output: one line per segment, with time, speaker, Armenian and English."""

from __future__ import annotations

import sys

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
SPEAKER_COLORS = ["\033[36m", "\033[33m", "\033[35m", "\033[32m", "\033[34m", "\033[31m"]


class Printer:
    def __init__(
        self, stream=sys.stdout, color: bool | None = None, output_file: str | None = None
    ):
        self.stream = stream
        self.color = stream.isatty() if color is None else color
        self.output_file = output_file
        self._colors: dict[str, str] = {}

    def _paint(self, text: str, code: str) -> str:
        return f"{code}{text}{RESET}" if self.color else text

    def speaker_color(self, speaker: str) -> str:
        if speaker not in self._colors:
            self._colors[speaker] = SPEAKER_COLORS[len(self._colors) % len(SPEAKER_COLORS)]
        return self._colors[speaker]

    def segment(
        self,
        started_at: float,
        timestamp: float,
        speaker: str,
        armenian: str,
        english: str,
        stats: str = "",
    ) -> None:
        clock = timestamp - started_at
        hh, rem = divmod(int(clock), 3600)
        mm, ss = divmod(rem, 60)
        stamp_raw = f"[{hh:02d}:{mm:02d}:{ss:02d}]"
        who_raw = f"{speaker:<9}"

        line = f"{self._paint(stamp_raw, DIM)} {self._paint(who_raw, self.speaker_color(speaker))} HY: {self._paint(armenian, BOLD)}  EN: {english}"
        if stats:
            line += f"  {self._paint(stats, DIM)}"
        print(line, file=self.stream, flush=True)

        if self.output_file:
            plain_line = f"{stamp_raw} {who_raw} HY: {armenian}  EN: {english}"
            if stats:
                plain_line += f"  {stats}"
            try:
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(plain_line + "\n")
            except OSError as exc:
                print(f"! failed to write output file: {exc}", file=sys.stderr)
