"""Interactive CART coach CLI."""

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.knowledge import find_repo_root, load_cart_markdown
from speakbetter_coach.llm import ChatCompleter

WELCOME_TEXT = """SpeakBetter AI — CART coach (text)
Context → Adversity → Resolution → Takeaway

Describe a workplace situation you want to turn into a short story.
Commands: hint | example [dentist|a|b|c|d] | next | save [path] | restart | quit
"""


def run_interactive(completer: ChatCompleter) -> None:
    root = find_repo_root()
    cart = load_cart_markdown(root)
    app = CoachApp(completer, cart, voice_mode=False)
    print(WELCOME_TEXT)
    print(app.start())
    print()
    while True:
        try:
            line = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        out, exit_ = app.handle_line(line)
        if out:
            print(f"\nCoach> {out}\n")
        if exit_:
            break
