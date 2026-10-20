import sys

from speakbetter_coach.cli import run_interactive
from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.knowledge import find_repo_root, load_cart_markdown
from speakbetter_coach.llm import OpenAIChatCompleter


def main() -> None:
    try:
        load_local_env()
        find_repo_root()
        load_cart_markdown()
        run_interactive(OpenAIChatCompleter())
    except RuntimeError as err:
        print(f"Error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
    except FileNotFoundError as err:
        print(
            f"Error: {err}\n"
            "Launch the CLI from the speakbetter-ai repository root "
            "(the folder that contains knowledge/cart.md).",
            file=sys.stderr,
        )
        raise SystemExit(1) from err


if __name__ == "__main__":
    main()
