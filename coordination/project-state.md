# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-006 — local LiveKit voice prototype (task defined; implementation not yet verified).

## Product direction
Build a natural spoken coaching experience around the existing CART method (Context, Adversity, Resolution, Takeaway). Preserve the current Python text CLI and its coaching knowledge. The first voice milestone is local-only; cloud deployment is a later task.

## Last verified application state (SB-005)
- Repository: `KaranAgar1987/speakbetter-ai` on `ai-coordination` (not merged to `main`).
- `coach/SMOKE-TEST.md` — manual live-API checklist (macOS); notes billing and never committing keys.
- `coach/README.md` — macOS setup/run steps; links to smoke-test documentation.
- CLI hardening: `save` matches only the intended command token; save failures report failure; write errors handled cleanly; missing API key exits with a message.
- Offline tests: **32 passed** in the last reported SB-005 run. Re-run before relying on this baseline.
- Live OpenAI end-to-end session was not run in the Cursor agent environment during SB-005; the owner later reported a successful live text session.
- `knowledge/cart.md` and `research/philipp-humm/` were preserved through SB-005.

## SB-006 scope
- Build a minimal browser microphone + spoken-response prototype connected through LiveKit to the existing Python CART coach.
- Preserve CART flow and current CLI; do not build a separate chat product.
- Configure turn-taking so the user can speak freely without unsolicited suggestions after each answer.
- Test locally first; no cloud deployment in this milestone.
- Actual implementation and end-to-end voice status remain **unverified until Cursor reports results**.

## Prior milestones
- SB-005: [5accb7b](https://github.com/KaranAgar1987/speakbetter-ai/commit/5accb7b7614825d6dcfae0243c580784c8b3bc0a)
- SB-004: [fa66657](https://github.com/KaranAgar1987/speakbetter-ai/commit/fa6665709be0a0b99958bcedb8452b582694c528)
- SB-003: [72bb217](https://github.com/KaranAgar1987/speakbetter-ai/commit/72bb217684ed7719f5bf199d4eab26aa8d238edd)

## Next step
Cursor: read `coordination/next-task.md` and execute SB-006 on `ai-coordination`. ChatGPT reviews the report after Cursor commits and pushes the result.
