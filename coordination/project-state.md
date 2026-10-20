# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** Establish a reliable ChatGPT ↔ Cursor handoff, then build incrementally.

## Product direction
SpeakBetter AI is intended to help users improve workplace communication and spoken responses. The current agreed initial product direction is a minimal **text-based CART coach**, rather than a complex architecture or video/audio product at the outset.

## Core method
Use the existing CART methodology:
1. **Context** — establish the situation and relevant background.
2. **Adversity** — identify the challenge, friction, or difficulty.
3. **Resolution** — explain the action taken or response chosen.
4. **Takeaway** — capture the learning and what to do differently next time.

Preserve the repository's existing research and knowledge documents; inspect and reuse them rather than replacing them.

## Known state before the first Cursor inspection
- Repository: `KaranAgar1987/speakbetter-ai`
- The project contains research/knowledge documentation and CART methodology material.
- The minimal text-based coach has been proposed, but the first implementation has not yet been verified in this coordination workflow.
- The exact existing file structure and any current application code must be confirmed by Cursor in task SB-001.

## Current workflow state
- The `ai-coordination` branch is dedicated to coordination and initial handoff.
- Cursor's first task is inspection-only: document the repository baseline and recommend the smallest next coding step.
- Do not assume any feature is implemented until repository evidence and validation confirm it.

## Next milestone
After Cursor reports its findings, ChatGPT will review the report and write a focused implementation task into `next-task.md`.
