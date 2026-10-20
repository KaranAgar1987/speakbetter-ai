from speakbetter_coach.cli import run_interactive
from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.llm import OpenAIChatCompleter


def main() -> None:
    load_local_env()
    run_interactive(OpenAIChatCompleter())


if __name__ == "__main__":
    main()
