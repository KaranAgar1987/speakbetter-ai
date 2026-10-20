# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-002 implemented and reviewed; SB-003 is the next scoped usability improvement.

## Product direction
SpeakBetter AI helps users improve workplace communication. The initial product is a minimal **text-based CART coach** (CLI), not voice/video or a large application stack.

## Core method
CART: **Context → Adversity → Resolution → Takeaway**, per `knowledge/cart.md`.

## Verified state after SB-002
- Repository: `KaranAgar1987/speakbetter-ai`
- Implementation commit: [`3e91930`](https://github.com/KaranAgar1987/speakbetter-ai/commit/3e91930eeb444267b4740d9f1df4692c0dabe8ec)
- Follow-up report commit: [`0261329`](https://github.com/KaranAgar1987/speakbetter-ai/commit/0261329de5f119b4159a8a156815a08f66fcc7b0)
- Branch: `ai-coordination`; no merge to `main`.
- `coach/`: Python CLI package `speakbetter_coach`, loads `knowledge/cart.md`, uses OpenAI-backed coaching, supports `hint`, `example`, `next`, `restart`, `quit`, and includes guardrails.
- Offline tests reported in Cursor's report: 14 passed. Live API session was not tested because no API key was available in the agent environment.
- `knowledge/cart.md` and `research/philipp-humm/` were not modified.
- Current setup caveat: README says the CLI does not automatically load `.env`; users must export or source environment variables manually.

## Coordination workflow
- `coordination/next-task.md` defines SB-003: automatically load a local `.env` file safely, document setup, and add offline tests.
- Cursor must check branch and working tree, preserve unrelated changes, implement only the task, run tests, update the report/state, commit and push to `origin/ai-coordination`, and provide a verified commit SHA/link.
- Do not merge to `main`. GitHub file updates do not automatically start Cursor; the owner must run the Cursor Agent for each handoff.

## Next milestone
Complete SB-003, review the pushed commit and tests, then decide the next smallest product step.
