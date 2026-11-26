"""The demo packs: identifiers, names, stickers (file stem, sticker name, emojis, art) and groups."""

import math
from collections.abc import Callable
from dataclasses import dataclass

from art import draw as a
from art.draw import GINGER, GREY, HUSKY, svg

# Animated stickers: 24 frames at 12 fps give a 2 s loop, within the 3 s Telegram and Signal allow.
FRAMES: int = 24
FPS: int = 12


@dataclass(frozen=True, slots=True)
class Sticker:
    """One sticker of a pack.

    Attributes:
        stem (str): File name without extension, also the sort order.
        name (str): Sticker name shown in the app.
        emojis (list[str]): Emojis the sticker is filed under.
        still (str | None): SVG of a still sticker, or None if animated.
        frame (Callable[[float], str] | None): SVG of an animated sticker at phase t in [0, 1), or None if still.
        defs (str): Extra ``<defs>`` content of the art.
    """

    stem: str
    name: str
    emojis: list[str]
    still: str | None = None
    frame: Callable[[float], str] | None = None
    defs: str = ""


@dataclass(frozen=True, slots=True)
class Pack:
    """One demo pack.

    Attributes:
        id (str): Pack identifier, also the folder name.
        name (str): Pack name shown in the app.
        stickers (list[Sticker]): The stickers, in order.
        tray (str): Stem of the sticker used as the tray icon.
    """

    id: str
    name: str
    stickers: list[Sticker]
    tray: str

    @property
    def animated(self) -> bool:
        """Whether the pack holds animated stickers.

        Returns:
            bool: True if any sticker has a frame function.
        """
        return any(s.frame for s in self.stickers)


@dataclass(frozen=True, slots=True)
class Group:
    """A pack group as written to ``shim.json`` (field order is the JSON key order).

    Attributes:
        key (str): Group key, unique in the export.
        name (str): Group name shown in the app.
        parent (str | None): Key of the parent group, or None for a top group.
        packs (list[str]): Identifiers of the packs in the group.
    """

    key: str
    name: str
    parent: str | None
    packs: list[str]


def S(stem: str, name: str, emojis: str, body: str, defs: str = "") -> Sticker:
    """Build a still sticker.

    Args:
        stem (str): File name without extension.
        name (str): Sticker name.
        emojis (str): Space-separated emojis.
        body (str): SVG body of the art.
        defs (str): Extra ``<defs>`` content.

    Returns:
        Sticker: The sticker with its complete SVG.
    """
    return Sticker(stem, name, emojis.split(), still=svg(body, defs))


def A(stem: str, name: str, emojis: str, frame: Callable[[float], str], defs: str = "") -> Sticker:
    """Build an animated sticker.

    Args:
        stem (str): File name without extension.
        name (str): Sticker name.
        emojis (str): Space-separated emojis.
        frame (Callable[[float], str]): SVG body at phase t in [0, 1).
        defs (str): Extra ``<defs>`` content.

    Returns:
        Sticker: The sticker with a frame function that returns complete SVGs.
    """
    return Sticker(stem, name, emojis.split(), frame=lambda t: svg(frame(t), defs), defs=defs)


CATS: Pack = Pack(
    "demo-cats",
    "Demo Cats",
    [
        S("01_hi", "hi", "👋 😺", a.cat(paws="wave", extras=a.text(130, 90, "Hi!", 80, stroke="#ff8c42", rot=-10))),
        S("02_happy", "happy", "😊 😺", a.cat(eye="happy", tail=0.6)),
        S(
            "03_love",
            "love",
            "😍 ❤️",
            a.cat(
                eye="heart",
                blush_strong=True,
                extras=a.heart(90, 110, 1.3, rot=-15) + a.heart(420, 80, 1.0, rot=12) + a.heart(440, 170, 0.7),
            ),
        ),
        S(
            "04_lol",
            "lol",
            "😂 🤣",
            a.cat(eye="laugh", mouth_kind="open", tilt=-6, extras=a.drop(120, 230, 1.0) + a.drop(392, 230, 1.0)),
        ),
        S("05_sad", "sad", "😢 😿", a.cat(GREY, eye="sad", mouth_kind="frown", extras=a.drop(186, 300, 1.2))),
        S(
            "06_angry",
            "grumpy",
            "😠 😾",
            a.cat(
                GREY,
                eye="angry",
                mouth_kind="flat",
                extras='<path d="M410 90 l20 -30 l10 40 l30 -30" stroke="#e63946" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
            ),
        ),
        S(
            "07_wow",
            "wow",
            "😮 🙀",
            a.cat(eye="big", mouth_kind="o", paws="up", extras=a.sparkle(80, 120, 26) + a.sparkle(440, 110, 20)),
        ),
        S("08_sleepy", "sleepy", "😴 💤", a.cat(eye="closed", mouth_kind="cat", extras=a.zzz(360, 120))),
        S("09_cool", "cool", "😎", a.cat(eye="shades", mouth_kind="smile", extras=a.sparkle(420, 120, 24, "#ffffff"))),
        S("10_ok", "ok", "👍 👌", a.cat(eye="wink", mouth_kind="tongue", paws="thumb")),
        S(
            "11_coffee",
            "coffee",
            "☕ 🌅",
            a.cat(eye="closed", mouth_kind="cat", paws="none", extras=a.mug(256, 410, 0.9, "#3a86ff")),
        ),
        S(
            "12_thanks",
            "thanks",
            "🙏 💕",
            a.cat(GINGER, eye="happy", blush_strong=True, extras=a.text(256, 500, "Thanks!", 76, stroke="#ff4d6d")),
        ),
    ],
    "02_happy",
)

