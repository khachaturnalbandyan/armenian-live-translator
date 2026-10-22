"""Terminal output: one line per segment, with time, speaker, Armenian and English."""

from __future__ import annotations

import sys

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
SPEAKER_COLORS = ["\033[36m", "\033[33m", "\033[35m", "\033[32m", "\033[34m", "\033[31m"]


class Printer:
    def __init__(self, stream=sys.stdout, color: bool | None = None):
        self.stream = stream
        self.color = stream.isatty() if color is None else color
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
        stamp = self._paint(f"[{hh:02d}:{mm:02d}:{ss:02d}]", DIM)
        who = self._paint(f"{speaker:<9}", self.speaker_color(speaker))
        line = f"{stamp} {who} HY: {self._paint(armenian, BOLD)}  EN: {english}"
        if stats:
            line += f"  {self._paint(stats, DIM)}"
        print(line, file=self.stream, flush=True)
