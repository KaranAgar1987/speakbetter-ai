"""Locate repository root and load knowledge/cart.md."""

from pathlib import Path

CART_RELATIVE = Path("knowledge") / "cart.md"


def find_repo_root(start: Path | None = None) -> Path:
    """Walk parents from start until knowledge/cart.md exists."""
    current = (start or Path(__file__).resolve()).parent
    for candidate in [current, *current.parents]:
        if (candidate / CART_RELATIVE).is_file():
            return candidate
    raise FileNotFoundError(
        f"Could not find {CART_RELATIVE} by walking up from {current}"
    )


def load_cart_markdown(repo_root: Path | None = None) -> str:
    root = repo_root or find_repo_root()
    path = root / CART_RELATIVE
    return path.read_text(encoding="utf-8")


def cart_path(repo_root: Path | None = None) -> Path:
    root = repo_root or find_repo_root()
    return root / CART_RELATIVE
