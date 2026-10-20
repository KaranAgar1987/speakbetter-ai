# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-003 complete — automatic `.env` loading for the CART CLI.

## Product direction
SpeakBetter AI helps users improve workplace communication. The initial product is a minimal **text-based CART coach** (CLI), not voice/video or a large application stack.

## Core method
CART: **Context → Adversity → Resolution → Takeaway**, per `knowledge/cart.md`.

## Verified state after SB-003
- Repository: `KaranAgar1987/speakbetter-ai`
- Branch: `ai-coordination` (not merged to `main`).
- `coach/`: Python CLI loads `knowledge/cart.md`; OpenAI coaching; session commands unchanged from SB-002.
- **Environment:** On startup, `load_local_env()` loads `coach/.env` then repository-root `.env` via `python-dotenv` with `override=False` (shell variables win; `coach/.env` wins over root `.env` for duplicate keys).
- Dependencies: `openai`, `python-dotenv` in `coach/requirements.txt`.
- Offline tests: **19** passed (`PYTHONPATH=coach python -m unittest discover -s coach/tests -v`).
- `knowledge/cart.md` and `research/philipp-humm/` unchanged.

## Prior milestones
- SB-002 implementation: [`3e91930`](https://github.com/KaranAgar1987/speakbetter-ai/commit/3e91930eeb444267b4740d9f1df4692c0dabe8ec)

## Coordination workflow
- Cursor completes tasks per `coordination/next-task.md`, updates report/state, commits and pushes to `origin/ai-coordination`.
- Owner runs Cursor for each handoff; GitHub file changes do not auto-start Cursor.

## Next milestone
Review SB-003 commit and tests; ChatGPT defines the next task in `next-task.md`.
