# Decisions

## D-001 — Use GitHub files for assistant handoffs
**Status:** Accepted  
**Decision:** Use the files in `coordination/` to pass tasks and reports between ChatGPT and Cursor.  
**Rationale:** This keeps instructions and results in a shared, versioned place and reduces manual copy/paste.  
**Consequence:** Cursor must be started or prompted to read the updated task; GitHub file changes do not automatically trigger Cursor by themselves.

## D-002 — Start on a separate coordination branch
**Status:** Accepted  
**Decision:** Use `ai-coordination` for the initial handoff setup and keep `main` untouched by this workflow.  
**Rationale:** Isolates coordination changes and reduces risk to existing research and project files.

## D-003 — Build incrementally
**Status:** Accepted  
**Decision:** Begin with repository inspection, then implement the smallest useful text-based CART coach before considering broader architecture or richer interaction modes.  
**Rationale:** Validate the existing project and core user experience before adding complexity.

## D-004 — Preserve existing CART research
**Status:** Accepted  
**Decision:** Keep Context, Adversity, Resolution, Takeaway as the core method and reuse existing research/knowledge documents where relevant. Do not replace them without explicit instruction.  
**Rationale:** The existing material is the foundation for the product.

## D-005 — OpenAI for first text coach (SB-002)
**Status:** Accepted  
**Decision:** Use the OpenAI Chat Completions API from a local Python CLI for natural-language coaching; read `OPENAI_API_KEY` and optional `OPENAI_MODEL` from the environment only.  
**Rationale:** Smallest path to useful follow-ups while keeping automated tests offline via mocks.  
**Consequence:** Live coaching requires a network and API key; tests must not call the API.

## How to amend decisions
Add a new numbered decision with status, decision, rationale, and consequences. Do not silently rewrite an accepted decision; mark it superseded if the direction changes.
