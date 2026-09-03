"""Convert source PNGs in assets/ into web-sized WebP.

The cards reference the .webp files, so run this after dropping a new image in:

    python optimize_assets.py

Originals are left alone — they're the masters. Only files whose .webp is
missing or older than the source are rebuilt.

Requires Pillow (`pip install pillow`), which is a local authoring dependency
only. Neither the Streamlit app nor build.py needs it.
"""

from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).parent / "assets"

# The hero spans the full viewport, so it keeps more pixels than the cards,
# which render around 340px wide (~700px on a 2x display).
HERO_MAX_WIDTH = 1920
CARD_MAX_WIDTH = 1200
HERO_QUALITY = 85
CARD_QUALITY = 82


def is_icon(src: Path) -> bool:
    """Icons and favicons are referenced as .png (the tool tiles inline them),
    so converting them only leaves unused .webp files behind."""
    return "icon" in src.stem


def optimize(src: Path) -> Path | None:
    dst = src.with_suffix(".webp")
    if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
        return None

    with Image.open(src) as im:
        im = im.convert("RGB")
        # Anything twice as wide as it is tall is a banner, not a card thumbnail.
        # The mobile hero crop is squarer than that but is still a full-bleed
        # background, so it earns the hero's width and quality by name.
        is_hero = im.width / im.height >= 2 or src.stem.startswith("seattle_hero")
        max_width = HERO_MAX_WIDTH if is_hero else CARD_MAX_WIDTH
        if im.width > max_width:
            height = round(im.height * max_width / im.width)
            im = im.resize((max_width, height), Image.LANCZOS)
        im.save(dst, "WEBP", quality=HERO_QUALITY if is_hero else CARD_QUALITY, method=6)

    return dst


def main() -> None:
    sources = sorted(ASSETS.glob("*.png"))
    if not sources:
        print("no PNGs found in assets/")
        return

    total_src = total_dst = 0
    for src in sources:
        if is_icon(src):
            continue
        dst = optimize(src)
        before = src.stat().st_size
        after = src.with_suffix(".webp").stat().st_size
        total_src += before
        total_dst += after
        status = "skipped (up to date)" if dst is None else "converted"
        print(f"{src.name:28} {before/1e6:6.2f}MB → {after/1e6:5.2f}MB  {status}")

    print(f"\n{'total':28} {total_src/1e6:6.2f}MB → {total_dst/1e6:5.2f}MB")


if __name__ == "__main__":
    main()
