import unittest

from speakbetter_coach.guardrails import (
    contains_forbidden_coach_language,
    filter_forbidden_phrases,
)


class TestGuardrails(unittest.TestCase):
    def test_detects_score_language(self) -> None:
        self.assertTrue(contains_forbidden_coach_language("Your CART score: 87%"))
        self.assertTrue(contains_forbidden_coach_language("This is a pass/fail check."))

    def test_allows_normal_coaching(self) -> None:
        self.assertFalse(
            contains_forbidden_coach_language("What did you learn from that experience?")
        )

    def test_filter_removes_bad_line(self) -> None:
        raw = "Nice work.\nYour validated story badge is unlocked.\nTry adding emotion."
        cleaned = filter_forbidden_phrases(raw)
        self.assertNotIn("validated", cleaned.lower())
        self.assertIn("emotion", cleaned.lower())


if __name__ == "__main__":
    unittest.main()