DOGS: Pack = Pack(
    "demo-dogs",
    "Demo Dogs",
    [
        S(
            "01_hello",
            "hello",
            "👋 🐶",
            a.dog(paws="wave", tail=1, extras=a.text(130, 90, "Hello!", 70, stroke="#2ec4b6", rot=-10)),
        ),
        S("02_happy", "happy", "😄 🐕", a.dog(eye="happy", mouth_kind="tongue", tail=1)),
        S(
            "03_love",
            "love",
            "🥰 ❤️",
            a.dog(
                eye="heart", blush_strong=True, extras=a.heart(80, 100, 1.2, rot=-12) + a.heart(430, 90, 1.0, rot=10)
            ),
        ),
        S(
            "04_lol",
            "lol",
            "😂",
            a.dog(eye="laugh", mouth_kind="open", tilt=6, extras=a.drop(110, 220) + a.drop(402, 220)),
        ),
        S("05_puppy_eyes", "puppy eyes", "🥺 🙏", a.dog(eye="big", mouth_kind="wobbly", tilt=-8, ear_lift=-6)),
        S("06_sad", "sad", "😢", a.dog(HUSKY, eye="sad", mouth_kind="frown", extras=a.drop(184, 290, 1.2))),
        S(
            "07_huh",
            "huh?",
            "🤔 ❓",
            a.dog(
                HUSKY, eye="normal", mouth_kind="flat", tilt=-14, extras=a.text(420, 120, "?", 120, stroke="#7b8cff")
            ),
        ),
        S("08_angry", "grr", "😠 🐺", a.dog(HUSKY, eye="angry", mouth_kind="frown")),
        S(
            "09_ball",
            "play?",
            "🎾 🐕",
            a.dog(
                eye="big",
                mouth_kind="open",
                tail=1,
                extras='<circle cx="410" cy="410" r="54" fill="#c6e83a"/>'
                '<path d="M370 376 q40 30 6 76 M450 444 q-40 -30 -6 -76" stroke="#ffffff" stroke-width="9" fill="none"/>',
            ),
        ),
        S("10_sleepy", "nap", "😴 💤", a.dog(eye="closed", mouth_kind="smile", extras=a.zzz(360, 110))),
        S("11_ok", "ok", "👍", a.dog(HUSKY, eye="wink", mouth_kind="tongue", paws="thumb")),
        S(
            "12_bye",
            "bye",
            "👋 🐾",
            a.dog(HUSKY, eye="happy", paws="wave", extras=a.text(140, 80, "Bye!", 80, stroke="#3a86ff", rot=-8)),
        ),
    ],
    "02_happy",
)

CHRISTMAS: Pack = Pack(
    "demo-christmas",
    "Demo Christmas",
    [
        S(
            "01_merry",
            "merry christmas",
            "🎄 🎅",
            a.cat(eye="happy", hat="santa", extras=a.text(256, 505, "Merry Xmas!", 66, stroke="#2a9d55")),
        ),
        S(
            "02_reindeer",
            "reindeer",
            "🦌 🐶",
            a.dog(
                eye="happy",
                mouth_kind="tongue",
                hat="antlers",
                extras='<circle cx="256" cy="262" r="24" fill="#e63946"/><circle cx="248" cy="254" r="7" fill="#fff" opacity=".6"/>',
            ),
        ),
        S("03_tree", "tree", "🎄", a.tree()),
        S("04_gift", "gift", "🎁", a.gift()),
        S("05_gingerbread", "gingerbread", "🍪 😋", a.gingerbread("happy")),
        S("06_candy_cane", "candy cane", "🍬", a.candy_cane()),
        S("07_stocking", "stocking", "🧦", a.stocking()),
        S("08_bauble", "bauble", "🔮 ✨", a.bauble()),
        S(
            "09_gift_cat",
            "for you",
            "🎁 😻",
            a.cat(
                eye="heart",
                paws="none",
                hat="santa",
                extras='<g transform="translate(256 420) scale(.42) translate(-256 -320)">'
                + a.gift("#2a9d55", "#ffd23f")
                + "</g>",
            ),
        ),
        S(
            "10_pip_santa",
            "ho ho ho",
            "🎅 🐦",
            a.pip(
                eye="happy", held="none", hat="santa", extras=a.text(130, 90, "Ho ho!", 66, stroke="#e63946", rot=-10)
            ),
            a.PIP_DEFS,
        ),
    ],
    "03_tree",
)


