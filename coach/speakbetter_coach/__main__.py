from speakbetter_coach.cli import run_interactive
from speakbetter_coach.llm import OpenAIChatCompleter


def main() -> None:
    run_interactive(OpenAIChatCompleter())


if __name__ == "__main__":
    main()
