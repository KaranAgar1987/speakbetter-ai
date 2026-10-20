"""OpenAI chat completion wrapper (mockable for tests)."""

import os
from typing import Protocol


class ChatCompleter(Protocol):
    def complete(self, messages: list[dict[str, str]]) -> str: ...


class OpenAIChatCompleter:
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy coach/.env.example to .env and add your key."
            )

    def complete(self, messages: list[dict[str, str]]) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.6,
        )
        content = response.choices[0].message.content
        return (content or "").strip()


class ScriptCompleter:
    """Offline stub for tests: echoes a safe coaching line."""

    def complete(self, messages: list[dict[str, str]]) -> str:
        last_user = next(
            (m["content"] for m in reversed(messages) if m.get("role") == "user"),
            "",
        )
        return (
            "Thanks for sharing that. What felt most uncertain or at stake for you "
            f"in that moment? (You said: {last_user[:80]}…)"
        )
