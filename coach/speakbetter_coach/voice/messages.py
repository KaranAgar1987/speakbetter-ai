"""Helpers for LiveKit agent message objects."""


def user_message_text(message) -> str:
    """Extract user text from a LiveKit ``ChatMessage`` (SDK versions differ)."""
    content = getattr(message, "text_content", None)
    if callable(content):
        return (content() or "").strip()
    if isinstance(content, str):
        return content.strip()
    return str(message).strip()
