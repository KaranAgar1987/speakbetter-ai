# Next Task for Cursor

**Task ID:** SB-001  
**Status:** Ready  
**Priority:** High  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective
Inspect the existing SpeakBetter AI repository and produce a concise, evidence-based baseline assessment. Do not build the application in this task.

## Steps
1. Read `coordination/README.md`, `coordination/project-state.md`, and `coordination/decisions.md`.
2. Inspect the repository structure, existing research/knowledge docs, and any existing application code or tests.
3. Identify what already exists, what is missing for a minimal text-based CART coach, and any constraints or reusable material relevant to the first implementation.
4. Recommend the smallest sensible next implementation task. Keep the existing CART method (Context, Adversity, Resolution, Takeaway) and do not replace the research with generic content.
5. Do not install dependencies, create an app, or make unrelated edits in this task. Only edit `coordination/cursor-report.md`; update `project-state.md` only if the inspection reveals a factual correction to the current snapshot.

## Acceptance criteria
- The report lists the key folders/files inspected and summarizes what each relevant item contains.
- The report separates confirmed facts from assumptions and unknowns.
- The report identifies the simplest next coding task and relevant files to create or modify.
- No existing project files are changed other than the allowed coordination file updates.
- The report states which checks were run, or explicitly says none were needed for this inspection-only task.

## When complete
Replace the contents of `coordination/cursor-report.md` using the report template in that file, commit the report (and any justified factual state correction) on `ai-coordination`, and stop. Do not begin the next implementation task until ChatGPT updates this file.
