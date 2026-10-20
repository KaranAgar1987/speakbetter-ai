"""Issue short-lived LiveKit room tokens (server-side only)."""

import os

from livekit import api

from speakbetter_coach.voice.config import LiveKitConfig


def livekit_agent_name() -> str:
    """Empty name = default worker; must match WorkerOptions.agent_name."""
    return os.environ.get("LIVEKIT_AGENT_NAME", "")


def create_participant_token(
    config: LiveKitConfig,
    identity: str = "speakbetter-user",
    name: str = "SpeakBetter user",
) -> str:
    """Return a JWT for the browser; never include the API secret in the response."""
    agent_name = livekit_agent_name()
    room_config = api.RoomConfiguration(
        name=config.room,
        agents=[api.RoomAgentDispatch(agent_name=agent_name)],
    )
    token = (
        api.AccessToken(config.api_key, config.api_secret)
        .with_identity(identity)
        .with_name(name)
        .with_grants(
            api.VideoGrants(
                room_join=True,
                room=config.room,
                can_publish=True,
                can_subscribe=True,
            )
        )
        .with_room_config(room_config)
    )
    return token.to_jwt()
