import os
import unittest
from unittest import mock

from speakbetter_coach.voice.config import load_livekit_config


class TestVoiceConfig(unittest.TestCase):
    def test_missing_vars_raises(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError) as ctx:
                load_livekit_config()
            msg = str(ctx.exception)
            self.assertIn("LIVEKIT_URL", msg)
            self.assertIn("OPENAI_API_KEY", msg)
            self.assertNotIn("sk-", msg)

    def test_loads_when_set(self) -> None:
        env = {
            "LIVEKIT_URL": "wss://example.livekit.cloud",
            "LIVEKIT_API_KEY": "APIkey",
            "LIVEKIT_API_SECRET": "secret",
            "OPENAI_API_KEY": "sk-test",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            cfg = load_livekit_config()
            self.assertEqual(cfg.room, "speakbetter-cart")
            self.assertEqual(cfg.url, "wss://example.livekit.cloud")


if __name__ == "__main__":
    unittest.main()
