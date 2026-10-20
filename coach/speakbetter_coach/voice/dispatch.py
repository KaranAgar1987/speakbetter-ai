"""Ensure the voice worker is dispatched into the coaching room."""

import asyncio
import logging

from livekit import api

from speakbetter_coach.voice.config import LiveKitConfig
from speakbetter_coach.voice.tokens import livekit_agent_name

logger = logging.getLogger(__name__)

_AGENT_KIND = 4  # livekit.protocol.models.ParticipantInfo.Kind.AGENT


def _http_url(ws_url: str) -> str:
    return ws_url.replace("ws://", "http://").replace("wss://", "https://")


def _room_has_agent(participants) -> bool:
    for participant in participants:
        if getattr(participant, "kind", None) == _AGENT_KIND:
            return True
        if participant.identity.startswith("agent-"):
            return True
    return False


async def _ensure_async(config: LiveKitConfig) -> None:
    lk = api.LiveKitAPI(_http_url(config.url), config.api_key, config.api_secret)
    try:
        listed = await lk.room.list_participants(
            api.ListParticipantsRequest(room=config.room)
        )
        if _room_has_agent(listed.participants):
            return
        req = api.CreateAgentDispatchRequest()
        req.agent_name = livekit_agent_name()
        req.room = config.room
        await lk.agent_dispatch.create_dispatch(req)
        logger.info("requested agent dispatch for room %s", config.room)
    except Exception:
        logger.exception("could not ensure agent dispatch for room %s", config.room)
    finally:
        await lk.aclose()


def ensure_agent_dispatch(config: LiveKitConfig) -> None:
    """Dispatch the registered worker if the room has no agent yet."""
    asyncio.run(_ensure_async(config))
