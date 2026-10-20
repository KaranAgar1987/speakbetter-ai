import unittest
from unittest import mock

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.llm import ScriptCompleter


class TestVoiceCoachMode(unittest.TestCase):
    def test_conversational_voice_invokes_llm_on_story_text(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True, voice_conversational=True)
        app.start()
        with mock.patch.object(completer, "complete", wraps=completer.complete) as mocked:
            app.handle_line("Last week I presented to the leadership team.")
            mocked.assert_called()

    def test_efficient_voice_ack_without_llm(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True, voice_conversational=False)
        app.start()
        with mock.patch.object(completer, "complete") as mocked:
            out, _ = app.handle_line("Last week I presented to the leadership team.")
            mocked.assert_not_called()
        self.assertIn("next", out.lower())
        self.assertIn("Last week", out)

    def test_voice_checkin_not_recorded_as_story(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True)
        app.start()
        out, _ = app.handle_line("Hello, can you hear me?")
        self.assertIn("hear you", out.lower())
        self.assertNotIn("Hello, can you hear me?", app.session.step_drafts.get("context", ""))

    def test_voice_hint_phrase(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True)
        app.start()
        out, _ = app.handle_line("give me a hint")
        self.assertIn("scene", out.lower())

    def test_coaching_trigger_invokes_llm(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True)
        app.start()
        with mock.patch.object(completer, "complete", wraps=completer.complete) as mocked:
            app.handle_line("Can you give me feedback on that?")
            mocked.assert_called()


if __name__ == "__main__":
    unittest.main()
