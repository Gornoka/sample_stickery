"""Builds the demo packs and their release zips with the Sticker Shim tools.

images/<id>/  ->  packs/<id>/ (stickers.py make, then names and emojis from art/packs.py)
packs/        ->  site/ (stickers.py publish: index.json and pack folders); release.py zips site/

Usage: python build.py --tools ../sticker_shim/tools [--skip-make]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "art"))

from packs import PACKS  # noqa: E402

PUBLISHER = "Sticker Shim demo"


def stickers(tools: Path, *args: str) -> None:
    subprocess.run(["uv", "run", "--project", str(tools), str(tools / "stickers.py"), *args], check=True)


def make(tools: Path) -> None:
    for p in PACKS:
        src = ROOT / "images" / p.id
        stickers(
            tools,
            "make",
            str(src),
            "--out",
            str(ROOT / "packs" / p.id),
            "--id",
            p.id,
            "--name",
            p.name,
            "--publisher",
            PUBLISHER,
            "--margin",
            "0",
        )
        path = ROOT / "packs" / p.id / "contents.json"
        c = json.loads(path.read_text(encoding="utf-8"))
        by_stem = {s.stem: s for s in p.stickers}
        for entry in c["stickers"]:
            s = by_stem[Path(entry["image_file"]).stem]
            entry["emojis"] = s.emojis
            entry["name"] = s.name
        path.write_text(json.dumps(c, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def publish(tools: Path) -> None:
    """packs/ -> site/: index.json plus pack folders, served for URL import and zipped by release.py."""
    stickers(tools, "check", str(ROOT / "packs"))
    site = ROOT / "site"
    stickers(tools, "publish", str(ROOT / "packs"), "--out", str(site), "--no-zip", "--force")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools", type=Path, required=True, help="the tools/ folder of a sticker_shim checkout")
    ap.add_argument("--skip-make", action="store_true", help="only publish the committed packs/ to site/")
    a = ap.parse_args()
    tools = a.tools.resolve()
    if not a.skip_make:
        make(tools)
    publish(tools)


if __name__ == "__main__":
    main()
