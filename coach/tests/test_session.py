import unittest

from speakbetter_coach.cli import CoachApp
from speakbetter_coach.llm import ScriptCompleter
from speakbetter_coach.session import Session, Step


class TestSession(unittest.TestCase):
    def test_advance_through_cart_steps(self) -> None:
        s = Session()
        s.advance_step()
        self.assertEqual(s.step, Step.CONTEXT)
        s.advance_step()
        self.assertEqual(s.step, Step.ADVERSITY)
        s.advance_step()
        self.assertEqual(s.step, Step.RESOLUTION)
        s.advance_step()
        self.assertEqual(s.step, Step.TAKEAWAY)
        s.advance_step()
        self.assertEqual(s.step, Step.ASSEMBLE)

    def test_record_step_content(self) -> None:
        s = Session()
        s.step = Step.CONTEXT
        s.record_step_content("Monday standup.")
        self.assertIn("Monday", s.step_drafts["context"])


class TestCoachApp(unittest.TestCase):
    def setUp(self) -> None:
        self.cart = "# CART\nContext Adversity Resolution Takeaway\n"
        self.app = CoachApp(ScriptCompleter(), self.cart)

    def test_hint_command(self) -> None:
        self.app.start()
        out, exit_ = self.app.handle_line("hint")
        self.assertFalse(exit_)
        self.assertIn("Context", out)

    def test_example_dentist_label(self) -> None:
        out, _ = self.app.handle_line("example dentist")
        self.assertIn("SRC-001", out)

    def test_example_speakbetter_label(self) -> None:
        out, _ = self.app.handle_line("example a")
        self.assertIn("SpeakBetter AI", out)

    def test_restart(self) -> None:
        self.app.start()
        self.app.handle_line("I was in a meeting.")
        out, exit_ = self.app.handle_line("restart")
        self.assertFalse(exit_)
        self.assertIn("restarted", out.lower())

    def test_quit(self) -> None:
        out, exit_ = self.app.handle_line("quit")
        self.assertTrue(exit_)

    def test_coach_reply_no_forbidden_on_script(self) -> None:
        self.app.start()
        out, _ = self.app.handle_line("We had a tough sprint review.")
        self.assertNotIn("pass/fail", out.lower())
        self.assertNotIn("validated story", out.lower())


if __name__ == "__main__":
    unittest.main()
