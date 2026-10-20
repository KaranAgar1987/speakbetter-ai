import tempfile
import unittest
from pathlib import Path
from unittest import mock

from speakbetter_coach.cli import CoachApp
from speakbetter_coach.llm import ScriptCompleter
from speakbetter_coach.session import Session, Step
from speakbetter_coach.story_save import (
    DEFAULT_FILENAME,
    format_story_markdown,
    parse_save_command,
    story_is_complete,
    write_story_file,
)


class TestStorySave(unittest.TestCase):
    def _full_drafts(self) -> dict[str, str]:
        return {
            "context": "Team demo on Tuesday.",
            "adversity": "Staging was down.",
            "resolution": "We used a recording.",
            "takeaway": "What I learned is honesty beats pretending.",
        }

    def test_format_markdown_sections(self) -> None:
        md = format_story_markdown(self._full_drafts())
        self.assertIn("## Context", md)
        self.assertIn("## Takeaway", md)
        self.assertIn("Staging was down.", md)
        self.assertNotIn("OPENAI", md)

    def test_story_not_complete_until_done(self) -> None:
        s = Session()
        s.step_drafts = self._full_drafts()
        s.step = Step.TAKEAWAY
        self.assertFalse(story_is_complete(s.step_drafts, s.step))
        s.step = Step.DONE
        self.assertTrue(story_is_complete(s.step_drafts, s.step))

    def test_save_writes_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "out.md"
            cmd = parse_save_command("save out.md", cwd=Path(tmp))
            assert cmd is not None
            ok, msg = write_story_file(cmd, "# test\n")
            self.assertTrue(ok)
            self.assertTrue(path.is_file())
            self.assertIn(str(path.resolve()), msg)

    def test_existing_file_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / DEFAULT_FILENAME
            target.write_text("old", encoding="utf-8")
            cmd = parse_save_command("save", cwd=Path(tmp))
            assert cmd is not None
            ok, msg = write_story_file(cmd, "# new\n")
            self.assertFalse(ok)
            self.assertIn("already exists", msg.lower())
            self.assertEqual(target.read_text(encoding="utf-8"), "old")

    def test_force_overwrites(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "story.md"
            target.write_text("old", encoding="utf-8")
            cmd = parse_save_command("save --force story.md", cwd=Path(tmp))
            assert cmd is not None
            ok, _ = write_story_file(cmd, "# new\n")
            self.assertTrue(ok)
            self.assertEqual(target.read_text(encoding="utf-8"), "# new\n")

    def test_incomplete_session_message(self) -> None:
        app = CoachApp(ScriptCompleter(), "# CART\n", cwd=Path("."))
        app.start()
        out, _ = app.handle_line("save")
        self.assertIn("not ready", out.lower())

    def test_save_after_done_no_extra_llm_calls(self) -> None:
        completer = ScriptCompleter()
        with tempfile.TemporaryDirectory() as tmp:
            app = CoachApp(completer, "# CART\n", cwd=Path(tmp))
            app.start()
            for text in (
                "Context line.",
                "Adversity line.",
                "Resolution line.",
                "Takeaway line.",
            ):
                app.handle_line(text)
                app.handle_line("next")
            self.assertEqual(app.session.step, Step.DONE)
            with mock.patch.object(
                completer, "complete", wraps=completer.complete
            ) as mocked:
                out, _ = app.handle_line("save")
                mocked.assert_not_called()
            self.assertIn("saved", out.lower())
            saved = Path(tmp) / DEFAULT_FILENAME
            self.assertTrue(saved.is_file())
            content = saved.read_text(encoding="utf-8")
            self.assertIn("Context line.", content)
            self.assertIn("Takeaway line.", content)


if __name__ == "__main__":
    unittest.main()