def _snowman(t: float) -> str:
    """Waving snowman in falling snow.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    return a.falling_snow(t, 10, 7) + a.snowman(
        "happy", arm=12 * math.sin(2 * math.pi * t), scarf_swing=10 * math.sin(2 * math.pi * t)
    )


def _flake(t: float) -> str:
    """Turning snowflake with a blue outline.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    return a.snowflake(256, 256, 190, "#7fc8f8", rot=60 * t, width=24) + a.snowflake(
        256, 256, 190, "#ffffff", rot=60 * t, width=10
    )


def _cocoa(t: float) -> str:
    """Hot cocoa with rising steam.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    return a.mug(256, 330, 1.6, "#e63946", "#7a4a2a", steam=t)


def _cat_cold(t: float) -> str:
    """Shivering grey cat with beanie and scarf.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    shiver = 5 * math.sin(2 * math.pi * t * 6)
    return (
        f'<g transform="translate({shiver:.1f} 0)">'
        + a.cat(
            GREY, eye="closed", mouth_kind="wobbly", hat="beanie", extras=a.scarf(256, 330, 220, "#e63946", "#ffffff")
        )
        + "</g>"
        + a.falling_snow(t, 8, 11)
    )


def _tree_lights(t: float) -> str:
    """Christmas tree with twinkling lights.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    return a.tree(lights_phase=t)


def _dog_snow(t: float) -> str:
    """Husky hopping in the snow.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    hop = -abs(math.sin(math.pi * t * 2)) * 40
    return (
        a.snow_ground()
        + a.dog(HUSKY, eye="happy", mouth_kind="open", tail=math.sin(2 * math.pi * t * 2), dy=hop - 10)
        + a.falling_snow(t, 8, 5)
    )


def _pip_snow(t: float) -> str:
    """Pip flapping in the snow.

    Args:
        t (float): Animation phase in [0, 1).

    Returns:
        str: SVG body of the frame.
    """
    return a.pip(
        eye="happy", held="none", hat="beanie", wing=0.5 + 0.5 * math.sin(2 * math.pi * t * 2)
    ) + a.falling_snow(t, 10, 9)


WINTER: Pack = Pack(
    "demo-winter",
    "Demo Snow Days",
    [
        A("01_snowman", "snowman", "⛄ ❄️", _snowman),
        A("02_snowflake", "snowflake", "❄️", _flake),
        A("03_cocoa", "hot cocoa", "☕ 🍫", _cocoa),
        A("04_cold_cat", "so cold", "🥶 🐱", _cat_cold),
        A("05_lights", "lights", "🎄 ✨", _tree_lights),
        A("06_snow_dog", "snow day", "🐶 ❄️", _dog_snow),
        A("07_pip_snow", "pip in snow", "🐦 ❄️", _pip_snow, a.PIP_DEFS),
    ],
    "02_snowflake",
)

PIP: Pack = Pack(
    "demo-pip",
    "Pip the Magpie",
    [
        S(
            "01_hi",
            "hi",
            "👋 🐦",
            a.pip(wing=1.0, held="none", beak_open=True, extras=a.text(120, 100, "Hi!", 80, stroke="#1fb7a5", rot=-10)),
            a.PIP_DEFS,
        ),
        S(
            "02_shiny",
            "shiny!",
            "✨ 🌟",
            a.pip(extras=a.sparkle(470, 150, 22) + a.sparkle(420, 290, 16) + a.sparkle(60, 200, 20, "#1fb7a5")),
            a.PIP_DEFS,
        ),
        S("03_love", "love", "😍 ❤️", a.pip(eye="heart", held="heart"), a.PIP_DEFS),
        S("04_happy", "happy", "😊", a.pip(eye="happy", held="none", beak_open=True, tilt=-6), a.PIP_DEFS),
        S(
            "05_wow",
            "wow",
            "😮",
            a.pip(eye="big", held="none", beak_open=True, extras=a.text(110, 110, "!", 140, stroke="#ffb347")),
            a.PIP_DEFS,
        ),
        S("06_sad", "sad", "😢", a.pip(eye="sad", held="none", extras=a.drop(330, 210, 1.1)), a.PIP_DEFS),
        S("07_sleepy", "sleepy", "😴", a.pip(eye="closed", held="none", extras=a.zzz(380, 90)), a.PIP_DEFS),
        S(
            "08_thanks",
            "thanks",
            "🙏",
            a.pip(eye="happy", extras=a.text(256, 500, "Thanks!", 76, stroke="#6a3fd1")),
            a.PIP_DEFS,
        ),
    ],
    "02_shiny",
)

PACKS: list[Pack] = [CATS, DOGS, CHRISTMAS, WINTER, PIP]

# Two top groups; "Christmas" is a subgroup of "Winter" to show nesting.
GROUPS: list[Group] = [
    Group("g1", "Pets", None, [CATS.id, DOGS.id, PIP.id]),
    Group("g2", "Winter", None, [WINTER.id]),
    Group("g3", "Christmas", "g2", [CHRISTMAS.id]),
]
