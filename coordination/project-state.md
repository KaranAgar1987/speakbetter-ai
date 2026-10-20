# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-004 complete — save assembled CART story to local Markdown.

## Product direction
SpeakBetter AI helps users improve workplace communication. The initial product is a minimal text-based CART coach (CLI), guided by `knowledge/cart.md`.

## Core method
CART: **Context → Adversity → Resolution → Takeaway**.

## Verified state after SB-004
- Repository: `KaranAgar1987/speakbetter-ai`
- Branch: `ai-coordination` (not merged to `main`).
- `coach/` CLI: CART session, OpenAI coaching, `.env` auto-load (SB-003).
- **Save:** `save` / `save path.md` / `save --force` writes user step drafts to Markdown after assembly (`Step.DONE`). Default file: `speakbetter-cart-story.md` in the process working directory. No extra API call on save; existing files are not silently overwritten.
- Offline tests: **26** passed — `PYTHONPATH=coach python -m unittest discover -s coach/tests -v`.
- `knowledge/cart.md` and `research/philipp-humm/` unchanged.

## Prior milestones
- SB-003: [`72bb217`](https://github.com/KaranAgar1987/speakbetter-ai/commit/72bb217684ed7719f5bf199d4eab26aa8d238edd)
- SB-002: [`3e91930`](https://github.com/KaranAgar1987/speakbetter-ai/commit/3e91930eeb444267b4740d9f1df4692c0dabe8ec)

## Coordination workflow
- Cursor implements tasks from `coordination/next-task.md`, updates report/state, commits and pushes to `origin/ai-coordination`.

## Next milestone
Review SB-004 commit; ChatGPT defines SB-005 in `next-task.md`.
