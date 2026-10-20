# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** First minimal text-based CART coach (SB-002) implemented and under review.

## Product direction
SpeakBetter AI helps users improve workplace communication. The initial product is a minimal **text-based CART coach** (CLI), not voice/video or a large application stack.

## Core method
CART: **Context → Adversity → Resolution → Takeaway**, per `knowledge/cart.md` (verified from SRC-001, SRC-002).

## Known state (after SB-002)
- Repository: `KaranAgar1987/speakbetter-ai`
- `main`: initial research/knowledge commit only; product work on `ai-coordination`.
- **`coach/`** — Python CLI package `speakbetter_coach`: loads `knowledge/cart.md` at runtime, OpenAI-backed coaching, commands `hint` / `example` / `next` / `restart` / `quit`, guardrails against score/pass-fail language.
- **`knowledge/cart.md`** — unchanged; primary product spec.
- **`research/philipp-humm/`** — unchanged.
- **`coordination/`** — handoff files; latest task report in `cursor-report.md`.
- Tests: `PYTHONPATH=coach python -m unittest discover -s coach/tests -v` (14 tests, offline).

## Current workflow state
- SB-002 complete pending owner review of pushed commit and report.
- Do not merge to `main` without explicit owner decision.
- Next task will be written by ChatGPT in `next-task.md` after report review.

## Next milestone
Review SB-002 commit, run CLI manually with API key, then define the next smallest improvement (e.g. env loading, Hindi coach prompts, or session export).
