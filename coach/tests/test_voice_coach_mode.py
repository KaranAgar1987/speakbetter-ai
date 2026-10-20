import unittest
from unittest import mock

from speakbetter_coach.coach_app import CoachApp
from speakbetter_coach.llm import ScriptCompleter


class TestVoiceCoachMode(unittest.TestCase):
    def test_ack_without_llm_on_plain_story_text(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True)
        app.start()
        with mock.patch.object(completer, "complete") as mocked:
            out, _ = app.handle_line("Last week I presented to the leadership team.")
            mocked.assert_not_called()
        self.assertIn("next", out.lower())

    def test_coaching_trigger_invokes_llm(self) -> None:
        completer = ScriptCompleter()
        app = CoachApp(completer, "# CART\n", voice_mode=True)
        app.start()
        with mock.patch.object(completer, "complete", wraps=completer.complete) as mocked:
            app.handle_line("Can you give me feedback on that?")
            mocked.assert_called()


if __name__ == "__main__":
    unittest.main()
