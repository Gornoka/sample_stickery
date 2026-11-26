"""Writes the SVGs, renders them to PNG and assembles animated stickers. Output: images/<pack id>/."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

from packs import FPS, FRAMES, PACKS

HERE = Path(__file__).resolve().parent


def main(out: Path, only: set[str]) -> None:
    svg_dir = out.parent / "svg"
    jobs: list[tuple[Path, Path]] = []
    anim: list[tuple[Path, list[Path]]] = []
    for p in PACKS:
        for s in p.stickers:
            if only and f"{p.id}/{s.stem}" not in only and p.id not in only:
                continue
            (out / p.id).mkdir(parents=True, exist_ok=True)
            (svg_dir / p.id).mkdir(parents=True, exist_ok=True)
            if s.still is not None:
                src = svg_dir / p.id / f"{s.stem}.svg"
                src.write_text(s.still, encoding="utf-8")
                jobs.append((src, out / p.id / f"{s.stem}.png"))
            else:
                assert s.frame is not None
                fdir = svg_dir / p.id / s.stem
                fdir.mkdir(exist_ok=True)
                pngs = []
                for i in range(FRAMES):
                    src = fdir / f"f{i:02d}.svg"
                    src.write_text(s.frame(i / FRAMES), encoding="utf-8")
                    png = fdir / f"f{i:02d}.png"
                    jobs.append((src, png))
                    pngs.append(png)
                anim.append((out / p.id / f"{s.stem}.webp", pngs))
    jobs_file = svg_dir / "jobs.txt"
    jobs_file.write_text("".join(f"{a}\t{b}\n" for a, b in jobs), encoding="utf-8")
    env = dict(os.environ)
    env.setdefault("NODE_PATH", subprocess.check_output(["npm", "root", "-g"], text=True).strip())
    subprocess.run(["node", str(HERE / "render.js"), str(jobs_file)], check=True, env=env)
    for p in PACKS:
        if only and p.id not in only:
            continue
        s = next(x for x in p.stickers if x.stem == p.tray)
        first = svg_dir / p.id / s.stem / "f00.png" if s.frame else out / p.id / f"{s.stem}.png"
        Image.open(first).save(out / p.id / "tray.png")
    for dst, pngs in anim:
        frames = [Image.open(x).convert("RGBA") for x in pngs]
        frames[0].save(
            dst,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // FPS,
            loop=0,
            lossless=False,
            quality=80,
            method=6,
        )
    print(f"{len(jobs)} frames rendered, {len(anim)} animated stickers")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), set(sys.argv[2:]))
