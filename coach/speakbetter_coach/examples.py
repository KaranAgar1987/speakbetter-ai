"""Example stories from knowledge/cart.md with required attribution labels."""

VERIFIED_DENTIST = """[Verified source example — condensed paraphrase from SRC-001 / Philipp Humm teaching; not exact quotes]

Context: April 2022, dentist in Amsterdam for a routine check-up; dentist suggests adding 1mm of filling to front teeth after years of grinding; it sounded like a good idea.

Adversity: About 30 minutes later he lisps; the first day teeth feel alien—lisping, clashing, spitting; he worries about his job and speaking invites.

Resolution: Second day still weird but less so; one week later it feels fine; teeth still a bit short and gray but he's happy enough.

Takeaway: Change feels odd at first, but after a few rounds it becomes more natural.
"""

SPEAKBETTER_ILLUSTRATIONS: dict[str, str] = {
    "a": """[Original SpeakBetter AI illustration A — not from Philipp Humm]

Context: Last Tuesday, ten minutes before a client demo, in the war room with PM—payment flow needed to be live.
Adversity: Staging down, backup env on old branch, client's exec already on the call.
Resolution: Walked through a recorded clip, shipped hotfix in parallel, sent follow-up link that night.
Takeaway: What I learned is that an honest partial demo plus a clear recovery plan beats pretending nothing failed.
""",
    "b": """[Original SpeakBetter AI illustration B — not from Philipp Humm]

Context: First month as team lead, 1:1 with Alex after three sprints of missed deadlines.
Adversity: Torn between fair and firm—afraid they'd shut down; unsure if notes were too harsh.
Resolution: Named the pattern, asked what was blocking them, agreed on one smaller commitment for next week.
Takeaway: What I learned is that specific examples and curiosity land better than a vague 'you need to improve.'
""",
    "c": """[Original SpeakBetter AI illustration C — not from Philipp Humm]

Context: Q3 renewal call; champion quiet; finance joined without warning.
Adversity: Re-evaluating vendors; deck had last year's pricing; unclear who owned the decision.
Resolution: Paused, asked what success looks like in twelve months, offered a pilot for one team.
Takeaway: What I learned is that when the room shifts, questions beat sliding another slide.
""",
    "d": """[Original SpeakBetter AI illustration D — not from Philipp Humm]

Context: Final-round interview for a product role after a quarter of prep.
Adversity: Rejection; recruiter cited domain depth gap; embarrassment and replaying answers.
Resolution: Asked recruiter for one concrete gap; rewrote portfolio stories; booked mock interviews for motivation practice.
Takeaway: What I learned is that rejection helps only when I name one change in how I prepare—not when I treat it as proof I don't belong.
""",
}

EXAMPLE_MENU = """Examples (from knowledge/cart.md):
  example dentist     — Verified SRC-001 paraphrase (Philipp Humm teaching)
  example a|b|c|d     — Original SpeakBetter AI workplace illustrations
"""


def resolve_example_command(parts: list[str]) -> str | None:
    if not parts:
        return EXAMPLE_MENU
    key = parts[0].lower()
    if key == "dentist":
        return VERIFIED_DENTIST
    if key in SPEAKBETTER_ILLUSTRATIONS:
        return SPEAKBETTER_ILLUSTRATIONS[key]
    return EXAMPLE_MENU + "\nUnknown option. Try: example dentist | example a"
