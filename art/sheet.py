"""Contact sheet of every pack in an images folder (first frame of animated stickers).

Usage: uv run art/sheet.py images preview.png
"""

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from PIL import Image, ImageDraw, ImageFont

# 6 x 200 px gives a 1200 px wide sheet, readable in a GitHub README.
CELL: int = 200
COLS: int = 6
# Pack titles; Pillow's built-in font is used when this one is missing.
DEFAULT_FONT: Path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


@dataclass(frozen=True, slots=True)
class Args:
    """Command-line arguments.

    Attributes:
        src (Path): Images folder, one subfolder per pack.
        out (Path): PNG file to write.
        font (Path): TrueType font for the pack titles.
    """

    src: Path
    out: Path
    font: Path


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Parse command-line arguments.

    Args:
        argv (Sequence[str] | None): Argument vector, defaulting to ``sys.argv[1:]``.

    Returns:
        Args: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    _ = parser.add_argument("src", type=Path, help="images folder, one subfolder per pack")
    _ = parser.add_argument("out", type=Path, help="PNG file to write (overwritten)")
    _ = parser.add_argument(
        "--font",
        type=Path,
        default=DEFAULT_FONT,
        help=f"TrueType font for the pack titles; Pillow's default if missing (default: {DEFAULT_FONT})",
    )
    namespace = parser.parse_args(argv)
    return Args(src=cast(Path, namespace.src), out=cast(Path, namespace.out), font=cast(Path, namespace.font))


def sheet(src: Path, font_path: Path) -> Image.Image:
    """Draw every sticker of every pack folder on one image, a titled block per pack.

    Args:
        src (Path): Images folder, one subfolder per pack.
        font_path (Path): TrueType font for the pack titles.

    Returns:
        Image.Image: The contact sheet.
    """
    packs = sorted(p for p in src.iterdir() if p.is_dir())
    files = {p: sorted(f for f in p.iterdir() if f.name != "tray.png") for p in packs}
    rows = sum((len(fs) + COLS - 1) // COLS for fs in files.values())
    font = ImageFont.truetype(str(font_path), 22) if font_path.exists() else ImageFont.load_default()
    img = Image.new("RGB", (COLS * CELL, rows * CELL + 40 * len(packs)), "#cfd6e4")
    d = ImageDraw.Draw(img)
    y = 0
    for p in packs:
        d.text((10, y + 8), p.name, fill="#222", font=font)
        y += 40
        for i, f in enumerate(files[p]):
            im = Image.open(f).convert("RGBA").resize((CELL, CELL))  # pyright: ignore[reportUnknownMemberType]  # Pillow types size with numpy
            img.paste(im, ((i % COLS) * CELL, y + (i // COLS) * CELL), im)
        y += ((len(files[p]) + COLS - 1) // COLS) * CELL
    return img


def main() -> int:
    """Write the contact sheet.

    Returns:
        int: Process exit code (0 success, 2 the images folder is missing).
    """
    args = parse_args()
    if not args.src.is_dir():
        print(f"error: images folder not found: {args.src}", file=sys.stderr)
        return 2
    sheet(args.src, args.font).save(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
