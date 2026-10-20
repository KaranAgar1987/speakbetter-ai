import unittest
from pathlib import Path

from speakbetter_coach.knowledge import cart_path, find_repo_root, load_cart_markdown


class TestKnowledge(unittest.TestCase):
    def test_find_cart_from_coach_package(self) -> None:
        root = find_repo_root(Path(__file__).resolve())
        self.assertTrue((root / "knowledge" / "cart.md").is_file())

    def test_load_cart_contains_cart_framework(self) -> None:
        text = load_cart_markdown()
        self.assertIn("Context", text)
        self.assertIn("Adversity", text)
        self.assertIn("Resolution", text)
        self.assertIn("Takeaway", text)

    def test_cart_path_matches_load(self) -> None:
        path = cart_path()
        self.assertEqual(path.read_text(encoding="utf-8"), load_cart_markdown())


if __name__ == "__main__":
    unittest.main()
