"""Writes the SVGs, renders them to PNG and assembles animated stickers. Output: <out>/<pack id>/.

SVGs and animation frames go to svg/ next to <out>. Rendering needs Node with Playwright and Chromium (render.js).

Usage: uv run art/build_images.py images [<pack id> | <pack id>/<stem> ...]
"""

import argparse
import os
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from PIL import Image

from art.packs import FPS, FRAMES, PACKS

HERE: Path = Path(__file__).resolve().parent


class RenderError(Exception):
    """Raised when the SVGs cannot be rendered."""


@dataclass(frozen=True, slots=True)
class Args:
    """Command-line arguments.

    Attributes:
        out (Path): Output folder, one subfolder per pack.
        only (set[str]): Pack ids or ``<id>/<stem>`` to render; empty renders everything.
    """

    out: Path
    only: set[str]


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Parse command-line arguments.

    Args:
        argv (Sequence[str] | None): Argument vector, defaulting to ``sys.argv[1:]``.

    Returns:
        Args: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    _ = parser.add_argument("out", type=Path, help="output folder, one subfolder per pack")
    _ = parser.add_argument("only", nargs="*", help="pack ids or <id>/<stem> to render (default: all)")
    namespace = parser.parse_args(argv)
    return Args(out=cast(Path, namespace.out).resolve(), only=set(cast(list[str], namespace.only)))


def render(jobs_file: Path) -> None:
    """Render the SVG -> PNG jobs listed in a file with render.js.

    Args:
        jobs_file (Path): Lines of ``<svg>\\t<png>``.

    Raises:
        RenderError: If npm or node is missing or rendering fails.
    """
    env = dict(os.environ)
    try:
        if "NODE_PATH" not in env:
            env["NODE_PATH"] = subprocess.check_output(["npm", "root", "-g"], text=True).strip()
        _ = subprocess.run(["node", str(HERE / "render.js"), str(jobs_file)], check=True, env=env)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RenderError(f"rendering failed: {exc}") from exc


def build(out: Path, only: set[str]) -> str:
    """Write the SVGs, render them and save PNGs, animated WebPs and tray icons.

    Args:
        out (Path): Output folder, one subfolder per pack.
        only (set[str]): Pack ids or ``<id>/<stem>`` to render; empty renders everything.

    Returns:
        str: A one-line summary.

    Raises:
        RenderError: If rendering fails.
    """
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
                _ = src.write_text(s.still, encoding="utf-8")
                jobs.append((src, out / p.id / f"{s.stem}.png"))
            else:
                assert s.frame is not None
                fdir = svg_dir / p.id / s.stem
                fdir.mkdir(exist_ok=True)
                pngs: list[Path] = []
                for i in range(FRAMES):
                    src = fdir / f"f{i:02d}.svg"
                    _ = src.write_text(s.frame(i / FRAMES), encoding="utf-8")
                    png = fdir / f"f{i:02d}.png"
                    jobs.append((src, png))
                    pngs.append(png)
                anim.append((out / p.id / f"{s.stem}.webp", pngs))
    jobs_file = svg_dir / "jobs.txt"
    _ = jobs_file.write_text("".join(f"{a}\t{b}\n" for a, b in jobs), encoding="utf-8")
    render(jobs_file)
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
    return f"{len(jobs)} frames rendered, {len(anim)} animated stickers"


def main() -> int:
    """Render the images.

    Returns:
        int: Process exit code (0 success, 2 rendering failed).
    """
    args = parse_args()
    try:
        print(build(args.out, args.only))
    except RenderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
