import unittest
from types import SimpleNamespace

from speakbetter_coach.voice.messages import user_message_text


class TestVoiceMessages(unittest.TestCase):
    def test_property_style(self) -> None:
        msg = SimpleNamespace(text_content="Hello coach")
        self.assertEqual(user_message_text(msg), "Hello coach")

    def test_callable_style(self) -> None:
        msg = SimpleNamespace(text_content=lambda: "Legacy")
        self.assertEqual(user_message_text(msg), "Legacy")


if __name__ == "__main__":
    unittest.main()
