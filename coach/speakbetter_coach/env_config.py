"""Load local .env files without overriding the process environment."""

from pathlib import Path

from speakbetter_coach.knowledge import find_repo_root


def load_local_env(repo_root: Path | None = None) -> list[Path]:
    """
    Load environment variables from local files.

    Precedence (highest first):
      1. Variables already set in the process environment
      2. ``coach/.env``
      3. Repository-root ``.env`` (fills keys not set by coach file)

    Returns paths that were loaded (missing files are skipped).
    """
    from dotenv import load_dotenv

    root = repo_root or find_repo_root()
    loaded: list[Path] = []

    coach_env = root / "coach" / ".env"
    root_env = root / ".env"

    if coach_env.is_file():
        load_dotenv(coach_env, override=False)
        loaded.append(coach_env)

    if root_env.is_file():
        load_dotenv(root_env, override=False)
        loaded.append(root_env)

    return loaded
