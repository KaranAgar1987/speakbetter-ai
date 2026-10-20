import unittest

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.llm import ScriptCompleter
from speakbetter_coach.voice_coaching import (
    build_voice_turn_extra,
    infer_communication_scenario,
    trim_voice_messages,
)


class TestVoiceCoaching(unittest.TestCase):
    def test_trim_keeps_system_and_recent_turns(self) -> None:
        messages = [{"role": "system", "content": "sys"}]
        for i in range(20):
            messages.append({"role": "user", "content": f"u{i}"})
            messages.append({"role": "assistant", "content": f"a{i}"})
        trimmed = trim_voice_messages(messages, max_turns=3)
        self.assertEqual(trimmed[0]["role"], "system")
        self.assertEqual(len(trimmed), 1 + 6)
        self.assertIn("u19", trimmed[-2]["content"])

    def test_infer_interview_scenario(self) -> None:
        self.assertEqual(
            infer_communication_scenario("preparing for a panel interview", {}),
            "interview practice",
        )

    def test_voice_extra_includes_anti_repeat(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True, voice_conversational=True)
        app.start()
        app.session.chat_messages.append(
            {"role": "assistant", "content": "What was at stake for you?"}
        )
        extra = build_voice_turn_extra(
            app.session, "I led a roadmap review", "Focus on Context"
        )
        self.assertIn("Last coach line", extra)
        self.assertIn("What was at stake", extra)

    def test_coach_reply_uses_trimmed_messages(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True, voice_conversational=True)
        app.start()
        captured: list[int] = []

        def spy_complete(messages, *, max_tokens=None):
            captured.append(len(messages))
            return ScriptCompleter().complete(messages, max_tokens=max_tokens)

        app.completer.complete = spy_complete  # type: ignore[method-assign]
        for i in range(12):
            app.handle_line(f"Detail line {i} about the project.")
        self.assertTrue(captured)
        self.assertLessEqual(captured[-1], 17)


if __name__ == "__main__":
    unittest.main()
