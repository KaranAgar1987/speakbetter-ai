"""LiveKit and voice provider configuration (no secrets in logs)."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LiveKitConfig:
    url: str
    api_key: str
    api_secret: str
    room: str
    openai_api_key: str
    openai_model: str


REQUIRED_LIVEKIT_VARS = ("LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET")


def load_livekit_config() -> LiveKitConfig:
    missing = [name for name in REQUIRED_LIVEKIT_VARS if not os.environ.get(name)]
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        missing.append("OPENAI_API_KEY")
    if missing:
        raise RuntimeError(
            "Missing environment variables for voice: "
            + ", ".join(missing)
            + ". See coach/.env.example and coach/VOICE.md."
        )
    return LiveKitConfig(
        url=os.environ["LIVEKIT_URL"].rstrip("/"),
        api_key=os.environ["LIVEKIT_API_KEY"],
        api_secret=os.environ["LIVEKIT_API_SECRET"],
        room=os.environ.get("LIVEKIT_ROOM", "speakbetter-cart"),
        openai_api_key=openai_key,
        openai_model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    )
