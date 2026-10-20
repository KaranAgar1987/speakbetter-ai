import os
import unittest
from unittest import mock

from speakbetter_coach.__main__ import main


class TestMainEntrypoint(unittest.TestCase):
    @mock.patch("speakbetter_coach.__main__.run_interactive")
    @mock.patch("speakbetter_coach.__main__.load_cart_markdown")
    @mock.patch("speakbetter_coach.__main__.find_repo_root")
    @mock.patch("speakbetter_coach.__main__.load_local_env")
    @mock.patch("speakbetter_coach.__main__.OpenAIChatCompleter")
    def test_main_starts_when_configured(
        self, _completer, _load_env, _root, _cart, run
    ) -> None:
        main()
        run.assert_called_once()

    @mock.patch("speakbetter_coach.__main__.load_local_env")
    @mock.patch("speakbetter_coach.__main__.OpenAIChatCompleter", side_effect=RuntimeError("OPENAI_API_KEY is not set"))
    def test_missing_api_key_exits_cleanly(self, _completer, _load_env) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
