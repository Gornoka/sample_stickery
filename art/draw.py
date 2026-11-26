"""SVG art for the demo sticker packs: characters, expressions and props, drawn in code."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

# Shared palette: one outline ink and one blush so every character matches.
INK: str = "#2b1d14"
BLUSH: str = "#ff8fa3"
# Inter if installed, else the DejaVu Sans that ships with most Linux renderers.
FONT: str = "Inter, 'DejaVu Sans', Arial, sans-serif"

# White die-cut edge with a soft drop shadow, applied to the whole sticker body.
OUTLINE: str = (
    '<filter id="cut" x="-15%" y="-15%" width="130%" height="130%">'
    '<feMorphology in="SourceAlpha" operator="dilate" radius="11" result="d"/>'
    '<feFlood flood-color="#ffffff"/><feComposite in2="d" operator="in" result="w"/>'
    '<feMorphology in="SourceAlpha" operator="dilate" radius="13" result="d2"/>'
    '<feGaussianBlur in="d2" stdDeviation="4" result="b"/><feOffset dx="0" dy="4" in="b" result="s"/>'
    '<feFlood flood-color="#000000" flood-opacity=".22"/><feComposite in2="s" operator="in" result="sh"/>'
    '<feMerge><feMergeNode in="sh"/><feMergeNode in="w"/><feMergeNode in="SourceGraphic"/></feMerge>'
    "</filter>"
)


# Overlay markup that stays outside the die-cut filter (falling snow).
OVER: re.Pattern[str] = re.compile(r"<!--over-->(.*?)<!--/over-->", re.S)


def svg(body: str, defs: str = "") -> str:
    """Wrap a sticker body in a 512x512 SVG with the white die-cut edge.

    Everything inside gets the edge, except overlays marked ``<!--over-->`` (falling snow).

    Args:
        body (str): SVG markup of the sticker.
        defs (str): Extra ``<defs>`` content, such as gradients.

    Returns:
        str: A complete SVG document.
    """
    over = "".join(OVER.findall(body))
    body = OVER.sub("", body)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">'
        f"<defs>{OUTLINE}{defs}</defs>"
        f'<g transform="translate(256 256) scale(.86) translate(-256 -256)"><g filter="url(#cut)">{body}</g>{over}</g></svg>'
    )


# --- small props -------------------------------------------------------------


def heart(x: float, y: float, s: float = 1.0, color: str = "#ff4d6d", rot: float = 0) -> str:
    """Draw a heart.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        s (float): Scale factor.
        color (str): Fill colour.
        rot (float): Rotation in degrees.

    Returns:
        str: SVG markup.
    """
    return (
        f'<path transform="translate({x} {y}) rotate({rot}) scale({s})" fill="{color}" '
        'd="M0 12 C-30 -10 -22 -38 0 -24 C22 -38 30 -10 0 12 Z"/>'
    )


def star(x: float, y: float, r: float, color: str = "#ffd23f", rot: float = 0) -> str:
    """Draw a five-pointed star.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        r (float): Outer radius.
        color (str): Fill and stroke colour.
        rot (float): Rotation in degrees.

    Returns:
        str: SVG markup.
    """
    pts: list[str] = []
    for i in range(10):
        a = math.pi / 5 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{rr * math.cos(a):.1f},{rr * math.sin(a):.1f}")
    return (
        f'<polygon transform="translate({x} {y}) rotate({rot})" points="{" ".join(pts)}" fill="{color}" '
        f'stroke="{color}" stroke-width="{r * 0.18:.1f}" stroke-linejoin="round"/>'
    )


def sparkle(x: float, y: float, r: float, color: str = "#ffd23f") -> str:
    """Draw a four-pointed sparkle.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        r (float): Radius of the points.
        color (str): Fill colour.

    Returns:
        str: SVG markup.
    """
    return (
        f'<path transform="translate({x} {y})" fill="{color}" d="M0 {-r} Q{r * 0.15} {-r * 0.15} {r} 0 '
        f'Q{r * 0.15} {r * 0.15} 0 {r} Q{-r * 0.15} {r * 0.15} {-r} 0 Q{-r * 0.15} {-r * 0.15} 0 {-r} Z"/>'
    )


def drop(x: float, y: float, s: float = 1.0, color: str = "#5ec8ff") -> str:
    """Draw a tear or sweat drop.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        s (float): Scale factor.
        color (str): Fill colour.

    Returns:
        str: SVG markup.
    """
    return f'<path transform="translate({x} {y}) scale({s})" fill="{color}" d="M0 -22 C10 -6 16 2 16 10 A16 16 0 0 1 -16 10 C-16 2 -10 -6 0 -22 Z"/>'


def text(
    x: float, y: float, s: str, size: int = 64, color: str = "#ffffff", stroke: str = "#ff4d6d", rot: float = 0
) -> str:
    """Draw bold outlined text.

    Args:
        x (float): Anchor x (text is centred on it).
        y (float): Baseline y.
        s (str): The text.
        size (int): Font size.
        color (str): Fill colour.
        stroke (str): Outline colour.
        rot (float): Rotation in degrees around the anchor.

    Returns:
        str: SVG markup.
    """
    common = f'x="{x}" y="{y}" font-family="{FONT}" font-weight="900" font-size="{size}" text-anchor="middle" transform="rotate({rot} {x} {y})"'
    return (
        f'<text {common} fill="{stroke}" stroke="{stroke}" stroke-width="{size * 0.32:.0f}" stroke-linejoin="round">{s}</text>'
        f'<text {common} fill="{color}">{s}</text>'
    )


def zzz(x: float, y: float) -> str:
    """Draw three rising "Z" letters.

    Args:
        x (float): x of the first letter.
        y (float): Baseline y of the first letter.

    Returns:
        str: SVG markup.
    """
    return "".join(
        f'<text x="{x + i * 34}" y="{y - i * 40}" font-family="{FONT}" font-weight="900" font-size="{44 + i * 14}" '
        f'fill="#7b8cff">Z</text>'
        for i in range(3)
    )


def snowflake(x: float, y: float, r: float, color: str = "#ffffff", rot: float = 0, width: float = 0) -> str:
    """Draw a six-armed snowflake.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        r (float): Arm length.
        color (str): Stroke colour.
        rot (float): Rotation in degrees.
        width (float): Stroke width; 0 picks one from ``r``.

    Returns:
        str: SVG markup.
    """
    w = width or max(2.5, r * 0.14)
    arms: list[str] = []
    for i in range(6):
        a = 60 * i
        b = r * 0.55
        arms.append(
            f'<g transform="rotate({a})"><line x1="0" y1="0" x2="0" y2="{-r}"/>'
            f'<line x1="0" y1="{-b}" x2="{r * 0.28}" y2="{-b - r * 0.25}"/>'
            f'<line x1="0" y1="{-b}" x2="{-r * 0.28}" y2="{-b - r * 0.25}"/></g>'
        )
    return (
        f'<g transform="translate({x} {y}) rotate({rot})" stroke="{color}" stroke-width="{w:.1f}" '
        f'stroke-linecap="round">{"".join(arms)}</g>'
    )


def mug(
    x: float, y: float, s: float = 1.0, color: str = "#e94f4f", drink: str = "#7a4a2a", steam: float | None = 0.0
) -> str:
    """Draw a mug with a drink and optional animated steam.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        s (float): Scale factor.
        color (str): Mug colour.
        drink (str): Drink colour.
        steam (float | None): Steam animation phase in [0, 1), or None for no steam.

    Returns:
        str: SVG markup.
    """
    out = f'<g transform="translate({x} {y}) scale({s})">'
    if steam is not None:
        for i, dx in enumerate((-28, 0, 28)):
            ph = steam * 2 * math.pi + i * 2.1
            o = 0.35 + 0.45 * (0.5 + 0.5 * math.sin(ph))
            yy = -8 * math.sin(ph)
            out += (
                f'<path d="M{dx} {-70 + yy} q-14 -22 0 -42 q14 -20 0 -42" stroke="#c9d3df" stroke-width="10" '
                f'fill="none" stroke-linecap="round" opacity="{o:.2f}"/>'
            )
    out += (
        '<path d="M48 -30 a30 30 0 0 1 0 60" stroke="#ffffff" stroke-width="26" fill="none"/>'
        f'<path d="M48 -30 a30 30 0 0 1 0 60" stroke="{color}" stroke-width="14" fill="none"/>'
        f'<path d="M-62 -52 H62 V30 a40 40 0 0 1 -40 40 H-22 a40 40 0 0 1 -40 -40 Z" fill="{color}"/>'
        f'<ellipse cx="0" cy="-52" rx="62" ry="14" fill="{drink}"/>'
        '<ellipse cx="-14" cy="-55" rx="16" ry="6" fill="#ffffff" opacity=".85"/>'
        '<ellipse cx="14" cy="-51" rx="12" ry="5" fill="#ffffff" opacity=".85"/>'
        '<path d="M-44 -30 v60" stroke="#ffffff" stroke-width="10" stroke-linecap="round" opacity=".35"/>'
        "</g>"
    )
    return out


def santa_hat(x: float, y: float, s: float = 1.0, rot: float = 0, bob: float = 0) -> str:
    """Draw a Santa hat.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        s (float): Scale factor.
        rot (float): Rotation in degrees.
        bob (float): Horizontal offset of the bobble.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">'
        f'<path d="M-120 0 C-100 -110 20 -150 110 -90 C130 -70 {150 + bob} -20 {150 + bob} 10 L110 -40 C90 -20 80 -10 120 0 Z" fill="#e63946"/>'
        '<path d="M-60 -60 C-20 -110 40 -120 80 -100" stroke="#ff6b78" stroke-width="10" fill="none" stroke-linecap="round" opacity=".7"/>'
        '<rect x="-138" y="-22" width="276" height="50" rx="25" fill="#ffffff"/>'
        f'<circle cx="{150 + bob}" cy="22" r="30" fill="#ffffff"/>'
        "</g>"
    )


