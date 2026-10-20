"""Issue short-lived LiveKit room tokens (server-side only)."""

from livekit import api

from speakbetter_coach.voice.config import LiveKitConfig


def create_participant_token(
    config: LiveKitConfig,
    identity: str = "speakbetter-user",
    name: str = "SpeakBetter user",
) -> str:
    """Return a JWT for the browser; never include the API secret in the response."""
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
    )
    return token.to_jwt()
