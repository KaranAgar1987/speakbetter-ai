"""Per-turn timing for voice latency diagnosis."""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class TurnTimer:
    """Record stage timestamps for one user turn."""

    started_at: float = field(default_factory=time.perf_counter)
    marks: dict[str, float] = field(default_factory=dict)

    def mark(self, stage: str) -> None:
        self.marks[stage] = time.perf_counter()

    def deltas_ms(self) -> dict[str, float]:
        ordered = sorted(self.marks.items(), key=lambda item: item[1])
        out: dict[str, float] = {}
        prev = self.started_at
        for name, ts in ordered:
            out[name] = round((ts - prev) * 1000, 1)
            prev = ts
        if ordered:
            out["total_ms"] = round((ordered[-1][1] - self.started_at) * 1000, 1)
        return out
