# SpeakBetter AI — CART text coach (CLI)

Minimal local, text-only coach guided by [`../knowledge/cart.md`](../knowledge/cart.md). No web UI, voice, or database.

## Prerequisites

- Python 3.11+ (3.10+ should work)
- OpenAI API key

## Setup (macOS)

Run these from the **repository root** (`speakbetter-ai/`, the folder that contains `knowledge/cart.md`):

```bash
python3 -m venv coach/.venv
source coach/.venv/bin/activate
pip install -r coach/requirements.txt
cp coach/.env.example coach/.env
```

Edit **`coach/.env`** (do not commit it) and set your OpenAI key:

```bash
OPENAI_API_KEY=your-key-here
OPENAI_MODEL=gpt-4o-mini   # optional
```

Live API calls **incur usage charges** on your OpenAI account. For a full manual checklist, see [`SMOKE-TEST.md`](./SMOKE-TEST.md).

On startup, the CLI **automatically loads** local env files (via `python-dotenv`):

| Priority | Source |
|----------|--------|
| 1 (highest) | Variables already exported in your shell |
| 2 | `coach/.env` |
| 3 | `.env` at the repository root (only keys not set above) |

You do **not** need to `source` the file before launch. Never commit a real `.env`.

## Run

From the repository root (so `knowledge/cart.md` can be found):

```bash
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach
```

If `OPENAI_API_KEY` is missing, the CLI prints a short error and exits (no traceback). Launch from the repository root so `knowledge/cart.md` can be found.

## Session commands

| Command | Action |
|---------|--------|
| `hint` | Coach prompt for the current CART step |
| `example` | List example options |
| `example dentist` | Verified SRC-001 paraphrase (labeled) |
| `example a` … `d` | SpeakBetter AI illustrations (labeled) |
| `next` | Move to the next CART step when ready |
| `save` | Save completed story to `speakbetter-cart-story.md` in the current directory |
| `save my-story.md` | Save to a specific path (relative to current directory) |
| `save --force` | Overwrite the default file if it already exists |
| `save --force path.md` | Overwrite a specific file if it already exists |
| `restart` | New story |
| `quit` | Exit |

After you finish **Takeaway**, type `next` once more to assemble your draft. Then use `save` to write a Markdown file with **Context**, **Adversity**, **Resolution**, and **Takeaway** sections (your words only—no API keys or hidden prompts). Saving does not call the OpenAI API. If the target file exists, the CLI refuses to overwrite unless you pass `--force`.

Type natural-language answers between steps. The coach may ask follow-ups per `cart.md`; use `next` when you are ready to advance.

## Tests (offline)

```bash
cd /path/to/speakbetter-ai
PYTHONPATH=coach python -m unittest discover -s coach/tests -v
```

Tests mock the language model and do not call the network.

## Voice prototype (optional)

LiveKit browser voice uses the same `CoachApp` logic. Install voice dependencies and follow **[VOICE.md](./VOICE.md)**. The text CLI does not require LiveKit.

## Scope

- Does not modify `research/philipp-humm/` or `knowledge/cart.md`.
- Does not show pass/fail scores or validation badges.
