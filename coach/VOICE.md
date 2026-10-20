# SpeakBetter AI — LiveKit voice prototype (SB-006)

Local browser voice session for the **same CART coach** as the text CLI (`CoachApp` + `knowledge/cart.md`). Not deployed to cloud in this milestone.

## Architecture

| Component | Role |
|-----------|------|
| **LiveKit server** | WebRTC room (local Docker or LiveKit Cloud) |
| **`speakbetter_coach.voice.token_server`** | Serves `voice_web/index.html` and `GET /token` (JWT only; **API secret stays server-side**) |
| **`speakbetter_coach.voice.agent`** | LiveKit worker: OpenAI **STT** + **TTS**, VAD/endpointing, routes final user text through **`CoachApp` (voice_mode)** |
| **OpenAI Chat Completions** | Same as CLI when user asks for coaching (`hint`, feedback, etc.) |
| **Text CLI** | Unchanged: `PYTHONPATH=coach python -m speakbetter_coach` |

**Charges:** LiveKit (if using Cloud), OpenAI (STT, TTS, and chat when coaching runs). You control keys and usage.

## Environment variables

Copy `coach/.env.example` → `coach/.env`. Required for voice:

| Variable | Purpose |
|----------|---------|
| `LIVEKIT_URL` | e.g. `ws://localhost:7880` (dev server) or `wss://…livekit.cloud` |
| `LIVEKIT_API_KEY` | LiveKit project key |
| `LIVEKIT_API_SECRET` | **Server only** — used for tokens and agent worker |
| `OPENAI_API_KEY` | STT, TTS, and CART coaching LLM |
| `OPENAI_MODEL` | Optional; chat model (default `gpt-4o-mini`) |
| `LIVEKIT_ROOM` | Optional; default `speakbetter-cart` |
| `OPENAI_TTS_VOICE` | Optional; default `ash` |
| `VOICE_MIN_ENDPOINTING_DELAY` | Optional; default `0.8` seconds |
| `VOICE_MAX_ENDPOINTING_DELAY` | Optional; default `6.0` seconds |
| `VOICE_HTTP_PORT` | Optional; token/UI server port (default `8787`) |

## macOS setup (repository root)

```bash
python3 -m venv coach/.venv
source coach/.venv/bin/activate
pip install -r coach/requirements-voice.txt
cp coach/.env.example coach/.env
# Edit coach/.env with your keys (never commit).
```

### 1. Start LiveKit (local dev)

```bash
docker run --rm -p 7880:7880 -p 7881:7881 \
  -e LIVEKIT_KEYS="devkey: secret" \
  livekit/livekit-server --dev
```

Example `.env` for local dev:

```bash
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
```

### 2. Token + browser UI

```bash
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach.voice.token_server
```

Open http://127.0.0.1:8787/ → **Connect** → allow microphone.

### 3. Voice agent worker

In another terminal:

```bash
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach.voice.agent dev
```

The agent loads `coach/.env` in **`main()`** before the LiveKit worker starts (the worker needs `LIVEKIT_URL` immediately; loading only inside a job entrypoint is too late).

## Voice behavior (turn-taking)

- VAD + min/max endpointing delays reduce cutting off mid-thought (not perfect; verify in a real session).
- **Voice mode (default):** **conversational** — each turn uses the same CART coach LLM as the text CLI (brief spoken replies). Set `VOICE_CONVERSATIONAL=false` for the older ack-only mode (saves API calls).
- Spoken/text commands: `next`, `hint`, `example`, `save`, `restart`, `quit` (same logic as CLI where applicable).

## Text CLI (unchanged)

```bash
PYTHONPATH=coach python -m speakbetter_coach
```

## Offline tests

```bash
PYTHONPATH=coach python -m unittest discover -s coach/tests -v
```

Voice config/token tests mock secrets; they do not start LiveKit or call OpenAI.

## Troubleshooting

| Issue | Check |
|-------|--------|
| `Missing environment variables for voice` | `coach/.env` and auto-load; see `coach/README.md` |
| Token 503 | LiveKit vars missing in token server process |
| No agent audio | Agent worker running? Room name matches? OpenAI key valid? |
| Browser cannot connect | `LIVEKIT_URL` reachable from browser (use `ws://localhost:7880` for local Docker) |

## Limitations (SB-006)

- Local prototype only; no production auth or cloud deploy.
- End-to-end voice **not verified** in CI without your LiveKit + OpenAI credentials.
- Turn-taking tuning is configurable but not guaranteed for all accents/noise.
