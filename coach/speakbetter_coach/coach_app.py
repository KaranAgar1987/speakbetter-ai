"""Shared CART coach session logic (CLI and voice)."""

from pathlib import Path

from speakbetter_coach.examples import resolve_example_command
from speakbetter_coach.guardrails import filter_forbidden_phrases
from speakbetter_coach.prompts import (
    VOICE_CONVERSATIONAL_APPENDIX,
    assembly_instruction,
    build_system_message,
    step_instruction,
)
from speakbetter_coach.session import Session, Step
from speakbetter_coach.story_save import (
    format_story_markdown,
    is_save_command,
    parse_save_command,
    story_is_complete,
    write_story_file,
)
from speakbetter_coach.llm import ChatCompleter

VOICE_COACHING_TRIGGERS = (
    "hint",
    "help",
    "coach",
    "feedback",
    "suggest",
    "improve",
    "what do you think",
    "example",
)

# Short check-ins (not story content). Avoid coaching trigger words in spoken replies (speaker echo).
VOICE_CHECKIN_PHRASES = (
    "can you hear",
    "do you hear",
    "are you listening",
    "can you listen",
    "hear me",
    "testing",
    "test test",
)


class CoachApp:
    def __init__(
        self,
        completer: ChatCompleter,
        cart_markdown: str,
        cwd: Path | None = None,
        voice_mode: bool = False,
        voice_conversational: bool | None = None,
    ) -> None:
        self.completer = completer
        self.system_message = build_system_message(cart_markdown)
        self.session = Session()
        self.cwd = cwd or Path.cwd()
        self.voice_mode = voice_mode
        if voice_conversational is None:
            voice_conversational = voice_mode
        self.voice_conversational = voice_conversational

    def start(self) -> str:
        self.session.reset()
        system = self.system_message
        if self.voice_mode and self.voice_conversational:
            system = f"{system}\n\n{VOICE_CONVERSATIONAL_APPENDIX}"
        self.session.chat_messages = [
            {"role": "system", "content": system},
        ]
        self.session.advance_step()  # WELCOME -> CONTEXT
        opening = (
            "Let's build your story step by step, starting with Context. "
            "Where were you, who was involved, and what did you want to achieve?"
        )
        self._append_assistant(opening)
        return opening

    def _append_assistant(self, content: str) -> str:
        safe = filter_forbidden_phrases(content)
        self.session.chat_messages.append({"role": "assistant", "content": safe})
        return safe

    def _coach_reply(self, user_text: str) -> str:
        step = self.session.current_cart_step()
        extra = ""
        if step:
            extra = f"\n\n[Current CART step: {step.label}. {step_instruction(step)}]"
        self.session.chat_messages.append(
            {"role": "user", "content": user_text + extra}
        )
        reply = self.completer.complete(self.session.chat_messages)
        return self._append_assistant(reply)

    def _user_wants_coaching(self, lower: str) -> bool:
        return any(trigger in lower for trigger in VOICE_COACHING_TRIGGERS)

    def _voice_wants_step_hint(self, lower: str) -> bool:
        text = lower.strip().rstrip(".,!?")
        if text in ("hint", "coach", "help"):
            return True
        if text.startswith(("hint ", "coach ", "help ")):
            return True
        return any(p in text for p in ("give me a hint", "need a hint", "coaching please"))

    def _is_voice_checkin(self, lower: str) -> bool:
        text = lower.strip().rstrip(".,!?")
        if len(text) > 80:
            return False
        if text in ("hello", "hi", "hey", "hi there"):
            return True
        return any(p in lower for p in VOICE_CHECKIN_PHRASES)

    def _voice_checkin_reply(self) -> str:
        step = self.session.current_cart_step()
        label = step.label if step else "Context"
        return (
            f"Yes, I hear you. We're on {label}. "
            "Tell me your story for this step, say next when you're done, or say coach for help."
        )

    def _voice_story_ack(self, raw: str) -> str:
        snippet = raw.strip()
        if len(snippet) > 55:
            snippet = snippet[:52] + "..."
        return (
            f"Got it — {snippet}. Say next when you're ready, or say coach for help on this step."
        )

    def handle_line(self, line: str) -> tuple[str, bool]:
        """Return (output, should_exit)."""
        raw = line.strip()
        if not raw:
            return "", False

        lower = raw.lower()
        if lower in ("quit", "exit", "q"):
            return "Goodbye. Your story draft is saved in this session until you quit.", True

        if lower == "restart":
            text = self.start()
            return "Session restarted.\n\n" + text, False

        if lower == "hint" or (self.voice_mode and self._voice_wants_step_hint(lower)):
            return self.session.hint_text(), False

        if lower.startswith("example"):
            parts = raw.split()[1:]
            return resolve_example_command(parts) or "", False

        if is_save_command(raw):
            return self._handle_save(raw), False

        if lower == "next":
            if self.session.step == Step.ASSEMBLE:
                return (
                    "Story assembly is already complete. Say restart for a new story.",
                    False,
                )
            if self.session.step not in (
                Step.CONTEXT,
                Step.ADVERSITY,
                Step.RESOLUTION,
                Step.TAKEAWAY,
            ):
                return "Share your Context first, then say next to move on.", False
            self.session.advance_step()
            if self.session.step == Step.ASSEMBLE:
                return self._assemble(), False
            label = self.session.step.label
            prompt = self.session.hint_text()
            msg = f"Moving to {label}.\n\n{prompt}"
            self._append_assistant(msg)
            return msg, False

        if self.session.step in (
            Step.CONTEXT,
            Step.ADVERSITY,
            Step.RESOLUTION,
            Step.TAKEAWAY,
        ):
            if self.voice_mode and self._is_voice_checkin(lower):
                reply = self._voice_checkin_reply()
                self._append_assistant(reply)
                return reply, False

            self.session.record_step_content(raw)
            use_efficient_ack = (
                self.voice_mode
                and not self.voice_conversational
                and not self._user_wants_coaching(lower)
            )
            if use_efficient_ack:
                reply = self._voice_story_ack(raw)
                self._append_assistant(reply)
                return reply, False
            reply = self._coach_reply(raw)
            return reply, False

        return self.session.hint_text(), False

    def _handle_save(self, raw: str) -> str:
        command = parse_save_command(raw, self.cwd)
        if command is None:
            return (
                "Could not parse save command. Try: save, save my-story.md, "
                "or save force to overwrite."
            )
        if not story_is_complete(self.session.step_drafts, self.session.step):
            return (
                "Your story is not ready to save yet. Complete Context, Adversity, "
                "Resolution, and Takeaway, then say next after Takeaway to finish assembly."
            )
        markdown = format_story_markdown(self.session.step_drafts)
        ok, message = write_story_file(command, markdown)
        if ok:
            return message
        return f"Save failed. {message}"

    def _assemble(self) -> str:
        instruction = assembly_instruction(self.session.step_drafts)
        self.session.chat_messages.append({"role": "user", "content": instruction})
        reply = self.completer.complete(self.session.chat_messages)
        reply = self._append_assistant(reply)
        self.session.step = Step.DONE
        prefix = "Your CART draft.\n\n" if self.voice_mode else "\n--- Your CART draft ---\n\n"
        return prefix + reply
