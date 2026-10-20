# SpeakBetter AI — Project State

**Last updated:** 2026-10-20  
**Coordination branch:** `feature/voice-coach-improvements`  
**Current milestone:** SB-007 — voice latency, adaptive coaching, and speech quality improvements.

## Product direction
CART coach from `knowledge/cart.md`. **Text CLI** remains the primary minimal product; **voice** is an optional local LiveKit prototype.

## Verified state after SB-007
- **Branch:** `feature/voice-coach-improvements` (not merged to `main`).
- **Text CLI:** unchanged — `PYTHONPATH=coach python -m speakbetter_coach`.
- **Voice:** SB-006 stack plus SB-007 tuning — per-turn timing logs, trimmed LLM context (`VOICE_LLM_MAX_TURNS`), capped reply tokens (`VOICE_LLM_MAX_TOKENS`), adaptive voice turn metadata (`voice_coaching.py`), configurable OpenAI STT/TTS (`speech_providers.py`), agent dispatch on `/token`.
- **Offline tests:** **50** passed (`PYTHONPATH=coach python -m unittest discover -s coach/tests -v`) with voice dependencies installed.
- **Live end-to-end voice (listen + speak):** **Not tested** in this Cursor run (no browser microphone session or subjective audio review). Local LiveKit Docker and token server HTTP health were reachable during the run.
- `knowledge/cart.md` and `research/philipp-humm/` unchanged.

## Prior milestones
- SB-006: LiveKit voice prototype on `ai-coordination` (merged to `main` via PR #1).
- SB-005: smoke-test hardening + `SMOKE-TEST.md`

## Next milestone
Owner live voice smoke test on `feature/voice-coach-improvements`; merge PR when satisfied.
