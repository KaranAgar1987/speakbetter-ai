# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-005 — smoke-test readiness and CLI hardening (no new product features).

## Product direction
Minimal text-based CART coach (CLI), guided by `knowledge/cart.md`.

## Verified state after SB-005
- Repository: `KaranAgar1987/speakbetter-ai` on `ai-coordination` (not merged to `main`).
- `coach/SMOKE-TEST.md` — manual live-API checklist (macOS); notes billing and never committing keys.
- `coach/README.md` — macOS setup/run steps; links to smoke test doc.
- **CLI hardening:** `save` matches only the `save` command token; duplicate save reports **Save failed.**; write errors handled without traceback; missing API key exits with message via `__main__.py`.
- Offline tests: **32** passed (`PYTHONPATH=coach python -m unittest discover -s coach/tests -v`).
- **Live OpenAI end-to-end session:** not run in Cursor agent environment (no API key); owner validates via `SMOKE-TEST.md`.
- `knowledge/cart.md` and `research/philipp-humm/` unchanged.

## Prior milestones
- SB-004: [`fa66657`](https://github.com/KaranAgar1987/speakbetter-ai/commit/fa6665709be0a0b99958bcedb8452b582694c528)
- SB-003: [`72bb217`](https://github.com/KaranAgar1987/speakbetter-ai/commit/72bb217684ed7719f5bf199d4eab26aa8d238edd)

## Next milestone
Owner live smoke test; ChatGPT defines SB-006 in `next-task.md`.
