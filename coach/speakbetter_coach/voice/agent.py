"""LiveKit voice worker — routes speech through the existing CART CoachApp."""

import logging
import os

from livekit.agents import (
    Agent,
    AgentSession,
    AutoSubscribe,
    JobContext,
    JobProcess,
    WorkerOptions,
    cli,
)
from livekit.plugins import openai, silero

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.knowledge import find_repo_root, load_cart_markdown
from speakbetter_coach.llm import OpenAIChatCompleter

logger = logging.getLogger("speakbetter-cart-voice")


class CARTVoiceAgent(Agent):
    """STT/TTS shell; coaching text comes from CoachApp (same as CLI)."""

    def __init__(self, coach: CoachApp) -> None:
        self.coach = coach
        super().__init__(
            instructions=coach.system_message,
            stt=openai.STT(),
            tts=openai.TTS(voice=os.environ.get("OPENAI_TTS_VOICE", "ash")),
            turn_detection="vad",
            min_endpointing_delay=float(os.environ.get("VOICE_MIN_ENDPOINTING_DELAY", "0.8")),
            max_endpointing_delay=float(os.environ.get("VOICE_MAX_ENDPOINTING_DELAY", "6.0")),
            allow_interruptions=True,
            llm=None,
        )

    async def on_enter(self) -> None:
        opening = self.coach.start()
        await self.session.say(opening, allow_interruptions=True)

    async def on_user_turn_completed(self, turn_ctx, new_message) -> None:
        text = new_message.text_content() or ""
        reply, should_exit = self.coach.handle_line(text)
        if reply:
            await self.session.say(reply, allow_interruptions=True)
        if should_exit:
            await self.session.shutdown()


def prewarm(proc: JobProcess) -> None:
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext) -> None:
    load_local_env()
    root = find_repo_root()
    cart = load_cart_markdown(root)
    coach = CoachApp(OpenAIChatCompleter(), cart, voice_mode=True)

    logger.info("connecting to room %s", ctx.room.name)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    await ctx.wait_for_participant()

    session = AgentSession(
        vad=ctx.proc.userdata["vad"],
        min_endpointing_delay=float(os.environ.get("VOICE_MIN_ENDPOINTING_DELAY", "0.8")),
        max_endpointing_delay=float(os.environ.get("VOICE_MAX_ENDPOINTING_DELAY", "6.0")),
    )
    agent = CARTVoiceAgent(coach)
    await session.start(agent=agent, room=ctx.room)


def main() -> None:
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))


if __name__ == "__main__":
    main()
