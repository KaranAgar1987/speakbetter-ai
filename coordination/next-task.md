# Next Task for Cursor

**Task ID:** SB-003  
**Status:** Ready  
**Priority:** Medium  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective
Make local setup less error-prone by automatically loading a local `.env` file for the CLI, while keeping secrets out of source control and preserving the minimal text-only CART coach.

## Scope
1. Read `coach/README.md`, `coach/requirements.txt`, the CLI entry point, configuration/API client code, and existing tests before editing.
2. Support loading environment variables from `coach/.env` or the repository-root `.env` at startup. Prefer the simplest reliable approach compatible with the existing project. If adding `python-dotenv`, keep the dependency explicit in `coach/requirements.txt`.
3. Preserve already-set process environment variables as the authoritative values; do not overwrite them with values from `.env`.
4. Keep `OPENAI_API_KEY` required and `OPENAI_MODEL` optional as currently documented. Never print secret values, include them in exceptions/reports, or commit a real `.env`.
5. Update `coach/README.md` so setup and run instructions accurately describe automatic loading and the supported `.env` location(s). Ensure `.env.example` contains placeholders only.
6. Add focused offline tests for loading behavior, precedence of process environment variables, and missing-key behavior. Mock external API calls; tests must not require a real key or network.
7. Do not add new product features, change CART coaching behavior, alter `knowledge/cart.md`, modify `research/philipp-humm/`, or merge into `main`.

## Acceptance criteria
- A user can create a local `coach/.env` by copying `coach/.env.example` and launch the CLI using the documented command without manually sourcing the file.
- A repository-root `.env` is supported if documented; precedence is deterministic and tested.
- Existing process environment variables take precedence over file values.
- Offline tests pass, and no secret values are committed or logged.
- `coordination/cursor-report.md` records changed files, exact commands and actual results, limitations, and the resulting commit SHA/link.

## Git workflow (required for this task)
- Work only on `ai-coordination`. Check the current branch and working tree first; preserve unrelated user changes. If unrelated uncommitted changes exist or the branch is wrong, stop and report the blocker without discarding changes.
- Implement only this task, run the focused tests and the full existing test suite, and review the final diff.
- Update `coordination/cursor-report.md` and `coordination/project-state.md` with verified facts.
- Commit only SB-003-related changes with a clear message.
- Push the commit to `origin/ai-coordination` and verify the remote commit. Report the full SHA, GitHub commit URL, push status, and test results. Do not claim success without verification.
- Do not merge to `main` and do not start another task after SB-003.