def antlers(x: float, y: float, s: float = 1.0) -> str:
    """Draw a pair of antlers.

    Args:
        x (float): Centre x between the antlers.
        y (float): y of the antler bases.
        s (float): Scale factor.

    Returns:
        str: SVG markup.
    """
    one = (
        '<path d="M0 0 C-10 -60 -50 -90 -80 -140 M-30 -60 C-60 -70 -90 -60 -110 -80 M-55 -105 C-40 -130 -40 -150 -30 -170" '
        'stroke="#8a5a32" stroke-width="20" fill="none" stroke-linecap="round"/>'
    )
    return (
        f'<g transform="translate({x} {y}) scale({s})"><g transform="translate(-70 0)">{one}</g>'
        f'<g transform="translate(70 0) scale(-1 1)">{one}</g></g>'
    )


def scarf(cx: float, y: float, w: float, color: str = "#e63946", stripe: str = "#ffffff", swing: float = 0) -> str:
    """Draw a striped scarf with a hanging end.

    Args:
        cx (float): Centre x of the neck.
        y (float): Top y of the scarf.
        w (float): Width around the neck.
        color (str): Scarf colour.
        stripe (str): Stripe colour.
        swing (float): Sideways offset of the hanging end.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g><path d="M{cx - w / 2} {y} Q{cx} {y + 40} {cx + w / 2} {y} L{cx + w / 2 + 4} {y + 36} Q{cx} {y + 80} {cx - w / 2 - 4} {y + 36} Z" fill="{color}"/>'
        f'<path d="M{cx + w / 4} {y + 40} L{cx + w / 4 + 10 + swing} {y + 140} L{cx + w / 4 + 60 + swing} {y + 128} L{cx + w / 4 + 44} {y + 34} Z" fill="{color}"/>'
        f'<path d="M{cx + w / 4 + 6 + swing * 0.4} {y + 80} L{cx + w / 4 + 52 + swing * 0.6} {y + 72} M{cx + w / 4 + 10 + swing * 0.7} {y + 108} L{cx + w / 4 + 56 + swing * 0.8} {y + 100}" '
        f'stroke="{stripe}" stroke-width="10" stroke-linecap="round"/>'
        f'<path d="M{cx - w / 2 + 20} {y + 22} Q{cx} {y + 58} {cx + w / 2 - 20} {y + 22}" stroke="{stripe}" stroke-width="10" fill="none" stroke-linecap="round"/></g>'
    )


def beanie(x: float, y: float, s: float = 1.0, color: str = "#3a86ff", band: str = "#ffffff") -> str:
    """Draw a beanie with a bobble.

    Args:
        x (float): Centre x in sticker units (0..512).
        y (float): Centre y in sticker units (0..512).
        s (float): Scale factor.
        color (str): Hat colour.
        band (str): Band and bobble colour.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g transform="translate({x} {y}) scale({s})">'
        f'<path d="M-130 10 C-130 -120 130 -120 130 10 Z" fill="{color}"/>'
        '<path d="M-60 -70 v60 M0 -90 v80 M60 -70 v60" stroke="#ffffff" stroke-width="8" opacity=".3" stroke-linecap="round"/>'
        f'<rect x="-142" y="-10" width="284" height="46" rx="20" fill="{band}"/>'
        f'<circle cx="0" cy="-110" r="32" fill="{band}"/>'
        "</g>"
    )


