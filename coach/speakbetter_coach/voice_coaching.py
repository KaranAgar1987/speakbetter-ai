"""Voice-specific coaching context (latency + adaptive CART)."""

from __future__ import annotations

import os
from typing import Iterable

from speakbetter_coach.session import STEP_ORDER, Session, Step

_SCENARIO_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("interview practice", ("interview", "hiring", "recruiter", "panel")),
    ("presentation or talk", ("presentation", "keynote", "slide", "audience")),
    ("workplace conversation", ("manager", "one on one", "1:1", "feedback meeting")),
    ("sales or client call", ("client", "prospect", "deal", "sales call")),
)


def infer_communication_scenario(text: str, drafts: dict[str, str]) -> str | None:
    blob = f"{text} {' '.join(drafts.values())}".lower()
    for label, keywords in _SCENARIO_PATTERNS:
        if any(k in blob for k in keywords):
            return label
    return None


def summarize_step_drafts(drafts: dict[str, str], current: Step | None) -> str:
    lines: list[str] = []
    for step in STEP_ORDER:
        chunk = drafts.get(step.value, "").strip()
        if not chunk:
            continue
        preview = chunk if len(chunk) <= 200 else chunk[:197] + "..."
        lines.append(f"{step.label}: {preview}")
    if current and current in STEP_ORDER and not drafts.get(current.value):
        lines.append(f"(User is still drafting {current.label}.)")
    return "\n".join(lines) if lines else "(No story draft captured yet.)"


def last_assistant_line(messages: Iterable[dict[str, str]]) -> str:
    for message in reversed(list(messages)):
        if message.get("role") == "assistant":
            return (message.get("content") or "").strip()
    return ""


def trim_voice_messages(
    messages: list[dict[str, str]],
    *,
    max_turns: int | None = None,
) -> list[dict[str, str]]:
    """Keep system prompt + recent turns to reduce LLM latency."""
    if max_turns is None:
        max_turns = int(os.environ.get("VOICE_LLM_MAX_TURNS", "8"))
    system = [m for m in messages if m.get("role") == "system"]
    dialogue = [m for m in messages if m.get("role") != "system"]
    cap = max(2, max_turns * 2)
    return system + dialogue[-cap:]


def build_voice_turn_extra(
    session: Session,
    user_text: str,
    step_instruction: str,
) -> str:
    step = session.current_cart_step()
    parts = [
        f"[Current CART step: {step.label if step else 'Context'}. {step_instruction}]",
        f"[Story draft so far:\n{summarize_step_drafts(session.step_drafts, step)}]",
    ]
    scenario = infer_communication_scenario(user_text, session.step_drafts)
    if scenario:
        parts.append(f"[User scenario: {scenario}. Adapt examples and follow-ups accordingly.]")
    prior = last_assistant_line(session.chat_messages)
    if prior:
        snippet = prior if len(prior) <= 240 else prior[:237] + "..."
        parts.append(
            "[Do not repeat or paraphrase the same question or advice as your last reply. "
            f"Last coach line: {snippet}]"
        )
    parts.append(
        "[Voice: 2–4 short spoken sentences. One follow-up only if this step needs more detail.]"
    )
    return "\n\n".join(parts)


def spoken_reply_limit() -> int:
    return int(os.environ.get("VOICE_LLM_MAX_TOKENS", "220"))
