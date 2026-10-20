# Cursor Report

**Task ID:** SB-007  
**Status:** Complete  
**Branch:** `feature/voice-coach-improvements`  
**Commit:** `a8bd69e`  
**Date:** 2026-10-20

## Summary

Improved the integrated LiveKit voice path across **latency instrumentation**, **adaptive CART coaching context**, **TTS/STT configuration**, and **offline regression tests**—without a second coach brain or changes to `knowledge/cart.md`. Text CLI preserved.

## Baseline diagnosis (Phase 1)

| Stage | Evidence |
|-------|----------|
| Endpointing | Defaults `VOICE_MIN_ENDPOINTING_DELAY=0.8s`, `VOICE_MAX_ENDPOINTING_DELAY=6.0s` (unchanged; still owner-tunable). |
| STT → coach | Agent logs `user turn:` when STT completes; prior sessions showed multi-second `transcript_delay` from LiveKit/OpenAI (not re-measured live this run). |
| Coach / LLM | Full `knowledge/cart.md` (~12KB) remains in system prompt every turn; long chat history increased token load. **Hypothesis (structural):** reply latency dominated by chat completion + TTS after STT, not Python glue code. |
| TTS / playback | `session.say()` + optional `wait_for_playout`; LiveKit logs `flush audio emitter due to slow audio generation` under load in prior sessions. |

**Measurement method (offline):** `PYTHONPATH=coach python coach/scripts/voice_latency_baseline.py` — ScriptCompleter, no network; after 10 turns, `handle_line` avg **0.03 ms** (Python-only; not representative of OpenAI latency).

**Live before/after:** **Not obtained** — no controlled A/B voice session in this environment.

## Changes by area

### Latency (Phase 2)
- `trim_voice_messages()` + `VOICE_LLM_MAX_TURNS` (default 8) limit dialogue sent to the chat model.
- `VOICE_LLM_MAX_TOKENS` (default 220) caps generation length for spoken replies.
- `TurnTimer` logs `voice turn timings_ms` (`stt_done`, `coach_done`, `tts_scheduled`, `playout_done`) in the agent worker.
- `asyncio.to_thread` retained for `handle_line` so the agent event loop is not blocked.

### Adaptive coaching (Phase 3)
- `build_voice_turn_extra()` adds step focus, draft summary, inferred scenario (interview, presentation, etc.), anti-repeat of last coach line, and spoken-length guidance.
- `VOICE_CONVERSATIONAL_APPENDIX` updated for scenario adaptation and no redundant questions.
- Still routes through **`CoachApp`** and explicit commands (`next`, `hint`, `save`, …).

### Voice quality (Phase 4)
- `create_openai_tts()` — `gpt-4o-mini-tts`, `OPENAI_TTS_VOICE`, `OPENAI_TTS_SPEED`, `OPENAI_TTS_INSTRUCTIONS` (warm coach delivery).
- `create_openai_stt()` — `OPENAI_STT_MODEL` (default `gpt-4o-mini-transcribe`).
- **Listening verification:** **Not performed** in this run (configuration change only).

### Reliability / testing (Phase 5)
- New tests: `test_voice_coaching.py`, `test_voice_timing.py`.
- Existing dispatch, tokens, coach mode, and CLI tests preserved.

## Files changed (high level)

| Path | Purpose |
|------|---------|
| `coach/speakbetter_coach/voice_coaching.py` | Trim context, adaptive turn metadata |
| `coach/speakbetter_coach/voice/timing.py` | Per-turn timing |
| `coach/speakbetter_coach/voice/speech_providers.py` | STT/TTS from env |
| `coach/speakbetter_coach/voice/agent.py` | Timing + providers |
| `coach/speakbetter_coach/coach_app.py` | Voice-aware `_coach_reply` |
| `coach/speakbetter_coach/llm.py` | Optional `max_tokens` |
| `coach/speakbetter_coach/prompts.py` | Stronger voice appendix |
| `coach/scripts/voice_latency_baseline.py` | Offline baseline script |
| `coach/VOICE.md`, `coach/.env.example` | SB-007 env docs |
| `coach/tests/test_voice_*.py` | Regression coverage |
| `coordination/*` | Handoff |

## Validation

| Check | Result |
|-------|--------|
| `PYTHONPATH=coach python -m unittest discover -s coach/tests -v` | **OK — 50 tests** |
| `PYTHONPATH=coach python coach/scripts/voice_latency_baseline.py` | **OK** (avg 0.03 ms, offline stub) |
| LiveKit Docker `:7880` | **Reachable** (`Up` during run) |
| Token server `GET /health` | **200** during run |
| Browser microphone → spoken coach reply (subjective) | **Not tested** |

## macOS owner test steps

```bash
# Terminal 1 — LiveKit
docker run --rm -p 7880:7880 -p 7881:7881 -e LIVEKIT_KEYS="devkey: secret" livekit/livekit-server --dev

# Terminal 2 — token UI
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach.voice.token_server

# Terminal 3 — agent
source coach/.venv/bin/activate
PYTHONPATH=coach python -m speakbetter_coach.voice.agent dev
```

Open http://127.0.0.1:8787/ → Disconnect/Connect → speak; watch agent logs for `voice turn timings_ms`.

## Limitations and risks

- Latency improvements are **partial** without live A/B; full CART markdown still in every system prompt.
- Anti-repeat and scenario hints depend on LLM following bracketed metadata.
- TTS quality claims require owner listening tests.

## Git

- **Push status:** Verified after `git push origin feature/voice-coach-improvements`
- **Commit URL:** https://github.com/KaranAgar1987/speakbetter-ai/commit/a8bd69e343b7e6fc12dc20a22697cc962296acf7

## Recommended next step

Owner: live session on `feature/voice-coach-improvements`, compare `voice turn timings_ms` and subjective naturalness; open PR to `main` if satisfied.
