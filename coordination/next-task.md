# Next Task for Cursor

**Task ID:** SB-005  
**Status:** Ready  
**Priority:** High  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective
Prepare and validate the first real user smoke test of the existing text-only CART CLI. Do not add another product feature yet. Make setup/run instructions and runtime failure handling clear, then run all checks that can be performed without a real API key.

## Scope
1. Read `coordination/README.md`, `coordination/project-state.md`, `coordination/decisions.md`, `coordination/cursor-report.md`, `coach/README.md`, and the coach implementation and tests.
2. Inspect the full user path: setup, automatic `.env` loading, CLI start, Context → Adversity → Resolution → Takeaway, `next` through assembly, `save`, and `quit`.
3. Check for obvious command-parsing and state-flow edge cases. In particular, confirm the `save` command only matches the intended command syntax (not unrelated words beginning with “save”), and that its success/failure message reflects whether a write actually succeeded.
4. Add or adjust focused offline tests for any defects found. Mock the model/API; no test may require a real OpenAI key or network.
5. Ensure expected user-facing errors (missing API key, invalid save arguments, permission/path errors) fail clearly without printing secret values or a traceback where avoidable. Do not hide unexpected programming errors silently.
6. Keep setup instructions concise and executable on macOS. Verify they consistently describe venv creation, installing requirements, copying `coach/.env.example` to `coach/.env`, editing the local key, and launching from the repository root. Never put a real key in a committed file.
7. Add a short `coach/SMOKE-TEST.md` with a manual test checklist and expected outcomes. Include a clear note that a live API call incurs API usage charges and that the user should use their own valid API key locally. Do not ask the user to paste a key into chat or commit it.
8. Run the full offline suite and any safe CLI checks possible without the API. Clearly mark live API behavior as **not tested** if no key is available; do not claim an end-to-end live session.
9. Update `coordination/cursor-report.md` and `coordination/project-state.md` with factual outcomes and remaining limitations.

## Acceptance criteria
- A new user can follow the macOS setup steps without manually sourcing `.env`.
- Tests cover the important command/state edge cases discovered in inspection.
- Saving never reports success if writing failed and never silently overwrites an existing file without `--force`.
- Full offline test suite passes.
- `coach/SMOKE-TEST.md` gives a clear manual validation sequence and expected behavior.
- No secrets are committed or printed.
- Report includes changed files, exact commands and actual results, limitations, commit SHA and commit URL.

## Git workflow (required)
- Work only on `ai-coordination`. Check current branch and working tree first; preserve unrelated user changes. If the branch is wrong or unrelated uncommitted changes exist, stop and report the blocker without discarding anything.
- Implement only SB-005; avoid new frameworks, unrelated refactors, web UI, voice/video, databases, and research edits.
- Run focused tests and the full test suite, review the final diff, and verify no real secrets are staged.
- Update `coordination/cursor-report.md` and `coordination/project-state.md`.
- Commit task-related changes, push to `origin/ai-coordination`, verify the remote commit, and report full SHA, URL, push status and test results.
- Do not merge to `main` and do not start another task after SB-005.
