"""CART session state."""

from dataclasses import dataclass, field
from enum import Enum


class Step(str, Enum):
    WELCOME = "welcome"
    CONTEXT = "context"
    ADVERSITY = "adversity"
    RESOLUTION = "resolution"
    TAKEAWAY = "takeaway"
    ASSEMBLE = "assemble"
    DONE = "done"

    @property
    def label(self) -> str:
        return {
            Step.WELCOME: "Welcome",
            Step.CONTEXT: "Context",
            Step.ADVERSITY: "Adversity",
            Step.RESOLUTION: "Resolution",
            Step.TAKEAWAY: "Takeaway",
            Step.ASSEMBLE: "Assemble",
            Step.DONE: "Done",
        }[self]


STEP_ORDER: list[Step] = [
    Step.CONTEXT,
    Step.ADVERSITY,
    Step.RESOLUTION,
    Step.TAKEAWAY,
]

HINTS: dict[Step, str] = {
    Step.CONTEXT: "Set the scene in one or two sentences. Who is this about and what did they want?",
    Step.ADVERSITY: "What was hard or unclear? What was at stake emotionally? Where did the pressure show up?",
    Step.RESOLUTION: "What action or decision changed things? What happened in the end?",
    Step.TAKEAWAY: "Finish with what you learned, not what the listener 'should' do.",
}


@dataclass
class Session:
    step: Step = Step.WELCOME
    step_drafts: dict[str, str] = field(default_factory=dict)
    chat_messages: list[dict[str, str]] = field(default_factory=list)

    def reset(self) -> None:
        self.step = Step.WELCOME
        self.step_drafts.clear()
        self.chat_messages.clear()

    def current_cart_step(self) -> Step | None:
        if self.step in STEP_ORDER:
            return self.step
        return None

    def record_step_content(self, text: str) -> None:
        if self.step in STEP_ORDER:
            prev = self.step_drafts.get(self.step.value, "")
            self.step_drafts[self.step.value] = (
                f"{prev}\n{text}".strip() if prev else text.strip()
            )

    def advance_step(self) -> Step:
        if self.step == Step.WELCOME:
            self.step = Step.CONTEXT
            return self.step
        if self.step in STEP_ORDER:
            idx = STEP_ORDER.index(self.step)
            if idx + 1 < len(STEP_ORDER):
                self.step = STEP_ORDER[idx + 1]
            else:
                self.step = Step.ASSEMBLE
            return self.step
        return self.step

    def hint_text(self) -> str:
        if self.step in HINTS:
            return f"[{self.step.label}] {HINTS[self.step]}"
        if self.step == Step.WELCOME:
            return "Share a professional situation (meeting, update, interview, sales call) you want to turn into a short story."
        return "Type your story content, or use: hint | example | next | restart | quit"
