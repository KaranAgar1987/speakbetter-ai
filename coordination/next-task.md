# Next Task for Cursor

**Task ID:** SB-004  
**Status:** Ready  
**Priority:** Medium  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective
Let users save their completed CART story as a local Markdown file, so they can reuse and refine it after a coaching session.

## Scope
1. Read `coordination/README.md`, `coordination/project-state.md`, `coordination/decisions.md`, `coordination/cursor-report.md`, `coach/README.md`, and the CLI/session code and tests.
2. Understand how the CLI assembles and presents the final CART story. Reuse existing assembled content if available; do not call the model again just to save.
3. Add a simple explicit command such as `save` (optionally `save path/to/story.md`) that writes the current completed/assembled story to a local Markdown file. If the story is not ready, explain what the user needs to do first.
4. Default to a clear local filename such as `speakbetter-cart-story.md` in the current working directory. If a path is provided, handle it safely and explain where the file was written. Do not silently overwrite an existing file: ask for confirmation or choose a safe non-overwriting behavior.
5. Save only the user's CART story and useful section headings (Context, Adversity, Resolution, Takeaway). Do not include API keys, hidden prompts, internal diagnostics, or private model messages.
6. Update `coach/README.md` with the command and examples.
7. Add offline automated tests for successful save, missing/not-yet-assembled story, and existing-file behavior. Tests must use temporary directories and must not make network calls.
8. Keep the CLI text-only and minimal. Do not add database, web UI, voice/video, or new external dependencies unless strictly required.
9. Do not modify `knowledge/cart.md` or anything under `research/philipp-humm/`.

## Acceptance criteria
- User can explicitly save a completed CART story to a local Markdown file.
- Saving does not make an additional OpenAI API request.
- Incomplete sessions cannot be mistakenly saved as completed stories.
- Existing files are never silently overwritten.
- Offline tests pass; README documents the feature.
- Cursor report records changed files, exact commands and real results, limitations, full commit SHA, and commit URL.

## Git workflow (required)
- Work only on `ai-coordination`. Check branch and working tree first; preserve unrelated user changes. If the branch is wrong or unrelated uncommitted changes exist, stop and report.
- Implement only SB-004, run focused and full tests, and review the final diff.
- Update `coordination/cursor-report.md` and `coordination/project-state.md` with verified facts.
- Commit only task-related changes, push to `origin/ai-coordination`, and verify the remote commit.
- Report the full SHA, GitHub commit URL, push status, tests run/results, and any blockers. Never claim unverified success.
- Do not merge into `main` and do not start another task.
