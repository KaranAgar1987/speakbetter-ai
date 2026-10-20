# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** Implement the first minimal text-based CART coach and validate the ChatGPT ↔ Cursor handoff.

## Product direction
SpeakBetter AI is intended to help users improve workplace communication and spoken responses. The initial product is a minimal **text-based CART coach**, not a complex architecture or video/audio product.

## Core method
Use the existing CART methodology:
1. **Context** — establish the situation and relevant background.
2. **Adversity** — identify the challenge, friction, or difficulty.
3. **Resolution** — explain the action taken or response chosen.
4. **Takeaway** — capture the learning and what to do differently next time.

Preserve the repository's existing research and knowledge documents; inspect and reuse them rather than replacing them.

## Known state (SB-001 inspection, 2026-10-20)
- Repository: `KaranAgar1987/speakbetter-ai`
- `main` remains at the initial research/knowledge commit; coordination and next-task changes are isolated on `ai-coordination`.
- Tracked content includes `knowledge/cart.md`, `research/philipp-humm/`, and `coordination/`.
- Primary coach specification: `knowledge/cart.md` (CART steps, coach rules, gap diagnostics, examples and attribution boundaries).
- Before SB-002: no application code, package manifest, tests, or CI existed.
- SB-001 report is available in `coordination/cursor-report.md`.

## Current workflow state
- `coordination/next-task.md` now defines **SB-002**, the first implementation task: a small local Python CLI coach using `knowledge/cart.md`.
- Cursor must work only on `ai-coordination`, preserve unrelated changes, implement the task, run offline tests, update the report and this state file, commit, push to `origin/ai-coordination`, and report the verified commit SHA/link.
- Do not merge to `main`; do not assume a feature is implemented until repository evidence and validation confirm it.
- GitHub file changes do not automatically start Cursor; the owner must run the Cursor Agent command for each handoff.

## Next milestone
Complete SB-002, review the pushed commit and test report, then decide the next smallest step.
