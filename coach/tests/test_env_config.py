import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from speakbetter_coach.env_config import load_local_env
from speakbetter_coach.llm import OpenAIChatCompleter


class TestEnvConfig(unittest.TestCase):
    def _fake_repo(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        (root / "knowledge").mkdir()
        (root / "knowledge" / "cart.md").write_text("# CART\n", encoding="utf-8")
        (root / "coach").mkdir()
        self.addCleanup(tmp.cleanup)
        return root

    def test_loads_coach_env(self) -> None:
        root = self._fake_repo()
        (root / "coach" / ".env").write_text(
            "OPENAI_API_KEY=from-coach-file\n", encoding="utf-8"
        )
        with mock.patch.dict(os.environ, {}, clear=True):
            loaded = load_local_env(root)
            self.assertEqual(loaded, [root / "coach" / ".env"])
            self.assertEqual(os.environ.get("OPENAI_API_KEY"), "from-coach-file")

    def test_loads_root_env_when_coach_missing(self) -> None:
        root = self._fake_repo()
        (root / ".env").write_text("OPENAI_API_KEY=from-root-file\n", encoding="utf-8")
        with mock.patch.dict(os.environ, {}, clear=True):
            loaded = load_local_env(root)
            self.assertEqual(loaded, [root / ".env"])
            self.assertEqual(os.environ.get("OPENAI_API_KEY"), "from-root-file")

    def test_coach_env_wins_over_root_for_same_key(self) -> None:
        root = self._fake_repo()
        (root / "coach" / ".env").write_text(
            "OPENAI_API_KEY=from-coach\nOPENAI_MODEL=coach-model\n",
            encoding="utf-8",
        )
        (root / ".env").write_text(
            "OPENAI_API_KEY=from-root\nOPENAI_MODEL=root-model\n",
            encoding="utf-8",
        )
        with mock.patch.dict(os.environ, {}, clear=True):
            load_local_env(root)
            self.assertEqual(os.environ.get("OPENAI_API_KEY"), "from-coach")
            self.assertEqual(os.environ.get("OPENAI_MODEL"), "coach-model")

    def test_process_env_wins_over_files(self) -> None:
        root = self._fake_repo()
        (root / "coach" / ".env").write_text(
            "OPENAI_API_KEY=from-file\n", encoding="utf-8"
        )
        with mock.patch.dict(
            os.environ, {"OPENAI_API_KEY": "from-process"}, clear=True
        ):
            load_local_env(root)
            self.assertEqual(os.environ.get("OPENAI_API_KEY"), "from-process")

    def test_missing_key_raises_clear_error(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError) as ctx:
                OpenAIChatCompleter()
            self.assertIn("OPENAI_API_KEY", str(ctx.exception))
            self.assertNotIn("sk-", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
