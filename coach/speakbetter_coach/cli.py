"""Interactive CART coach CLI."""

from pathlib import Path

from speakbetter_coach.examples import resolve_example_command
from speakbetter_coach.guardrails import filter_forbidden_phrases
from speakbetter_coach.knowledge import find_repo_root, load_cart_markdown
from speakbetter_coach.llm import ChatCompleter
from speakbetter_coach.prompts import (
    assembly_instruction,
    build_system_message,
    step_instruction,
)
from speakbetter_coach.session import Session, Step
from speakbetter_coach.story_save import (
    format_story_markdown,
    parse_save_command,
    story_is_complete,
    write_story_file,
)

WELCOME_TEXT = """SpeakBetter AI — CART coach (text)
Context → Adversity → Resolution → Takeaway

Describe a workplace situation you want to turn into a short story.
Commands: hint | example [dentist|a|b|c|d] | next | save [path] | restart | quit
"""


class CoachApp:
    def __init__(
        self,
        completer: ChatCompleter,
        cart_markdown: str,
        cwd: Path | None = None,
    ) -> None:
        self.completer = completer
        self.system_message = build_system_message(cart_markdown)
        self.session = Session()
        self.cwd = cwd or Path.cwd()

    def start(self) -> str:
        self.session.reset()
        self.session.chat_messages = [
            {"role": "system", "content": self.system_message},
        ]
        self.session.advance_step()  # WELCOME -> CONTEXT
        opening = (
            "Let's build your story step by step, starting with **Context**. "
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

        if lower == "hint":
            return self.session.hint_text(), False

        if lower.startswith("example"):
            parts = raw.split()[1:]
            return resolve_example_command(parts) or "", False

        if lower.startswith("save"):
            return self._handle_save(raw), False

        if lower == "next":
            if self.session.step == Step.ASSEMBLE:
                return "Story assembly is already complete. Type restart for a new story.", False
            if self.session.step not in (
                Step.CONTEXT,
                Step.ADVERSITY,
                Step.RESOLUTION,
                Step.TAKEAWAY,
            ):
                return "Share your Context first, then type next to move on.", False
            self.session.advance_step()
            if self.session.step == Step.ASSEMBLE:
                return self._assemble(), False
            label = self.session.step.label
            prompt = self.session.hint_text()
            msg = f"Moving to **{label}**.\n\n{prompt}"
            self._append_assistant(msg)
            return msg, False

        # Natural language: accumulate draft for current step and get coaching
        if self.session.step in (
            Step.CONTEXT,
            Step.ADVERSITY,
            Step.RESOLUTION,
            Step.TAKEAWAY,
        ):
            self.session.record_step_content(raw)
            reply = self._coach_reply(raw)
            return reply, False

        return self.session.hint_text(), False

    def _handle_save(self, raw: str) -> str:
        command = parse_save_command(raw, self.cwd)
        if command is None:
            return "Could not parse save command. Try: save | save my-story.md | save --force"
        if not story_is_complete(self.session.step_drafts, self.session.step):
            return (
                "Your story is not ready to save yet. Complete Context, Adversity, "
                "Resolution, and Takeaway, then type `next` after Takeaway to finish assembly."
            )
        markdown = format_story_markdown(self.session.step_drafts)
        ok, message = write_story_file(command, markdown)
        return message

    def _assemble(self) -> str:
        instruction = assembly_instruction(self.session.step_drafts)
        self.session.chat_messages.append({"role": "user", "content": instruction})
        reply = self.completer.complete(self.session.chat_messages)
        reply = self._append_assistant(reply)
        self.session.step = Step.DONE
        return "\n--- Your CART draft ---\n\n" + reply


def run_interactive(completer: ChatCompleter) -> None:
    root = find_repo_root()
    cart = load_cart_markdown(root)
    app = CoachApp(completer, cart)
    print(WELCOME_TEXT)
    print(app.start())
    print()
    while True:
        try:
            line = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        out, exit_ = app.handle_line(line)
        if out:
            print(f"\nCoach> {out}\n")
        if exit_:
            break
