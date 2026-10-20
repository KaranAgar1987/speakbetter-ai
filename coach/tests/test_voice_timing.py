import unittest

from speakbetter_coach.voice.timing import TurnTimer


class TestVoiceTiming(unittest.TestCase):
    def test_deltas_include_total(self) -> None:
        timer = TurnTimer()
        timer.mark("a")
        timer.mark("b")
        deltas = timer.deltas_ms()
        self.assertIn("a", deltas)
        self.assertIn("b", deltas)
        self.assertIn("total_ms", deltas)


if __name__ == "__main__":
    unittest.main()
