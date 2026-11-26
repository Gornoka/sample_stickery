"""Zips site/ into the release assets (no Sticker Shim tools needed).

dist/sticker-shim-demo.zip   every pack plus shim.json: the app imports them as editable own packs in their groups
dist/<pack id>.zip           one pack each, plain publish.py layout: the app imports it as a read-only pack

Usage: uv run release.py (replaces dist/)
"""

import argparse
import json
import shutil
import sys
import zipfile
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import cast

from art.packs import GROUPS

ROOT: Path = Path(__file__).resolve().parent
# Name of the zip with every pack and the groups; README and RELEASE_NOTES.md link it.
ALL: str = "sticker-shim-demo.zip"

type JsonObject = dict[str, object]


class ReleaseError(Exception):
    """Raised when site/ cannot be zipped."""


def parse_args(argv: Sequence[str] | None = None) -> None:
    """Parse command-line arguments (only ``--help``).

    Args:
        argv (Sequence[str] | None): Argument vector, defaulting to ``sys.argv[1:]``.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    _ = parser.parse_args(argv)


def add_pack(z: zipfile.ZipFile, site: Path, pid: str) -> None:
    """Add the files of one pack folder to a zip, under ``<pid>/``.

    Args:
        z (zipfile.ZipFile): The zip to write to.
        site (Path): The site/ folder.
        pid (str): Pack identifier, also the folder name.
    """
    for f in sorted((site / pid).iterdir()):
        z.write(f, f"{pid}/{f.name}")


def release(site: Path, dist: Path) -> None:
    """Write one zip per pack and one with every pack and the groups.

    Args:
        site (Path): The site/ folder written by build.py.
        dist (Path): Output folder; replaced completely.

    Raises:
        ReleaseError: If site/index.json is missing or unreadable.
    """
    try:
        index = cast(JsonObject, json.loads((site / "index.json").read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleaseError(f"cannot read {site / 'index.json'} ({exc}); run build.py first") from exc
    packs = cast(list[JsonObject], index["packs"])
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    kinds: dict[str, str] = {}
    for p in packs:
        pid = cast(str, p["identifier"])
        kinds[pid] = "animated" if p.get("animated_sticker_pack") else "still"
        one = {**index, "packs": [p]}
        with zipfile.ZipFile(dist / f"{pid}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("index.json", json.dumps(one, ensure_ascii=False, indent=2))
            add_pack(z, site, pid)
    no_ignored: list[str] = []
    shim: JsonObject = {
        "format": 1,
        "app": "demo",
        "kind": "group",
        "packs": {
            pid: {"own": True, "own_kind": k, "ignored": no_ignored, "projects": False} for pid, k in kinds.items()
        },
        "groups": [asdict(g) for g in GROUPS],
    }
    with zipfile.ZipFile(dist / ALL, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(site / "index.json", "index.json")
        z.writestr("shim.json", json.dumps(shim, ensure_ascii=False, indent=2))
        for p in packs:
            add_pack(z, site, cast(str, p["identifier"]))


def main() -> int:
    """Build the release zips and print their sizes.

    Returns:
        int: Process exit code (0 success, 2 site/ could not be read).
    """
    parse_args()
    dist = ROOT / "dist"
    try:
        release(ROOT / "site", dist)
    except ReleaseError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    for f in sorted(dist.iterdir()):
        print(f"{f.name}: {f.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