# --- faces -------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Face:
    """Eye and mouth anchors of a character head.

    Attributes:
        lx (float): x of the left eye.
        rx (float): x of the right eye.
        ey (float): y of both eyes.
        my (float): y of the mouth.
        eye (float): Eye scale factor.
    """

    lx: float
    rx: float
    ey: float
    my: float
    eye: float = 1.0


def eyes(f: Face, kind: str) -> str:
    """Draw both eyes of a face.

    Args:
        f (Face): Anchors of the face.
        kind (str): normal, big, happy, closed, laugh, heart, sad, angry, wink or shades.

    Returns:
        str: SVG markup.
    """
    s = f.eye
    out: list[str] = []
    for i, x in enumerate((f.lx, f.rx)):
        k = kind
        if kind == "wink":
            k = "normal" if i == 0 else "happy"
        if k == "normal":
            out.append(
                f'<ellipse cx="{x}" cy="{f.ey}" rx="{22 * s}" ry="{28 * s}" fill="{INK}"/>'
                f'<circle cx="{x + 8 * s}" cy="{f.ey - 11 * s}" r="{9 * s}" fill="#fff"/>'
                f'<circle cx="{x - 7 * s}" cy="{f.ey + 10 * s}" r="{4 * s}" fill="#fff" opacity=".8"/>'
            )
        elif k == "big":
            out.append(
                f'<circle cx="{x}" cy="{f.ey}" r="{34 * s}" fill="#fff" stroke="{INK}" stroke-width="7"/>'
                f'<circle cx="{x}" cy="{f.ey + 4}" r="{12 * s}" fill="{INK}"/>'
                f'<circle cx="{x + 4}" cy="{f.ey - 1}" r="{4 * s}" fill="#fff"/>'
            )
        elif k == "happy":
            out.append(
                f'<path d="M{x - 24 * s} {f.ey + 8} Q{x} {f.ey - 26 * s} {x + 24 * s} {f.ey + 8}" stroke="{INK}" '
                f'stroke-width="10" fill="none" stroke-linecap="round"/>'
            )
        elif k == "closed":
            out.append(
                f'<path d="M{x - 24 * s} {f.ey} Q{x} {f.ey + 20 * s} {x + 24 * s} {f.ey}" stroke="{INK}" '
                f'stroke-width="10" fill="none" stroke-linecap="round"/>'
            )
        elif k == "laugh":
            d = 1 if i == 0 else -1
            out.append(
                f'<path d="M{x - 20 * d} {f.ey - 18} L{x + 18 * d} {f.ey} L{x - 20 * d} {f.ey + 18}" stroke="{INK}" '
                f'stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            )
        elif k == "heart":
            out.append(heart(x, f.ey + 4, 1.25 * s))
        elif k == "sad":
            out.append(
                f'<ellipse cx="{x}" cy="{f.ey + 4}" rx="{22 * s}" ry="{26 * s}" fill="{INK}"/>'
                f'<circle cx="{x + 7 * s}" cy="{f.ey - 6}" r="{10 * s}" fill="#fff"/>'
                f'<circle cx="{x - 7 * s}" cy="{f.ey + 12}" r="{5 * s}" fill="#fff"/>'
            )
            d = 1 if i == 0 else -1
            out.append(
                f'<path d="M{x - 26 * d} {f.ey - 30} L{x + 16 * d} {f.ey - 44}" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
            )
        elif k == "angry":
            out.append(
                f'<ellipse cx="{x}" cy="{f.ey + 6}" rx="{20 * s}" ry="{22 * s}" fill="{INK}"/>'
                f'<circle cx="{x + 6}" cy="{f.ey - 2}" r="{7 * s}" fill="#fff"/>'
            )
            d = 1 if i == 0 else -1
            out.append(
                f'<path d="M{x - 28 * d} {f.ey - 40} L{x + 18 * d} {f.ey - 22}" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
            )
        elif k == "shades":
            pass
    if kind == "shades":
        out.append(
            f'<path d="M{f.lx - 44} {f.ey - 24} H{f.rx + 44}" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="M{f.lx - 40} {f.ey - 24} H{f.lx + 40} V{f.ey + 4} a24 24 0 0 1 -24 24 H{f.lx - 16} a24 24 0 0 1 -24 -24 Z" fill="{INK}"/>'
            f'<path d="M{f.rx - 40} {f.ey - 24} H{f.rx + 40} V{f.ey + 4} a24 24 0 0 1 -24 24 H{f.rx - 16} a24 24 0 0 1 -24 -24 Z" fill="{INK}"/>'
            f'<path d="M{f.lx - 26} {f.ey - 14} l18 0 M{f.rx - 26} {f.ey - 14} l18 0" stroke="#fff" stroke-width="7" stroke-linecap="round" opacity=".6"/>'
        )
    return "".join(out)


def blush(f: Face, strong: bool = False) -> str:
    """Draw blush on both cheeks.

    Args:
        f (Face): Anchors of the face.
        strong (bool): Whether the blush is more opaque.

    Returns:
        str: SVG markup.
    """
    o = ".85" if strong else ".55"
    return (
        f'<ellipse cx="{f.lx - 26}" cy="{f.ey + 46}" rx="24" ry="13" fill="{BLUSH}" opacity="{o}"/>'
        f'<ellipse cx="{f.rx + 26}" cy="{f.ey + 46}" rx="24" ry="13" fill="{BLUSH}" opacity="{o}"/>'
    )


def mouth(cx: float, y: float, kind: str) -> str:
    """Draw a mouth.

    Args:
        cx (float): Centre x.
        y (float): Top y.
        kind (str): cat, smile, open, tongue, o, frown, wobbly or flat.

    Returns:
        str: SVG markup.

    Raises:
        ValueError: If ``kind`` is unknown.
    """
    if kind == "cat":
        return (
            f'<path d="M{cx - 30} {y} q15 18 30 0 q15 18 30 0" stroke="{INK}" stroke-width="8" fill="none" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if kind == "smile":
        return (
            f'<path d="M{cx - 30} {y} q30 28 60 0" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        )
    if kind == "open":
        return (
            f'<path d="M{cx - 38} {y - 4} Q{cx} {y + 70} {cx + 38} {y - 4} Z" fill="#7a2335" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<path d="M{cx - 20} {y + 30} Q{cx} {y + 14} {cx + 20} {y + 30} Q{cx} {y + 46} {cx - 20} {y + 30} Z" fill="#ff7b93"/>'
        )
    if kind == "tongue":
        return (
            f'<path d="M{cx - 30} {y} q15 18 30 0 q15 18 30 0" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'
            f'<path d="M{cx - 14} {y + 10} v26 a14 14 0 0 0 28 0 v-26 Z" fill="#ff7b93" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M{cx} {y + 14} v18" stroke="#e0566f" stroke-width="4" stroke-linecap="round"/>'
        )
    if kind == "o":
        return f'<ellipse cx="{cx}" cy="{y + 16}" rx="18" ry="24" fill="#7a2335" stroke="{INK}" stroke-width="8"/>'
    if kind == "frown":
        return f'<path d="M{cx - 28} {y + 20} q28 -24 56 0" stroke="{INK}" stroke-width="9" fill="none" stroke-linecap="round"/>'
    if kind == "wobbly":
        return f'<path d="M{cx - 34} {y + 14} q11 -12 22 0 q12 12 24 0 q11 -12 22 0" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'
    if kind == "flat":
        return f'<path d="M{cx - 22} {y + 10} h44" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
    raise ValueError(kind)


# --- characters --------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Look:
    """Colours of a cat or dog.

    Attributes:
        fur (str): Main fur colour.
        shade (str): Darker fur for paw lines and dog ears.
        inner (str): Inner ear colour.
        belly (str): Belly and muzzle colour.
        stripe (str | None): Tabby stripes (cats), or None.
        patch (str | None): Eye patch (dogs), or None.
    """

    fur: str
    shade: str
    inner: str = "#ffb3c1"
    belly: str = "#fff4e6"
    stripe: str | None = None
    patch: str | None = None


# Coat presets for cat() and dog(); dog() checks for HUSKY by identity.
GINGER: Look = Look("#f6a24b", "#e07f26", stripe="#d9731c")
GREY: Look = Look("#a9b4c8", "#8592aa", stripe="#77839b")
BEAGLE: Look = Look("#f2d0a4", "#b46b37", patch="#b46b37", inner="#8f4f26")
HUSKY: Look = Look("#9fb1c9", "#6f84a3", belly="#ffffff", inner="#ffffff")


def cat(
    look: Look = GINGER,
    eye: str = "normal",
    mouth_kind: str = "cat",
    paws: str = "down",
    extras: str = "",
    under: str = "",
    tail: float = 0.0,
    blush_strong: bool = False,
    tilt: float = 0.0,
    dy: float = 0.0,
    hat: str = "",
) -> str:
    """Draw a round cat: body, head, ears and tail.

    Args:
        look (Look): Colours.
        eye (str): Eye kind, see ``eyes``.
        mouth_kind (str): Mouth kind, see ``mouth``.
        paws (str): down, wave, up, hold, thumb or none.
        extras (str): SVG drawn on top of the cat.
        under (str): SVG drawn behind the cat.
        tail (float): Tail swing, 0 at rest.
        blush_strong (bool): Whether the blush is more opaque.
        tilt (float): Rotation in degrees.
        dy (float): Vertical offset.
        hat (str): santa, beanie, antlers or "" for none.

    Returns:
        str: SVG markup.
    """
    f = Face(200, 312, 238, 280)
    tw = 30 * tail
    body = (
        f'<path d="M340 420 C420 420 {440 + tw} 330 {420 + tw} 270 C{410 + tw} 240 {380 + tw} 250 {392 + tw} 280 '
        f'C{404 + tw} 320 390 380 330 390 Z" fill="{look.fur}"/>'
        f'<ellipse cx="256" cy="400" rx="118" ry="78" fill="{look.fur}"/>'
        f'<ellipse cx="256" cy="414" rx="66" ry="52" fill="{look.belly}"/>'
    )
    head = (
        f'<path d="M128 170 L140 60 Q146 44 160 54 L238 112 Z" fill="{look.fur}"/>'
        f'<path d="M384 170 L372 60 Q366 44 352 54 L274 112 Z" fill="{look.fur}"/>'
        f'<path d="M146 140 L152 82 L204 120 Z" fill="{look.inner}"/>'
        f'<path d="M366 140 L360 82 L308 120 Z" fill="{look.inner}"/>'
        f'<ellipse cx="256" cy="230" rx="160" ry="132" fill="{look.fur}"/>'
    )
    if look.stripe:
        head += (
            f'<path d="M256 104 v34 M226 108 q4 22 10 30 M286 108 q-4 22 -10 30" stroke="{look.stripe}" stroke-width="12" '
            'stroke-linecap="round" fill="none"/>'
            f'<path d="M100 220 h34 M104 250 h28 M412 220 h-34 M408 250 h-28" stroke="{look.stripe}" stroke-width="11" stroke-linecap="round"/>'
        )
    muzzle = (
        f'<ellipse cx="236" cy="{f.my + 6}" rx="34" ry="26" fill="{look.belly}"/>'
        f'<ellipse cx="276" cy="{f.my + 6}" rx="34" ry="26" fill="{look.belly}"/>'
        f'<path d="M244 {f.my - 16} h24 l-12 12 Z" fill="#ff7b93" stroke="#ff7b93" stroke-width="8" stroke-linejoin="round"/>'
    )
    whisk = (
        f'<path d="M180 {f.my} l-62 -10 M180 {f.my + 14} l-60 8 M332 {f.my} l62 -10 M332 {f.my + 14} l60 8" '
        f'stroke="{INK}" stroke-width="4" stroke-linecap="round" opacity=".55"/>'
    )
    face = muzzle + whisk + eyes(f, eye) + blush(f, blush_strong) + mouth(256, f.my - 2, mouth_kind)
    hats = {
        "santa": santa_hat(256, 128, 0.95, -8),
        "beanie": beanie(256, 118, 0.98),
        "antlers": antlers(256, 108, 0.9),
    }
    top = hats.get(hat, "")
    behind = antlers(256, 118, 0.9) if hat == "antlers" else ""
    if hat == "antlers":
        top = ""
    return (
        f'<g transform="translate(0 {dy}) rotate({tilt} 256 300)">{under}{body}{behind}{head}{face}{top}'
        f"{_paws(look, paws)}{extras}</g>"
    )


def dog(
    look: Look = BEAGLE,
    eye: str = "normal",
    mouth_kind: str = "smile",
    paws: str = "down",
    extras: str = "",
    under: str = "",
    tail: float = 0.0,
    blush_strong: bool = False,
    tilt: float = 0.0,
    dy: float = 0.0,
    hat: str = "",
    ear_lift: float = 0.0,
) -> str:
    """Draw a round dog with floppy ears (pointed ears for the husky).

    Args:
        look (Look): Colours; ``HUSKY`` also changes ears and face.
        eye (str): Eye kind, see ``eyes``.
        mouth_kind (str): Mouth kind, see ``mouth`` ("cat" becomes "smile").
        paws (str): down, wave, up, hold, thumb or none.
        extras (str): SVG drawn on top of the dog.
        under (str): SVG drawn behind the dog.
        tail (float): Tail swing, 0 at rest.
        blush_strong (bool): Whether the blush is more opaque.
        tilt (float): Rotation in degrees.
        dy (float): Vertical offset.
        hat (str): santa, beanie, antlers or "" for none.
        ear_lift (float): Rotation of the floppy ears in degrees.

    Returns:
        str: SVG markup.
    """
    f = Face(204, 308, 222, 296)
    tw = 26 * tail
    ear = look.inner if look is HUSKY else look.shade
    body = (
        f'<path d="M350 400 C390 380 {420 + tw} 330 {430 + tw} 290" stroke="{look.fur}" stroke-width="34" fill="none" stroke-linecap="round"/>'
        f'<ellipse cx="256" cy="402" rx="116" ry="76" fill="{look.fur}"/>'
        f'<ellipse cx="256" cy="416" rx="64" ry="50" fill="{look.belly}"/>'
    )
    if look is HUSKY:
        ears = (
            f'<path d="M120 150 L136 40 Q142 26 156 36 L230 104 Z" fill="{look.shade}"/>'
            f'<path d="M392 150 L376 40 Q370 26 356 36 L282 104 Z" fill="{look.shade}"/>'
            '<path d="M140 128 L150 66 L200 108 Z" fill="#ffd9e0"/><path d="M372 128 L362 66 L312 108 Z" fill="#ffd9e0"/>'
        )
        front_ears = ""
    else:
        ears = ""
        front_ears = (
            f'<path transform="rotate({-ear_lift} 140 120)" d="M150 104 C90 100 70 180 84 250 C92 290 130 290 142 250 C150 210 170 150 180 120 Z" fill="{ear}"/>'
            f'<path transform="rotate({ear_lift} 372 120)" d="M362 104 C422 100 442 180 428 250 C420 290 382 290 370 250 C362 210 342 150 332 120 Z" fill="{ear}"/>'
        )
    head = f'<ellipse cx="256" cy="230" rx="150" ry="136" fill="{look.fur}"/>'
    if look is HUSKY:
        head += '<path d="M256 120 C210 150 200 200 190 240 C220 230 240 250 256 300 C272 250 292 230 322 240 C312 200 302 150 256 120 Z" fill="#ffffff"/>'
    if look.patch:
        head += f'<path d="M290 160 C340 150 370 190 362 240 C340 250 310 240 296 222 C284 200 280 176 290 160 Z" fill="{look.patch}"/>'
    muzzle = (
        f'<ellipse cx="256" cy="{f.my - 6}" rx="74" ry="56" fill="{look.belly}"/>'
        f'<ellipse cx="256" cy="{f.my - 34}" rx="28" ry="19" fill="{INK}"/>'
        f'<ellipse cx="248" cy="{f.my - 40}" rx="9" ry="5" fill="#fff" opacity=".6"/>'
        f'<path d="M256 {f.my - 16} v14" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
    )
    m = {"cat": "smile"}.get(mouth_kind, mouth_kind)
    face = muzzle + eyes(f, eye) + blush(f, blush_strong) + mouth(256, f.my, m)
    hats = {"santa": santa_hat(256, 116, 0.95, 8), "beanie": beanie(256, 112, 0.95, "#2ec4b6")}
    top = hats.get(hat, "")
    behind = antlers(256, 104, 0.9) if hat == "antlers" else ""
    return (
        f'<g transform="translate(0 {dy}) rotate({tilt} 256 300)">{under}{body}{behind}{ears}{head}{front_ears}{face}{top}'
        f"{_paws(look, paws)}{extras}</g>"
    )


def _paws(look: Look, paws: str) -> str:
    """Draw the paws of a cat or dog.

    Args:
        look (Look): Colours.
        paws (str): down, wave, up, hold, thumb; anything else draws none.

    Returns:
        str: SVG markup.
    """

    def paw(x: float, y: float, rot: float = 0) -> str:
        """Draw one paw.

        Args:
            x (float): Centre x.
            y (float): Centre y.
            rot (float): Rotation in degrees.

        Returns:
            str: SVG markup.
        """
        return (
            f'<g transform="translate({x} {y}) rotate({rot})"><ellipse rx="34" ry="28" fill="{look.fur}"/>'
            f'<path d="M-10 -6 v14 M10 -6 v14" stroke="{look.shade}" stroke-width="5" stroke-linecap="round"/></g>'
        )

    if paws == "down":
        return paw(206, 448) + paw(306, 448)
    if paws == "wave":
        return (
            paw(206, 448)
            + f'<path d="M350 380 Q410 330 420 260" stroke="{look.fur}" stroke-width="56" fill="none" stroke-linecap="round"/>'
            + paw(420, 246, -20)
            + '<path d="M450 190 q22 10 30 34 M466 168 q30 14 40 46" stroke="#ffb703" stroke-width="9" fill="none" stroke-linecap="round"/>'
        )
    if paws == "up":
        return (
            f'<path d="M160 380 Q110 320 120 250 M352 380 Q402 320 392 250" stroke="{look.fur}" stroke-width="56" fill="none" stroke-linecap="round"/>'
            + paw(118, 240, 20)
            + paw(394, 240, -20)
        )
    if paws == "hold":
        return paw(196, 392, 30) + paw(316, 392, -30)
    if paws == "thumb":
        return (
            paw(206, 448)
            + f'<path d="M352 400 Q400 380 404 330" stroke="{look.fur}" stroke-width="56" fill="none" stroke-linecap="round"/>'
            + f'<g transform="translate(404 316)"><ellipse rx="38" ry="34" fill="{look.fur}"/>'
            f'<rect x="-14" y="-82" width="28" height="60" rx="14" fill="{look.fur}"/>'
            f'<path d="M-22 -2 h44 M-22 14 h40" stroke="{look.shade}" stroke-width="5" stroke-linecap="round"/></g>'
        )
    return ""


# --- winter and Christmas objects -------------------------------------------


def tree(lights_phase: float | None = None) -> str:
    """Draw a Christmas tree with baubles and a star.

    Args:
        lights_phase (float | None): Twinkle animation phase in [0, 1), or None for steady lights.

    Returns:
        str: SVG markup.
    """
    out = (
        '<rect x="226" y="400" width="60" height="60" rx="10" fill="#8a5a32"/>'
        '<path d="M256 70 L380 220 H330 L420 330 H360 L450 420 H62 L152 330 H92 L182 220 H132 Z" fill="#2a9d55" '
        'stroke="#2a9d55" stroke-width="24" stroke-linejoin="round"/>'
        '<path d="M256 70 L330 160 M190 260 L300 300 M130 380 L380 360" stroke="#38b864" stroke-width="10" stroke-linecap="round" opacity=".6"/>'
        '<path d="M160 230 Q260 270 350 220 M120 340 Q250 380 400 330" stroke="#ffd23f" stroke-width="6" fill="none" stroke-dasharray="2 18" stroke-linecap="round"/>'
    )
    colors = ["#ff4d6d", "#ffd23f", "#4cc9f0", "#c77dff", "#ff9f1c"]
    balls = [
        (200, 200),
        (300, 180),
        (170, 300),
        (256, 270),
        (340, 300),
        (130, 400),
        (220, 380),
        (300, 400),
        (390, 390),
        (256, 150),
    ]
    for i, (x, y) in enumerate(balls):
        c = colors[i % len(colors)]
        o = 1.0
        if lights_phase is not None:
            o = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(2 * math.pi * (lights_phase + i * 0.37)))
        out += f'<circle cx="{x}" cy="{y}" r="17" fill="{c}" opacity="{o:.2f}"/><circle cx="{x - 5}" cy="{y - 5}" r="5" fill="#fff" opacity="{0.8 * o:.2f}"/>'
    glow = 1.0 if lights_phase is None else 0.75 + 0.25 * math.sin(2 * math.pi * lights_phase)
    out += star(256, 66, 46 * glow + 8, "#ffd23f")
    return out


def gift(color: str = "#e63946", ribbon: str = "#ffd23f", lid_lift: float = 0.0) -> str:
    """Draw a wrapped gift.

    Args:
        color (str): Paper colour.
        ribbon (str): Ribbon colour.
        lid_lift (float): How far the lid is lifted.

    Returns:
        str: SVG markup.
    """
    return (
        f'<rect x="120" y="230" width="272" height="220" rx="18" fill="{color}"/>'
        f'<rect x="232" y="230" width="48" height="220" fill="{ribbon}"/>'
        f'<g transform="translate(0 {-lid_lift})">'
        f'<path d="M256 180 C200 100 140 120 170 170 C180 186 220 186 256 180 Z" fill="{ribbon}"/>'
        f'<path d="M256 180 C312 100 372 120 342 170 C332 186 292 186 256 180 Z" fill="{ribbon}"/>'
        f'<rect x="100" y="176" width="312" height="70" rx="16" fill="{color}"/>'
        f'<rect x="232" y="176" width="48" height="70" fill="{ribbon}"/>'
        '<rect x="116" y="188" width="120" height="14" rx="7" fill="#fff" opacity=".3"/></g>'
    )


def gingerbread(eye: str = "normal", arm: float = 0.0) -> str:
    """Draw a gingerbread figure.

    Args:
        eye (str): Eye kind, see ``eyes``.
        arm (float): Arm rotation in degrees.

    Returns:
        str: SVG markup.
    """
    f = Face(226, 286, 150, 186, eye=0.7)
    return (
        '<g fill="#c47a3c">'
        '<circle cx="256" cy="160" r="86"/>'
        f'<path transform="rotate({-arm} 180 270)" d="M180 250 L80 220 a34 34 0 0 0 -10 64 L180 310 Z"/>'
        f'<path transform="rotate({arm} 332 270)" d="M332 250 L432 220 a34 34 0 0 1 10 64 L332 310 Z"/>'
        '<path d="M170 240 H342 Q350 330 330 360 L380 440 a36 36 0 0 1 -60 34 L256 400 L192 474 a36 36 0 0 1 -60 -34 L182 360 Q162 330 170 240 Z"/>'
        "</g>"
        '<g stroke="#ffffff" stroke-width="9" fill="none" stroke-linecap="round">'
        '<path d="M86 236 q-10 16 0 32 M426 236 q10 16 0 32 M146 438 q14 14 0 28 M366 438 q-14 14 0 28"/></g>'
        '<circle cx="256" cy="280" r="12" fill="#e63946"/><circle cx="256" cy="320" r="12" fill="#2a9d55"/>'
        '<circle cx="256" cy="360" r="12" fill="#3a86ff"/>'
        + eyes(f, eye)
        + mouth(256, f.my, "smile")
        + f'<ellipse cx="{f.lx - 22}" cy="{f.ey + 34}" rx="16" ry="9" fill="#ff8fa3" opacity=".7"/>'
        + f'<ellipse cx="{f.rx + 22}" cy="{f.ey + 34}" rx="16" ry="9" fill="#ff8fa3" opacity=".7"/>'
    )


def candy_cane() -> str:
    """Draw a candy cane with a holly bow.

    Returns:
        str: SVG markup.
    """
    return (
        '<path d="M300 470 V200 A80 80 0 0 0 140 200" stroke="#ffffff" stroke-width="64" fill="none" stroke-linecap="round"/>'
        '<path d="M300 470 V200 A80 80 0 0 0 140 200" stroke="#e63946" stroke-width="64" fill="none" stroke-linecap="round" stroke-dasharray="36 36"/>'
        '<path d="M282 440 V210" stroke="#fff" stroke-width="10" opacity=".45" stroke-linecap="round"/>'
        '<path d="M240 300 q60 -20 120 0" stroke="#2a9d55" stroke-width="0"/>'
        '<g transform="translate(330 300)"><path d="M0 0 C-40 -50 -90 -20 -60 10 C-40 26 -20 10 0 0 Z" fill="#2a9d55"/>'
        '<path d="M0 0 C40 -50 90 -20 60 10 C40 26 20 10 0 0 Z" fill="#2a9d55"/>'
        '<circle r="20" fill="#e63946"/><circle cx="-6" cy="-6" r="6" fill="#fff" opacity=".6"/></g>'
    )


def stocking() -> str:
    """Draw a Christmas stocking with a candy cane peeking out.

    Returns:
        str: SVG markup.
    """
    return (
        '<path d="M170 140 H330 V320 L380 360 a60 60 0 0 1 -60 110 L150 400 a60 60 0 0 1 20 -80 Z" fill="#e63946"/>'
        '<path d="M330 360 l50 0 a60 60 0 0 1 -60 110 Z" fill="#ffffff" opacity="0"/>'
        '<path d="M150 400 a60 60 0 0 1 20 -80 l40 30 Z" fill="#ffffff" opacity="0"/>'
        '<g fill="#ffffff"><circle cx="210" cy="230" r="10"/><circle cx="280" cy="270" r="10"/><circle cx="230" cy="340" r="10"/>'
        '<circle cx="320" cy="400" r="10"/><circle cx="290" cy="200" r="10"/></g>'
        '<rect x="148" y="90" width="204" height="74" rx="30" fill="#ffffff"/>'
        '<path d="M250 90 q-20 -40 10 -60" stroke="#8a5a32" stroke-width="10" fill="none" stroke-linecap="round"/>'
        + candy_peek()
    )


def candy_peek() -> str:
    """Draw the top of a candy cane behind the stocking cuff.

    Returns:
        str: SVG markup.
    """
    return (
        '<path d="M310 100 V20 A30 30 0 0 1 370 20" stroke="#ffffff" stroke-width="22" fill="none" stroke-linecap="round"/>'
        '<path d="M310 100 V20 A30 30 0 0 1 370 20" stroke="#e63946" stroke-width="22" fill="none" stroke-dasharray="14 14" stroke-linecap="round"/>'
        '<rect x="148" y="90" width="204" height="74" rx="30" fill="#ffffff"/>'
    )


def bauble(color: str = "#c77dff", swing: float = 0.0) -> str:
    """Draw a hanging bauble.

    Args:
        color (str): Bauble colour.
        swing (float): Swing in degrees around the hook.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g transform="rotate({swing} 256 60)">'
        '<path d="M256 20 V140" stroke="#ffd23f" stroke-width="8"/>'
        '<rect x="224" y="130" width="64" height="40" rx="8" fill="#ffd23f"/>'
        f'<circle cx="256" cy="300" r="150" fill="{color}"/>'
        '<path d="M110 280 Q256 330 402 280" stroke="#ffffff" stroke-width="22" fill="none" opacity=".85"/>'
        '<path d="M116 340 Q256 390 396 340" stroke="#ffd23f" stroke-width="12" fill="none" stroke-dasharray="4 22" stroke-linecap="round"/>'
        + snowflake(256, 220, 44, "#ffffff")
        + '<ellipse cx="190" cy="220" rx="36" ry="54" fill="#fff" opacity=".3" transform="rotate(30 190 220)"/>'
        + "</g>"
    )


def snowman(eye: str = "normal", arm: float = 0.0, scarf_swing: float = 0.0, hat: bool = True) -> str:
    """Draw a snowman with scarf and optional top hat.

    Args:
        eye (str): Eye kind, see ``eyes``.
        arm (float): Arm rotation in degrees.
        scarf_swing (float): Sideways offset of the scarf end.
        hat (bool): Whether to draw the top hat.

    Returns:
        str: SVG markup.
    """
    f = Face(226, 286, 150, 196, eye=0.75)
    out = (
        f'<path transform="rotate({-arm} 160 300)" d="M160 300 L70 230 M100 254 L72 270 M102 252 L96 216" stroke="#8a5a32" stroke-width="12" stroke-linecap="round" fill="none"/>'
        f'<path transform="rotate({arm} 352 300)" d="M352 300 L442 230 M412 254 L440 270 M410 252 L416 216" stroke="#8a5a32" stroke-width="12" stroke-linecap="round" fill="none"/>'
        '<circle cx="256" cy="372" r="110" fill="#ffffff" stroke="#d6e4f0" stroke-width="6"/>'
        '<circle cx="256" cy="290" r="82" fill="#ffffff" stroke="#d6e4f0" stroke-width="6"/>'
        '<circle cx="256" cy="160" r="84" fill="#ffffff" stroke="#d6e4f0" stroke-width="6"/>'
        '<path d="M300 380 a100 100 0 0 1 -110 70" stroke="#e3edf6" stroke-width="20" fill="none" stroke-linecap="round"/>'
        '<g fill="#2b2d42"><circle cx="256" cy="270" r="10"/><circle cx="256" cy="310" r="10"/><circle cx="256" cy="360" r="10"/></g>'
        + eyes(f, eye)
        + '<path d="M256 176 L320 190 L256 196 Z" fill="#ff8c42" stroke="#ff8c42" stroke-width="6" stroke-linejoin="round"/>'
        + "".join(
            f'<circle cx="{226 + i * 15}" cy="{214 + abs(i - 2) * -4 + 4}" r="5" fill="#2b2d42"/>' for i in range(5)
        )
        + f'<ellipse cx="{f.lx - 24}" cy="{f.ey + 34}" rx="16" ry="9" fill="#ff8fa3" opacity=".7"/>'
        + f'<ellipse cx="{f.rx + 24}" cy="{f.ey + 34}" rx="16" ry="9" fill="#ff8fa3" opacity=".7"/>'
        + scarf(256, 222, 150, "#3a86ff", "#ffffff", scarf_swing)
    )
    if hat:
        out += (
            '<rect x="186" y="80" width="140" height="18" rx="9" fill="#2b2d42"/>'
            '<rect x="206" y="10" width="100" height="80" rx="10" fill="#2b2d42"/>'
            '<rect x="206" y="62" width="100" height="16" fill="#e63946"/>'
            + '<g transform="translate(296 68)"><circle r="10" fill="#2a9d55"/><circle cx="10" cy="-6" r="8" fill="#e63946"/></g>'
        )
    return out


def mitten(color: str = "#e63946", wave: float = 0.0) -> str:
    """Draw a knitted mitten.

    Args:
        color (str): Mitten colour.
        wave (float): Rotation in degrees.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g transform="rotate({wave} 256 430)">'
        f'<path d="M180 400 V220 a80 80 0 0 1 150 -30 L330 200 a40 40 0 0 1 70 40 L340 330 V400 Z" fill="{color}"/>'
        '<rect x="166" y="388" width="186" height="70" rx="22" fill="#ffffff"/>'
        '<path d="M210 260 l20 20 l20 -20 l20 20 l20 -20 M210 320 l20 20 l20 -20 l20 20 l20 -20" stroke="#ffffff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        "</g>"
    )


def sled(bounce: float = 0.0) -> str:
    """Draw a sled.

    Args:
        bounce (float): Vertical offset.

    Returns:
        str: SVG markup.
    """
    return (
        f'<g transform="translate(0 {bounce})">'
        '<path d="M80 380 H400 a40 40 0 0 0 40 -40" stroke="#8a5a32" stroke-width="16" fill="none" stroke-linecap="round"/>'
        '<path d="M140 380 V340 M340 380 V340" stroke="#8a5a32" stroke-width="14" stroke-linecap="round"/>'
        '<rect x="96" y="300" width="300" height="46" rx="16" fill="#e63946"/>'
        "</g>"
    )


def snow_ground() -> str:
    """Draw a snow drift along the bottom.

    Returns:
        str: SVG markup.
    """
    return '<path d="M40 470 C100 430 180 450 256 440 C340 430 420 440 472 470 Z" fill="#ffffff" stroke="#d6e4f0" stroke-width="6"/>'


def falling_snow(t: float, n: int = 14, seed: int = 3) -> str:
    """Draw falling snowflakes as an overlay (outside the die-cut edge).

    The positions come from a small linear congruential generator, so the same seed gives the same snow.

    Args:
        t (float): Animation phase in [0, 1).
        n (int): Number of flakes.
        seed (int): Seed for the flake positions.

    Returns:
        str: SVG markup wrapped in ``<!--over-->`` markers.
    """
    out: list[str] = []
    rng = seed
    for i in range(n):
        rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF
        x = 40 + rng % 432
        rng = (rng * 1103515245 + 12345) & 0x7FFFFFFF
        y0 = rng % 512
        r = 7 + (rng >> 8) % 10
        y = (y0 + t * 512) % 560 - 30
        drift = 14 * math.sin(2 * math.pi * (t + i * 0.13))
        out.append(
            f'<circle cx="{x + drift:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" stroke="#b9d3ea" stroke-width="3"/>'
        )
    return "<!--over-->" + "".join(out) + "<!--/over-->"


# --- Pip, the Sticker Shim magpie --------------------------------------------

# Blue-green-violet sheen of magpie feathers, used by every Pip sticker.
PIP_DEFS: str = (
    '<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">'
    '<stop offset="0" stop-color="#1d6fd6"/><stop offset=".5" stop-color="#1fb7a5"/><stop offset="1" stop-color="#6a3fd1"/>'
    "</linearGradient>"
)


def pip(
    eye: str = "normal",
    beak_open: bool = False,
    held: str = "sticker",
    wing: float = 0.0,
    extras: str = "",
    tilt: float = 0.0,
    dy: float = 0.0,
    hat: str = "",
) -> str:
    """Draw Pip the magpie, facing right.

    Args:
        eye (str): normal, happy, closed, heart, big or sad.
        beak_open (bool): Whether the beak is open (then nothing is held).
        held (str): sticker, heart or none.
        wing (float): 0 folded, 1 raised (waving).
        extras (str): SVG drawn on top of Pip.
        tilt (float): Rotation in degrees.
        dy (float): Vertical offset.
        hat (str): santa, beanie or "" for none.

    Returns:
        str: SVG markup.

    Raises:
        ValueError: If ``eye`` is unknown.
    """
    ex, ey = 345, 160
    if eye == "normal":
        e = (
            f'<circle cx="{ex}" cy="{ey}" r="27" fill="#ffffff"/><circle cx="{ex + 7}" cy="{ey + 2}" r="16" fill="#1b1d2a"/>'
            f'<circle cx="{ex + 13}" cy="{ey - 5}" r="6" fill="#fff"/>'
        )
    elif eye == "happy":
        e = f'<path d="M{ex - 22} {ey + 8} Q{ex} {ey - 24} {ex + 22} {ey + 8}" stroke="#ffffff" stroke-width="11" fill="none" stroke-linecap="round"/>'
    elif eye == "closed":
        e = f'<path d="M{ex - 22} {ey} Q{ex} {ey + 18} {ex + 22} {ey}" stroke="#ffffff" stroke-width="11" fill="none" stroke-linecap="round"/>'
    elif eye == "heart":
        e = heart(ex, ey + 6, 1.2)
    elif eye == "big":
        e = (
            f'<circle cx="{ex}" cy="{ey}" r="34" fill="#ffffff"/><circle cx="{ex + 4}" cy="{ey + 2}" r="11" fill="#1b1d2a"/>'
            f'<circle cx="{ex + 8}" cy="{ey - 3}" r="4" fill="#fff"/>'
        )
    elif eye == "sad":
        e = (
            f'<circle cx="{ex}" cy="{ey + 4}" r="25" fill="#ffffff"/><circle cx="{ex + 5}" cy="{ey + 10}" r="15" fill="#1b1d2a"/>'
            f'<circle cx="{ex + 10}" cy="{ey + 4}" r="5" fill="#fff"/>'
            f'<path d="M{ex - 26} {ey - 38} L{ex + 20} {ey - 26}" stroke="#ffffff" stroke-width="9" stroke-linecap="round"/>'
        )
    else:
        raise ValueError(eye)
    beak = (
        '<path d="M405 170 L474 186 L405 196 Z" fill="#ffb347" stroke="#ffb347" stroke-width="10" stroke-linejoin="round"/>'
        '<path d="M405 204 L462 222 L405 222 Z" fill="#f08c2a" stroke="#f08c2a" stroke-width="10" stroke-linejoin="round"/>'
        if beak_open
        else '<path d="M405 172 L474 194 L405 214 Z" fill="#ffb347" stroke="#ffb347" stroke-width="10" stroke-linejoin="round"/>'
        '<path d="M410 194 L468 194" stroke="#d97a1e" stroke-width="5" stroke-linecap="round"/>'
    )
    hold = ""
    if held == "sticker" and not beak_open:
        hold = (
            '<g transform="translate(470 230) rotate(18)"><circle r="40" fill="#fff" stroke="#e6e9f2" stroke-width="3"/>'
            '<circle r="31" fill="#ffd23f"/>' + star(0, 2, 19, "#ffffff") + "</g>"
        )
    elif held == "heart" and not beak_open:
        hold = '<g transform="translate(470 232)">' + heart(0, 0, 1.4) + "</g>"
    w = wing
    wing_svg = (
        f'<g transform="rotate({-70 * w} 270 260)">'
        '<path d="M150 260 Q200 200 290 250 Q260 350 170 360 Q130 320 150 260 Z" fill="url(#sheen)" stroke="#1b1d2a" stroke-width="6"/>'
        '<path d="M175 300 q40 0 80 -20 M180 330 q40 0 70 -15" stroke="#ffffff" stroke-width="5" opacity=".5" fill="none" stroke-linecap="round"/>'
        "</g>"
    )
    hats = {"santa": santa_hat(320, 96, 0.72, 10), "beanie": beanie(326, 96, 0.68, "#3a86ff")}
    return (
        f'<g transform="translate(0 {dy}) rotate({tilt} 256 300)">'
        '<path d="M150 360 L40 460 L90 470 L180 400 Z" fill="url(#sheen)"/>'
        '<path d="M240 425 v40 m-14 0 h28 M310 425 v40 m-14 0 h28" stroke="#ffb347" stroke-width="10" stroke-linecap="round"/>'
        '<ellipse cx="270" cy="300" rx="150" ry="130" fill="#1b1d2a"/>'
        '<ellipse cx="300" cy="340" rx="90" ry="80" fill="#ffffff"/>'
        f"{wing_svg}"
        '<circle cx="330" cy="170" r="92" fill="#1b1d2a"/>'
        f'{e}<ellipse cx="315" cy="218" rx="16" ry="9" fill="{BLUSH}" opacity=".6"/>'
        f"{beak}{hold}{hats.get(hat, '')}{extras}</g>"
    )
