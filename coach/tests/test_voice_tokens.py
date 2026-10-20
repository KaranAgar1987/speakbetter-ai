import base64
import json
import os
import unittest
from unittest import mock

from speakbetter_coach.voice.config import LiveKitConfig
from speakbetter_coach.voice.tokens import create_participant_token


class TestVoiceTokens(unittest.TestCase):
    def test_token_does_not_contain_secret(self) -> None:
        secret = "super-secret-livekit-value"
        config = LiveKitConfig(
            url="wss://example.livekit.cloud",
            api_key="APIabcdef",
            api_secret=secret,
            room="speakbetter-cart",
            openai_api_key="sk-test",
            openai_model="gpt-4o-mini",
        )
        jwt = create_participant_token(config, identity="user-1")
        self.assertTrue(len(jwt) > 20)
        self.assertNotIn(secret, jwt)
        self.assertNotIn("super-secret", jwt)
        payload_b64 = jwt.split(".")[1]
        payload_b64 += "=" * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_b64))
        self.assertIn("roomConfig", payload)
        self.assertTrue(payload["roomConfig"].get("agents"))

    def test_token_endpoint_shape(self) -> None:
        env = {
            "LIVEKIT_URL": "wss://example.livekit.cloud",
            "LIVEKIT_API_KEY": "APIkey",
            "LIVEKIT_API_SECRET": "secret",
            "OPENAI_API_KEY": "sk-test",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            from speakbetter_coach.voice.config import load_livekit_config
            from speakbetter_coach.voice.tokens import create_participant_token

            cfg = load_livekit_config()
            token = create_participant_token(cfg)
            self.assertIsInstance(token, str)


if __name__ == "__main__":
    unittest.main()
