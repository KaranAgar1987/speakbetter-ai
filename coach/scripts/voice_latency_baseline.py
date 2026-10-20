"""Offline baseline: measure CoachApp handle_line time with/without voice context trim.

Run from repo root:
  PYTHONPATH=coach python coach/scripts/voice_latency_baseline.py
"""

import time

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.llm import ScriptCompleter


def _avg_ms(samples: list[float]) -> float:
    return round(sum(samples) / len(samples), 2)


def main() -> None:
    completer = ScriptCompleter()
    app = CoachApp(completer, "# CART\n", voice_mode=True, voice_conversational=True)
    app.start()
    for i in range(10):
        app.handle_line(f"Story beat {i}: we debated the launch timeline with leadership.")

    times: list[float] = []
    for _ in range(5):
        t0 = time.perf_counter()
        app.handle_line("The VP pushed back on scope and I had to reset expectations.")
        times.append((time.perf_counter() - t0) * 1000)

    print("Method: local ScriptCompleter (no network); after 10 prior turns.")
    print(f"Coach handle_line avg_ms={_avg_ms(times)} samples={len(times)}")


if __name__ == "__main__":
    main()
