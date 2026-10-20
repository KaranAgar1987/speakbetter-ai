# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `ai-coordination`  
**Current milestone:** SB-006 — local LiveKit voice prototype alongside text CLI.

## Product direction
CART coach from `knowledge/cart.md`. **Text CLI** remains the primary minimal product; **voice** is an optional local prototype.

## Verified state after SB-006
- Repository: `KaranAgar1987/speakbetter-ai` on `ai-coordination` (not merged to `main`).
- **Text CLI:** `PYTHONPATH=coach python -m speakbetter_coach` — unchanged command; logic in `speakbetter_coach/coach_app.py`.
- **Voice:** `coach/VOICE.md`, `coach/requirements-voice.txt`, `coach/voice_web/index.html`, `speakbetter_coach/voice/agent.py`, `speakbetter_coach/voice/token_server.py`.
- **Integration:** `CoachApp(voice_mode=True)` — records story text; chat API only on coaching triggers or assembly/commands; OpenAI STT/TTS via LiveKit plugins.
- **Secrets:** Browser gets JWT from `GET /token`; `LIVEKIT_API_SECRET` not sent to client.
- **Offline tests:** **38** passed (`PYTHONPATH=coach python -m unittest discover -s coach/tests -v`) with voice dependencies installed.
- **Live end-to-end voice:** **Not tested** in Cursor agent (no LiveKit/OpenAI session run). Owner validates per `coach/VOICE.md`.
- `knowledge/cart.md` and `research/philipp-humm/` unchanged.

## Prior milestones
- SB-005: smoke-test hardening + `SMOKE-TEST.md`
- SB-004: `save` command
- SB-003: auto `.env` load

## Next milestone
Owner live voice smoke test; ChatGPT defines SB-007 in `next-task.md`.
