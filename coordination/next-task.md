# Next Task for Cursor

**Task ID:** SB-007  
**Status:** Ready  
**Priority:** High  
**Owner:** Cursor  
**Branch:** `feature/voice-coach-improvements`

## Objective

Improve the existing SpeakBetter AI LiveKit voice experience across four connected areas in one coordinated task:

1. Response latency
2. Adaptive CART coaching intelligence
3. Voice quality and conversational naturalness
4. Integrated testing and reliability

The current local prototype can connect, accept speech, and respond, but responses feel slow, the voice/tone needs improvement, and the coach can feel repetitive or generic.

Preserve the existing Python CART coaching implementation and the minimal text CLI. Do not build a separate chat product or deploy to the cloud.

## Required workflow

Before coding, read:
- `coordination/README.md`
- `coordination/project-state.md`
- `coordination/decisions.md`
- `coordination/cursor-report.md`
- `coordination/next-task.md`
- `coach/README.md`
- `coach/VOICE.md`
- the current coach and LiveKit voice implementation, tests, and relevant knowledge files

Inspect the current branch, working tree, recent commits, and application structure.

- This task must run only on `feature/voice-coach-improvements`.
- The `ai-coordination` branch has already been merged into `main`.
- The feature branch was created from the latest `main`.
- Never make changes directly on `main`.
- Do not overwrite, discard, or silently include unrelated user changes.
- If the checked-out branch is not `feature/voice-coach-improvements`, or there are unrelated uncommitted changes, stop and report the blocker. Do not switch branches automatically.
- Preserve existing CLI commands, CART knowledge, research documents, and architecture unless a concrete need for change is demonstrated.

## Phase 1 — Establish a baseline and diagnose

Inspect the full path from user speech to spoken response:
- speech endpoint detection / VAD;
- speech-to-text;
- coach/LLM processing;
- text-to-speech;
- audio playback and turn completion;
- configuration and error handling.

Measure the current latency at each stage where practical. Record the measurement method and environment. Separate measured facts from hypotheses; do not claim a root cause without evidence.

## Phase 2 — Improve response latency

Use the baseline to target actual bottlenecks. Instrument timings for the key stages and overall time-to-first-audio where feasible.

Avoid unnecessary model calls and redundant processing. Tune endpointing only with care: do not cut the user off or treat every short pause as the end of a thought. Keep the implementation understandable and compatible with the existing stack. Do not introduce new paid services or switch providers without a demonstrated need.

Report before/after measurements under comparable conditions when possible. If comparable live measurements cannot be obtained, say so and provide the available evidence.

## Phase 3 — Improve adaptive coaching intelligence

Continue using the existing `CoachApp`, CART flow (Context → Adversity → Resolution → Takeaway), and `knowledge/cart.md`. Do not create a second independent coaching brain or replace CART with a generic prompt.

The coach should:
- understand the user's immediate goal and current context;
- ask relevant follow-up questions only when needed;
- avoid repeating questions or advice already given;
- let the user finish explaining their thoughts;
- avoid generic or unsolicited feedback after every sentence/answer;
- provide feedback, rewrites, or refinement when requested or at an appropriate coaching checkpoint;
- adapt its response to interview practice, workplace conversations, presentations, and other communication scenarios;
- preserve explicit CART navigation commands and current coaching behavior.

Add or update focused tests for adaptive behavior and regression cases. Prefer small, testable changes over broad redesign.

## Phase 4 — Improve voice quality and naturalness

Inspect the existing LiveKit/OpenAI speech configuration and actual supported options. Improve naturalness, pacing, tone, and spoken response length where the current stack allows it.

Keep voice responses concise but useful and context-aware. Avoid repetitive canned phrasing. Do not claim voice quality improved based only on configuration changes; identify what changed and whether it was verified in a real listening test. Do not expose secrets or add unnecessary providers/dependencies.

## Phase 5 — Integrated reliability and testing

Treat all four areas as one integrated deliverable. Validate interactions between latency, endpointing, coaching behavior, and audio output.

- Preserve all existing tests and CLI behavior.
- Add offline regression tests for the changed logic where practical.
- Mock external LiveKit/OpenAI calls in automated tests; tests must not require paid API calls.
- Run the full offline test suite and relevant lint/build checks available in the repository.
- If local LiveKit services and credentials are available, attempt a real browser-to-agent voice session and record the result.
- Clearly distinguish unit/offline tests from a real end-to-end test.
- If live testing is unavailable, report **not tested** and give exact commands and steps for the owner to run locally.
- Do not report a check as passing unless it actually ran and passed.

## Phase 6 — Documentation and handoff

Update relevant documentation, including `coordination/cursor-report.md` and `coordination/project-state.md`, based only on verified changes.

The final report must include:
1. Root causes found, with evidence.
2. Files changed and why.
3. Before/after latency measurements and measurement conditions, where available.
4. Coaching behavior changes and tests.
5. Voice configuration changes and whether voice quality was actually listened to/verified.
6. Exact test commands and results, including pass/fail counts.
7. Live end-to-end status: passed, failed, or not tested.
8. Remaining limitations, assumptions, and risks.
9. Exact local commands/steps to test on macOS.
10. Commit SHA/URL and verified remote push status.

Review the diff and ensure no credentials or local secrets are committed.

Commit task-related code, documentation, and coordination report on `feature/voice-coach-improvements`. Push that feature branch to origin and verify the remote commit. Do not merge into `main` or any other branch. Stop after this task; do not start a follow-up task automatically.

## Acceptance criteria

- The changes are on `feature/voice-coach-improvements`, not `main`.
- Existing CART knowledge and text CLI behavior are preserved.
- The four requested areas are addressed as one integrated task.
- Latency claims are backed by measurements or explicitly qualified.
- Coaching changes have relevant regression coverage.
- Voice changes and their verification status are clearly documented.
- The full offline test suite is run and its actual result reported.
- Real voice end-to-end status is reported truthfully.
- Coordination documents are updated, the feature branch is pushed, and the commit is identified.
- No merge into `main` is performed.

Start with repository and branch inspection, then establish the baseline before implementing changes. If blocked by branch state, local changes, unavailable services, or provider compatibility, report the specific blocker and continue only with independent safe work.
