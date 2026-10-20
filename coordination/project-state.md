# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-003 verified; SB-004 is the next usability improvement.

## Product direction
SpeakBetter AI helps users improve workplace communication. The initial product is a minimal text-based CART coach (CLI), guided by `knowledge/cart.md`.

## Core method
CART: **Context → Adversity → Resolution → Takeaway**.

## Verified state after SB-003
- Repository: `KaranAgar1987/speakbetter-ai`
- SB-003 implementation commit: [`72bb217`](https://github.com/KaranAgar1987/speakbetter-ai/commit/72bb217684ed7719f5bf199d4eab26aa8d238edd), verified through GitHub commit metadata.
- The SB-003 report at `coordination/cursor-report.md` states the commit was pushed to `origin/ai-coordination`.
- `coach/` contains a Python CLI using OpenAI-backed coaching and the existing CART knowledge document.
- Local environment loading: `coach/.env` then repository-root `.env`, without overriding already-set process environment variables.
- Offline test suite reported 19 passing tests: `PYTHONPATH=coach python -m unittest discover -s coach/tests -v`.
- A live OpenAI session was not tested in the agent environment because no API key was available.
- `.gitignore` excludes root `.env` and `coach/.env`, while allowing `coach/.env.example`.
- `knowledge/cart.md` and `research/philipp-humm/` remain unchanged.

## Coordination workflow
- `coordination/next-task.md` defines SB-004: save the assembled CART story to a local Markdown file, with explicit non-overwrite behavior and offline tests.
- Cursor must inspect branch/status, preserve unrelated changes, implement only the scoped task, run tests, update report/state, commit and push to `origin/ai-coordination`, and verify the remote commit.
- Do not merge to `main`. Updating GitHub files does not automatically start Cursor; the owner must run the Cursor Agent for each handoff.

## Next milestone
Complete SB-004, review its verified commit and tests, then decide whether to prioritize live user testing or another small improvement.
