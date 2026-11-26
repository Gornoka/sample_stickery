"""Contact sheet of every pack in an images folder (first frame of animated stickers).

Usage: python art/sheet.py images preview.png
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CELL = 200
COLS = 6
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")


def main(src: Path, out: Path) -> None:
    packs = sorted(p for p in src.iterdir() if p.is_dir())
    files = {p: sorted(f for f in p.iterdir() if f.name != "tray.png") for p in packs}
    rows = sum((len(fs) + COLS - 1) // COLS for fs in files.values())
    font = ImageFont.truetype(str(FONT), 22) if FONT.exists() else ImageFont.load_default()
    img = Image.new("RGB", (COLS * CELL, rows * CELL + 40 * len(packs)), "#cfd6e4")
    d = ImageDraw.Draw(img)
    y = 0
    for p in packs:
        d.text((10, y + 8), p.name, fill="#222", font=font)
        y += 40
        for i, f in enumerate(files[p]):
            im = Image.open(f).convert("RGBA").resize((CELL, CELL))
            img.paste(im, ((i % COLS) * CELL, y + (i // COLS) * CELL), im)
        y += ((len(files[p]) + COLS - 1) // COLS) * CELL
    img.save(out)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
