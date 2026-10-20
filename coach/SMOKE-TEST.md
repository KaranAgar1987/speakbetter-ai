# CART CLI — manual smoke test (macOS)

Use this checklist for the first **live** validation with your own OpenAI API key.  
**API usage is billed to your OpenAI account.** Do not paste your key into chat, commits, or this file.

## Prerequisites

- macOS with Python 3.10+
- Repository cloned; terminal at **repository root** (`speakbetter-ai/`)

## One-time setup

```bash
python3 -m venv coach/.venv
source coach/.venv/bin/activate
pip install -r coach/requirements.txt
cp coach/.env.example coach/.env
```

Edit `coach/.env` locally and set `OPENAI_API_KEY` to your key. The CLI loads this file automatically (no `source` needed).

## Launch

```bash
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach
```

| Check | Expected |
|-------|----------|
| Missing `OPENAI_API_KEY` (rename `.env` temporarily) | Clean error on stderr; exit code 1; **no** Python traceback |
| With valid key | Welcome text and Context opening question |

## Session flow (live API)

Work through one short workplace story:

| Step | Action | Expected |
|------|--------|----------|
| 1 | Type a Context sentence | Coach reply; no pass/fail or score language |
| 2 | `next` | Moves to Adversity |
| 3 | Adversity sentence, then `next` | Resolution step |
| 4 | Resolution sentence, then `next` | Takeaway step |
| 5 | Takeaway sentence, then `next` | Assembled draft (API call); session complete |
| 6 | `save` | Message **Story saved to** … with absolute path |
| 7 | Open the Markdown file | Four sections: Context, Adversity, Resolution, Takeaway; your text only |
| 8 | `save` again (same path) | **Save failed.** file exists message; file unchanged |
| 9 | `save --force` | Overwrites file; success message |
| 10 | `quit` | Exits cleanly |

## Command edge cases

| Input | Expected |
|-------|------------|
| `saved my notes` during Context | Treated as story text (not the save command) |
| `save` before assembly completes | Not ready to save message |
| `hint` | Current step prompt |
| `example dentist` | SRC-001 labeled example |
| `restart` | New session from Context |

## Offline automation (no API key)

```bash
PYTHONPATH=coach python -m unittest discover -s coach/tests -v
```

All tests should pass before you rely on the live checklist above.

## Not in scope for this smoke test

- Voice, video, web UI, database
- Merging to `main`
