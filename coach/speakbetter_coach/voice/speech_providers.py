"""OpenAI STT/TTS construction from environment (voice quality + latency knobs)."""

import os

from livekit.plugins import openai


def _float_env(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def create_openai_stt() -> openai.STT:
    model = os.environ.get("OPENAI_STT_MODEL", "gpt-4o-mini-transcribe")
    language = os.environ.get("OPENAI_STT_LANGUAGE")
    if language:
        return openai.STT(model=model, language=language)
    return openai.STT(model=model)


def create_openai_tts() -> openai.TTS:
    voice = os.environ.get("OPENAI_TTS_VOICE", "ash")
    model = os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    speed = _float_env("OPENAI_TTS_SPEED", 1.0)
    instructions = os.environ.get(
        "OPENAI_TTS_INSTRUCTIONS",
        "Speak as a warm, calm executive coach. Natural pacing, clear emphasis, "
        "no robotic list-reading.",
    )
    return openai.TTS(
        model=model,
        voice=voice,
        speed=speed,
        instructions=instructions,
    )
