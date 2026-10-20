# Next Task for Cursor

**Task ID:** SB-006  
**Status:** Ready  
**Priority:** High  
**Owner:** Cursor  
**Branch:** `ai-coordination`

## Objective

Build a **local LiveKit voice prototype for SpeakBetter AI**, integrating real-time browser voice with the existing Python CART coach. The deliverable is a working local prototype where the user can speak, the coach uses the existing CART logic, and the response is spoken back.

This is one task: voice integration is the implementation; the local voice prototype is the outcome. Do not build a separate chat UI or deploy to the cloud in this task.

## Required context

Before coding, read:
- `coordination/README.md`
- `coordination/project-state.md`
- `coordination/decisions.md`
- `coordination/cursor-report.md`
- `coordination/next-task.md` (this task)
- `coach/README.md`
- `coach/requirements.txt`
- the Python coach implementation and tests
- `knowledge/cart.md`

Inspect the current branch, working tree, recent commits, and current application structure. The last reported baseline was 32 passing offline tests, but verify the actual current state.

## Scope

### 1. Repository and architecture inspection
- Work only on `ai-coordination`.
- Check branch and working-tree status before editing.
- Preserve any existing user changes. If the branch is wrong or unrelated uncommitted changes are present, stop and report the blocker; do not switch branches or discard changes.
- Identify the existing CART coach entry point, OpenAI integration, configuration loading, and reusable coaching functions.
- Keep the implementation small and aligned with the current Python project.

### 2. LiveKit voice agent
- Use a currently supported, compatible LiveKit Agents Python SDK and documented APIs.
- Connect the agent to the existing CART coaching logic rather than duplicating CART instructions or building a second coach.
- Reuse the current OpenAI integration where practical, or document why a compatible LiveKit-supported provider path is preferable.
- Explicitly configure the required language-model and speech input/output components. Do not assume LiveKit transport alone provides speech recognition or text-to-speech.
- Keep the existing CLI and its commands working.

### 3. Minimal browser voice interface
Provide the smallest usable browser interface needed to:
- connect to a voice session;
- request microphone permission and capture speech;
- hear the agent's spoken response;
- display connection/session status and useful errors;
- disconnect cleanly.

Extend an existing frontend if one exists. If none exists, add only a minimal local interface and the smallest required backend/token endpoint. Do not build a separate chat product, elaborate dashboard, authentication system, or cloud deployment.

### 4. CART coaching behavior and turn-taking
Preserve Context → Adversity → Resolution → Takeaway and the existing coaching knowledge in `knowledge/cart.md`.

The user wants to speak freely before receiving a response:
- configure supported turn detection/endpointing and interruption behavior to avoid cutting off a user's thought;
- do not treat every short pause as the end of a turn;
- handle intentional user interruption gracefully;
- avoid duplicate responses;
- do not offer unsolicited feedback, rewrites, hints, or suggestions after every answer;
- only provide feedback/refinement when the user asks for it, while preserving explicit CART navigation commands and the current coaching flow.

Make sensible configurable choices and document known limits. Do not claim turn-taking is perfect unless verified in a real session.

### 5. Configuration and secrets
- Inspect current .env loading and .gitignore before changing configuration.
- Document the required LiveKit URL, API key, API secret, and any model/speech provider keys using the exact names required by the selected SDK.
- Update `.env.example` and setup documentation as needed, with placeholders only.
- Never overwrite the owner's local `.env`; never hardcode, print, or commit credentials.
- If LiveKit credentials or provider configuration are unavailable in the agent environment, complete independent work and tests, then clearly list what the owner must configure. Never invent credentials or claim a live connection worked when it did not.

### 6. Local setup and documentation
Document exact macOS commands from the repository root to install dependencies and start the agent and frontend. Explain how the browser obtains a short-lived LiveKit access token without exposing the API secret to the browser.

Document the selected architecture, speech/LLM providers, environment variables, local test procedure, any likely separate service/API usage charges, and troubleshooting. Do not deploy to cloud in SB-006.

### 7. Tests and validation
- Preserve existing tests and CLI behavior.
- Add offline tests for configuration validation, agent-to-CART integration, and token/session endpoint behavior where practical.
- Mock external LiveKit/OpenAI calls in automated tests; tests must not require paid API calls.
- Run the complete offline test suite and any available lint/build checks.
- Report the actual number of passing/failing tests.
- If credentials and local services are available, attempt a real browser-to-agent voice test. Clearly distinguish unit tests, mocked tests, and real end-to-end testing. If end-to-end testing cannot be performed, say **not tested** and provide the exact owner steps needed to test it.

### 8. Coordination report and Git workflow
- Update `coordination/cursor-report.md` with changed files, architecture choices, commands run and actual results, real voice test status, assumptions, risks/blockers, commit SHA/URL, push status, and the recommended next step.
- Update `coordination/project-state.md` to reflect only verified changes.
- Do not change `knowledge/cart.md` or existing research documents unless a necessary issue is found; if so, explain it before making unrelated changes.
- Review the final diff and ensure no secrets are staged.
- Commit task-related changes and the coordination report together on `ai-coordination`, then push to `origin/ai-coordination` and verify the remote commit, following the repository's coordination workflow.
- Do not merge to `main`.
- Stop after SB-006. Do not start a follow-up task.

## Acceptance criteria

1. Existing text CLI still works and existing tests pass.
2. A Python LiveKit voice agent can be started locally, subject to documented credentials.
3. A browser can connect, use the microphone, and receive spoken agent responses when credentials/providers are configured.
4. The voice agent uses the existing CART coach and knowledge rather than a duplicated generic coach.
5. Turn-taking is configured to let the user finish speaking; unsolicited suggestions after each answer are avoided.
6. The browser never receives the LiveKit API secret.
7. Setup instructions are executable and secrets remain uncommitted.
8. Offline tests pass, and real end-to-end voice status is reported truthfully.
9. The coordination report and project state are updated, and the commit is pushed to `origin/ai-coordination`.

Start with inspection, then implement the smallest viable local prototype. If any provider/API compatibility question arises, consult the SDK's current documentation rather than guessing.
