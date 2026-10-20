# Next Task for Cursor

**Task ID:** SB-002  
**Status:** Ready  
**Priority:** High  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective
Implement the smallest usable local, text-only CART coach as a Python command-line application. Use the existing `knowledge/cart.md` as the product specification. Do not build a web UI, voice/video features, database, multi-agent system, or modify the research corpus.

## Implementation scope
1. Add a small `coach/` directory with a runnable Python CLI, a concise README with setup/run instructions, and `.env.example` documenting `OPENAI_API_KEY` and any model setting. Never put real credentials in files or commits.
2. Use the OpenAI API for natural-language coaching, with the API key read only from the environment. Keep provider/model configuration simple and documented. Do not make network calls during tests.
3. Load `knowledge/cart.md` at runtime and use it as the source of coaching rules. Resolve its path robustly so the CLI can be launched from the repository root.
4. Guide the user through Context → Adversity → Resolution → Takeaway. Allow natural-language responses and useful follow-ups; support `hint`, `example`, `restart`, and `quit`. Clearly label examples as verified-source examples versus SpeakBetter illustrations according to `cart.md`.
5. Follow the constraints in `cart.md`: ask targeted follow-ups when a step is thin; do not give pass/fail judgments, numeric scores, or validation badges; do not present internal coach diagnostics as user-facing scores; preserve the distinction between verified material and original illustrations.
6. Keep the implementation minimal and readable. Avoid unnecessary dependencies and architecture. Do not edit `research/philipp-humm/` or rewrite `knowledge/cart.md`.
7. Add focused automated tests for the session flow and key behavior constraints. Mock the model/API layer so tests run offline. If no test framework is already present, use Python's standard library `unittest` rather than adding a large dependency.
8. Update `coordination/project-state.md` and this `coordination/cursor-report.md` to reflect actual implementation and validation results. Do not claim anything was tested unless it was run.

## Acceptance criteria
- A new user can follow the README to configure the API key and launch the CLI.
- The CLI loads `knowledge/cart.md` from the repository and provides a coherent text-only CART session.
- `hint`, `example`, `restart`, and `quit` work as documented.
- Automated tests pass offline and include at least one check preventing score/pass-fail language in normal coach output, where practical.
- No secrets are committed; no research corpus files are changed.
- The report lists changed files, exact commands run and results, remaining limitations, and the resulting commit SHA/link.

## Git workflow (required)
- Work only on `ai-coordination`; first check the current branch and working tree. Preserve unrelated user changes. If the branch is wrong or the working tree has unrelated changes, stop and report rather than switching or discarding work.
- After implementation, run the tests and any relevant manual checks.
- Update `coordination/cursor-report.md` and `coordination/project-state.md`.
- Commit all and only task-related changes on `ai-coordination` with a clear message.
- Push the commit to `origin/ai-coordination`. Verify that the push succeeded and report the full commit SHA and GitHub commit URL. Never claim it was pushed if it was not.
- Do not merge to `main`.
- Stop after SB-002; do not begin another task until ChatGPT updates `next-task.md`.

## Blockers
If the OpenAI API package or API behavior is unclear, inspect current project conventions and choose a small supported implementation. Do not require a live API key for automated tests. If a consequential issue prevents completion, document it and stop safely rather than inventing success.
