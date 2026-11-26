"""Builds the demo packs with the Sticker Shim tools.

images/<id>/  ->  packs/<id>/ (stickers.py make, then names and emojis from art/packs.py)
packs/        ->  site/ (stickers.py publish: index.json and pack folders); release.py zips site/

Usage: uv run build.py --tools ../sticker_shim/tools [--skip-make]
"""

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from art.packs import PACKS, Pack

ROOT: Path = Path(__file__).resolve().parent
# Publisher shown in the app for every demo pack.
PUBLISHER: str = "Sticker Shim demo"

type JsonObject = dict[str, object]


class BuildError(Exception):
    """Raised when the packs cannot be built."""


@dataclass(frozen=True, slots=True)
class Args:
    """Command-line arguments.

    Attributes:
        tools (Path): The tools/ folder of a sticker_shim checkout.
        skip_make (bool): Whether to only publish the committed packs/ to site/.
    """

    tools: Path
    skip_make: bool


def parse_args(argv: Sequence[str] | None = None) -> Args:
    """Parse command-line arguments.

    Args:
        argv (Sequence[str] | None): Argument vector, defaulting to ``sys.argv[1:]``.

    Returns:
        Args: The parsed arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    _ = parser.add_argument("--tools", type=Path, required=True, help="the tools/ folder of a sticker_shim checkout")
    _ = parser.add_argument("--skip-make", action="store_true", help="only publish the committed packs/ to site/")
    namespace = parser.parse_args(argv)
    return Args(tools=cast(Path, namespace.tools), skip_make=cast(bool, namespace.skip_make))


def stickers(tools: Path, *args: str) -> None:
    """Run one ``stickers.py`` command of the Sticker Shim tools.

    Args:
        tools (Path): The tools/ folder of a sticker_shim checkout.
        *args (str): Command and arguments for ``stickers.py``.

    Raises:
        BuildError: If the command fails.
    """
    try:
        _ = subprocess.run(["uv", "run", "--project", str(tools), str(tools / "stickers.py"), *args], check=True)
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"stickers.py {args[0]} failed with exit code {exc.returncode}") from exc


def make_pack(tools: Path, pack: Pack) -> None:
    """Build packs/<id>/ from images/<id>/ and set sticker names and emojis from art/packs.py.

    Args:
        tools (Path): The tools/ folder of a sticker_shim checkout.
        pack (Pack): The pack to build.

    Raises:
        BuildError: If ``stickers.py make`` fails or writes a sticker art/packs.py does not know.
    """
    out = ROOT / "packs" / pack.id
    stickers(
        tools,
        "make",
        str(ROOT / "images" / pack.id),
        "--out",
        str(out),
        "--id",
        pack.id,
        "--name",
        pack.name,
        "--publisher",
        PUBLISHER,
        "--margin",
        "0",
    )
    path = out / "contents.json"
    contents = cast(JsonObject, json.loads(path.read_text(encoding="utf-8")))
    by_stem = {s.stem: s for s in pack.stickers}
    for entry in cast(list[JsonObject], contents["stickers"]):
        stem = Path(cast(str, entry["image_file"])).stem
        if stem not in by_stem:
            raise BuildError(f"{path}: sticker {stem!r} is not in art/packs.py")
        entry["emojis"] = by_stem[stem].emojis
        entry["name"] = by_stem[stem].name
    _ = path.write_text(json.dumps(contents, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def publish(tools: Path) -> None:
    """Check packs/ and publish it to site/: index.json plus pack folders, zipped by release.py.

    Args:
        tools (Path): The tools/ folder of a sticker_shim checkout.
    """
    stickers(tools, "check", str(ROOT / "packs"))
    stickers(tools, "publish", str(ROOT / "packs"), "--out", str(ROOT / "site"), "--no-zip", "--force")


def main() -> int:
    """Run the build.

    Returns:
        int: Process exit code (0 success, 2 the build failed).
    """
    args = parse_args()
    tools = args.tools.resolve()
    if not (tools / "stickers.py").is_file():
        print(f"error: {tools / 'stickers.py'} not found; pass the tools/ folder of sticker_shim", file=sys.stderr)
        return 2
    try:
        if not args.skip_make:
            for pack in PACKS:
                make_pack(tools, pack)
        publish(tools)
    except BuildError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
