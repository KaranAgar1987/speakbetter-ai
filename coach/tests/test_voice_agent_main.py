import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from speakbetter_coach.voice import agent as voice_agent


class TestVoiceAgentMain(unittest.TestCase):
    def test_main_loads_env_before_run_app(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "knowledge").mkdir()
            (root / "knowledge" / "cart.md").write_text("# CART\n", encoding="utf-8")
            coach_dir = root / "coach"
            coach_dir.mkdir()
            (coach_dir / ".env").write_text(
                "LIVEKIT_URL=ws://localhost:7880\n"
                "LIVEKIT_API_KEY=devkey\n"
                "LIVEKIT_API_SECRET=secret\n"
                "OPENAI_API_KEY=sk-test\n",
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {}, clear=True):
                with mock.patch(
                    "speakbetter_coach.voice.agent.find_repo_root", return_value=root
                ):
                    with mock.patch(
                        "speakbetter_coach.voice.agent.cli.run_app"
                    ) as run_app:
                        voice_agent.main()
            run_app.assert_called_once()
            opts = run_app.call_args[0][0]
            self.assertEqual(opts.ws_url, "ws://localhost:7880")
            self.assertEqual(opts.api_key, "devkey")
            self.assertEqual(opts.api_secret, "secret")


if __name__ == "__main__":
    unittest.main()
