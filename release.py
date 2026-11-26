"""Zips site/ into the release assets (stdlib only, no Sticker Shim tools needed).

dist/sticker-shim-demo.zip   every pack plus shim.json: the app imports them as editable own packs in their groups
dist/<pack id>.zip           one pack each, plain publish.py layout: the app imports it as a read-only pack
"""

from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "art"))

from packs import GROUPS  # noqa: E402

ALL = "sticker-shim-demo.zip"


def add_pack(z: zipfile.ZipFile, site: Path, pid: str) -> None:
    for f in sorted((site / pid).iterdir()):
        z.write(f, f"{pid}/{f.name}")


def main() -> None:
    site, dist = ROOT / "site", ROOT / "dist"
    index = json.loads((site / "index.json").read_text(encoding="utf-8"))
    packs = index["packs"]
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    kinds = {}
    for p in packs:
        pid = p["identifier"]
        kinds[pid] = "animated" if p.get("animated_sticker_pack") else "still"
        one = {**index, "packs": [p]}
        with zipfile.ZipFile(dist / f"{pid}.zip", "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("index.json", json.dumps(one, ensure_ascii=False, indent=2))
            add_pack(z, site, pid)
    shim = {
        "format": 1,
        "app": "demo",
        "kind": "group",
        "packs": {pid: {"own": True, "own_kind": k, "ignored": [], "projects": False} for pid, k in kinds.items()},
        "groups": GROUPS,
    }
    with zipfile.ZipFile(dist / ALL, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(site / "index.json", "index.json")
        z.writestr("shim.json", json.dumps(shim, ensure_ascii=False, indent=2))
        for p in packs:
            add_pack(z, site, p["identifier"])
    for f in sorted(dist.iterdir()):
        print(f"{f.name}: {f.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
