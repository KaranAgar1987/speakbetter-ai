"""LiveKit voice worker — routes speech through the existing CART CoachApp."""

import asyncio
import logging
import os
import sys

from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
)
from livekit.plugins import silero

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.knowledge import find_repo_root, load_cart_markdown
from speakbetter_coach.llm import OpenAIChatCompleter
from speakbetter_coach.voice.config import load_livekit_config
from speakbetter_coach.voice.messages import user_message_text
from speakbetter_coach.voice.speech_providers import create_openai_stt, create_openai_tts
from speakbetter_coach.voice.timing import TurnTimer

logger = logging.getLogger("speakbetter-cart-voice")


def _endpointing_delay(name: str, default: str) -> float:
    return float(os.environ.get(name, default))


def _wait_for_playout_enabled() -> bool:
    return os.environ.get("VOICE_WAIT_FULL_PLAYOUT", "true").lower() in (
        "1",
        "true",
        "yes",
    )


class CARTVoiceAgent(Agent):
    """STT/TTS shell; coaching text comes from CoachApp (same as CLI)."""

    def __init__(self, coach: CoachApp) -> None:
        self.coach = coach
        super().__init__(
            instructions=coach.system_message,
            stt=create_openai_stt(),
            tts=create_openai_tts(),
            turn_detection="vad",
            min_endpointing_delay=_endpointing_delay("VOICE_MIN_ENDPOINTING_DELAY", "0.8"),
            max_endpointing_delay=_endpointing_delay("VOICE_MAX_ENDPOINTING_DELAY", "6.0"),
            allow_interruptions=True,
            llm=None,
        )

    async def on_enter(self) -> None:
        opening = self.coach.start()
        logger.info("speaking opening (%d chars)", len(opening))
        handle = self.session.say(opening, allow_interruptions=True)
        if _wait_for_playout_enabled():
            await handle.wait_for_playout()

    async def on_user_turn_completed(self, turn_ctx, new_message) -> None:
        timer = TurnTimer()
        text = user_message_text(new_message)
        if text:
            logger.info("user turn: %s", text[:200])
        timer.mark("stt_done")
        try:
            reply, should_exit = await asyncio.to_thread(self.coach.handle_line, text)
        except Exception:
            logger.exception("coach handle_line failed")
            reply = (
                "Sorry, I had trouble thinking that through. "
                "Please try again in a moment."
            )
            should_exit = False
        timer.mark("coach_done")
        if reply:
            logger.info("speaking reply (%d chars)", len(reply))
            handle = self.session.say(reply, allow_interruptions=True)
            timer.mark("tts_scheduled")
            if _wait_for_playout_enabled():
                await handle.wait_for_playout()
                timer.mark("playout_done")
            logger.info("voice turn timings_ms=%s", timer.deltas_ms())
        if should_exit:
            await self.session.shutdown()


def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext) -> None:
    load_local_env()
    root = find_repo_root()
    cart = load_cart_markdown(root)
    conversational = os.environ.get("VOICE_CONVERSATIONAL", "true").lower() in (
        "1",
        "true",
        "yes",
    )
    coach = CoachApp(
        OpenAIChatCompleter(),
        cart,
        voice_mode=True,
        voice_conversational=conversational,
    )

    logger.info("connecting to room %s", ctx.room.name)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    await ctx.wait_for_participant()

    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        min_endpointing_delay=_endpointing_delay("VOICE_MIN_ENDPOINTING_DELAY", "0.8"),
        max_endpointing_delay=_endpointing_delay("VOICE_MAX_ENDPOINTING_DELAY", "6.0"),
    )
    agent = CARTVoiceAgent(coach)
    await session.start(agent=agent, room=ctx.room)


def main() -> None:
    # LiveKit's CLI starts the worker (and dev subprocess) before any job entrypoint runs.
    # coach/.env must be loaded here, not only inside entrypoint().
    load_local_env()
    try:
        lk = load_livekit_config()
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        raise SystemExit(1) from err

    agent_name = os.environ.get("LIVEKIT_AGENT_NAME", "")
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
            ws_url=lk.url,
            api_key=lk.api_key,
            api_secret=lk.api_secret,
            agent_name=agent_name,
        )
    )


if __name__ == "__main__":
    main()
