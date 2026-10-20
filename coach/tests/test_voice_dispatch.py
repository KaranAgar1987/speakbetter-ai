import unittest
from types import SimpleNamespace
from unittest import mock

from speakbetter_coach.voice.config import LiveKitConfig
from speakbetter_coach.voice.dispatch import _room_has_agent


class TestVoiceDispatch(unittest.TestCase):
    def test_detects_agent_participant(self) -> None:
        user = SimpleNamespace(kind=0, identity="speakbetter-user")
        agent = SimpleNamespace(kind=4, identity="agent-abc")
        self.assertFalse(_room_has_agent([user]))
        self.assertTrue(_room_has_agent([user, agent]))


if __name__ == "__main__":
    unittest.main()
