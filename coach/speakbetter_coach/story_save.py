"""Save assembled CART stories to local Markdown files."""

from dataclasses import dataclass
from pathlib import Path

from speakbetter_coach.session import STEP_ORDER, Step

DEFAULT_FILENAME = "speakbetter-cart-story.md"

SECTION_TITLES = {
    Step.CONTEXT: "Context",
    Step.ADVERSITY: "Adversity",
    Step.RESOLUTION: "Resolution",
    Step.TAKEAWAY: "Takeaway",
}


def story_is_complete(step_drafts: dict[str, str], step: Step) -> bool:
    if step != Step.DONE:
        return False
    for cart_step in STEP_ORDER:
        text = step_drafts.get(cart_step.value, "").strip()
        if not text:
            return False
    return True


def format_story_markdown(step_drafts: dict[str, str]) -> str:
    lines = ["# CART story", ""]
    for cart_step in STEP_ORDER:
        title = SECTION_TITLES[cart_step]
        body = step_drafts.get(cart_step.value, "").strip()
        lines.append(f"## {title}")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


@dataclass
class SaveCommand:
    path: Path
    force: bool


def is_save_command(line: str) -> bool:
    """True only when the line is the ``save`` command (not e.g. ``saved`` or ``savings``)."""
    parts = line.strip().split()
    return bool(parts) and parts[0].lower() == "save"


def parse_save_command(line: str, cwd: Path | None = None) -> SaveCommand | None:
    """Parse ``save``, ``save --force``, ``save path.md``, or ``save --force path.md``."""
    if not is_save_command(line):
        return None
    parts = line.strip().split()
    base = cwd or Path.cwd()
    force = False
    path_parts: list[str] = []
    for token in parts[1:]:
        if token in ("--force", "-f"):
            force = True
        else:
            path_parts.append(token)
    if len(path_parts) > 1:
        return None
    if path_parts:
        target = Path(path_parts[0]).expanduser()
        if not target.is_absolute():
            target = base / target
    else:
        target = base / DEFAULT_FILENAME
    return SaveCommand(path=target.resolve(), force=force)


def write_story_file(command: SaveCommand, markdown: str) -> tuple[bool, str]:
    if command.path.exists() and not command.force:
        return (
            False,
            f"File already exists: {command.path}\n"
            "Use a different name (e.g. `save my-story.md`) or "
            "`save --force` to overwrite.",
        )
    try:
        command.path.parent.mkdir(parents=True, exist_ok=True)
        command.path.write_text(markdown, encoding="utf-8")
    except OSError:
        return (
            False,
            "Could not write the file. Check that the path is valid and you have permission.",
        )
    return True, f"Story saved to {command.path}"
