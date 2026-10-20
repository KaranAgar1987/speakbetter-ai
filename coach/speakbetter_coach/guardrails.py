"""Output constraints aligned with knowledge/cart.md §4 and §7."""

import re

# Phrases that should not appear in coach-facing output (case-insensitive).
FORBIDDEN_PATTERNS: list[re.Pattern[str]] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"validated\s+story",
        r"pass\s*/\s*fail",
        r"\bpass\b.*\bfail\b",
        r"\byou\s+passed\b",
        r"\byou\s+failed\b",
        r"\bscore\s*:\s*\d+",
        r"\b\d+\s*/\s*10\b",
        r"\b\d+%\s*(cart|score|complete)",
        r"validation\s+badge",
        r"numeric\s+grade",
    ]
]


def contains_forbidden_coach_language(text: str) -> bool:
    return any(p.search(text) for p in FORBIDDEN_PATTERNS)


def filter_forbidden_phrases(text: str) -> str:
    """Remove lines that look like scoring or validation (best-effort)."""
    if not contains_forbidden_coach_language(text):
        return text
    lines = []
    for line in text.splitlines():
        if contains_forbidden_coach_language(line):
            continue
        lines.append(line)
    return "\n".join(lines).strip() or (
        "Let's keep shaping your story—what feels most important to add next?"
    )
