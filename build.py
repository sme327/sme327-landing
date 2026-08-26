"""Render the Streamlit page to a static site in dist/.

    python build.py

The page has no widgets or callbacks — Streamlit is only ever used to emit one
HTML document — so it can be served as flat files from a CDN with no Python
runtime. Rather than duplicating the markup, this stubs out the `streamlit`
module, imports the app (which renders on import), and captures whatever it
passed to st.markdown(). One source of truth: edit streamlit_app.py and both
the Streamlit deploy and the static site follow.

Images are inlined as base64 data URIs by the app, which is fine for Streamlit
but wasteful over a CDN, where the browser could cache them separately. So the
data URIs are extracted back out to real files under dist/assets/ and the
references rewritten.

Standard library only — no Streamlit, no Pillow — so the host's build step needs
no dependencies installed. (Image *compression* is a separate authoring step;
see optimize_assets.py.)
"""

import base64
import hashlib
import re
import shutil
import sys
import types
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SITE_URL = "https://sme327.com"
DESCRIPTION = "Personal project hub for Shawn Espinosa — sports, data, and the things I build."


# ── Capture the app's output ──────────────────────────────────────────────────

class _StreamlitStub(types.ModuleType):
    """Records st.markdown() calls; no-ops everything else."""

    def __init__(self):
        super().__init__("streamlit")
        self.fragments: list[str] = []
        self.page_config: dict = {}

    def set_page_config(self, **kwargs):
        self.page_config = kwargs

    def markdown(self, body, unsafe_allow_html=False):
        self.fragments.append(body)

    def __getattr__(self, name):
        # Any other Streamlit call is a no-op. If the app ever grows a real
        # widget this silently drops it — which is the signal that the page is
        # no longer static and needs a different hosting story.
        def _noop(*args, **kwargs):
            return None

        return _noop


def capture_app() -> tuple[str, dict]:
    stub = _StreamlitStub()
    sys.modules["streamlit"] = stub
    sys.path.insert(0, str(ROOT))

    import streamlit_app  # noqa: F401  (renders on import)

    return "\n".join(stub.fragments), stub.page_config


# ── Turn inlined images back into files ───────────────────────────────────────

DATA_URI = re.compile(r"data:image/(?P<ext>[a-z]+);base64,(?P<data>[A-Za-z0-9+/=]+)")


def source_names_by_hash() -> dict[str, str]:
    """Map file contents to their original filename, so extracted images keep
    readable names instead of hashes."""
    names: dict[str, str] = {}
    # Sorted + first-wins so duplicate files (same bytes, two names) always
    # resolve to the same one instead of varying by directory order.
    for path in sorted((ROOT / "assets").iterdir()):
        if path.is_file():
            names.setdefault(hashlib.sha1(path.read_bytes()).hexdigest(), path.name)
    return names


def externalize_images(html: str) -> tuple[str, int]:
    out_dir = DIST / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    known = source_names_by_hash()
    written: dict[str, str] = {}

    def replace(match: re.Match) -> str:
        raw = base64.b64decode(match["data"])
        digest = hashlib.sha1(raw).hexdigest()
        if digest not in written:
            source = known.get(digest)
            stem = Path(source).stem if source else "image"
            ext = Path(source).suffix.lstrip(".") if source else match["ext"]
            # Content hash in the filename: changing an image changes its URL,
            # so assets can be cached forever without ever serving a stale one.
            name = f"{stem}.{digest[:8]}.{ext}"
            (out_dir / name).write_bytes(raw)
            written[digest] = name
        return f"assets/{written[digest]}"

    return DATA_URI.sub(replace, html), len(written)


# ── Document shell ────────────────────────────────────────────────────────────

HERO_REF = re.compile(r"background-image:url\('(assets/[^']+)'\)")


def social_image(body: str) -> str:
    """The hero, read back out of the rendered CSS rather than hardcoded, so it
    survives the image being renamed or swapped."""
    match = HERO_REF.search(body)
    return f"{SITE_URL}/{match.group(1)}" if match else ""


def document(body: str, config: dict) -> str:
    title = config.get("page_title", "sme327")

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{DESCRIPTION}">
<link rel="icon" href="/favicon.ico?v=8" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png?v=8">
<link rel="icon" type="image/png" sizes="64x64" href="/favicon-64.png?v=8">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png?v=8">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{social_image(body)}">
<meta name="twitter:card" content="summary_large_image">
<style>
/* The app's CSS paints .stApp, which doesn't exist outside Streamlit. */
html,body{{margin:0;padding:0;background:#080d1a;}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


# ── Host configuration ────────────────────────────────────────────────────────

# Cloudflare Pages reads these from the output root.
#
# Cache-Control is deliberately absent from the /* block: it matches everything
# including /assets/*, and two rules setting the same header on one request is
# ambiguous. HTML revalidates every time (it's 19KB and must reflect edits
# immediately); hashed assets are immutable, since a changed image gets a new
# filename rather than a new version of the same one.
#
# The page contains no JavaScript at all, so the CSP can deny scripts outright.
# 'unsafe-inline' for styles is unavoidable — the design is one big inline
# <style> block plus inline style attributes on the thumbnails.
HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Content-Security-Policy: default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; base-uri 'none'; form-action 'none'; frame-ancestors 'none'

/
  Cache-Control: public, max-age=0, must-revalidate

/index.html
  Cache-Control: public, max-age=0, must-revalidate

/assets/*
  Cache-Control: public, max-age=31536000, immutable
"""

ROBOTS = """\
User-agent: *
Allow: /
"""


# ── Build ─────────────────────────────────────────────────────────────────────

def main() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    body, config = capture_app()
    body, image_count = externalize_images(body)
    html = document(body, config)

    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "_headers").write_text(HEADERS, encoding="utf-8")
    (DIST / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    # No rel="mask-icon": Safari tints mask icons onto a white rounded square (in tabs, not just
    # pinned tabs, as of Safari 26), which put a white box behind the orange needle. The PNG/ICO
    # favicon is the intended tab icon — an orange square with the dark needle.
    for icon_name in (
        "favicon.ico",
        "favicon-32.png",
        "favicon-64.png",
        "apple-touch-icon.png",
    ):
        shutil.copy2(ROOT / "assets" / icon_name, DIST / icon_name)

    assets = sorted((DIST / "assets").glob("*"))
    asset_bytes = sum(p.stat().st_size for p in assets)
    print(f"dist/index.html   {len(html.encode())/1e3:8.1f} KB")
    print(f"dist/assets/      {asset_bytes/1e6:8.2f} MB  ({image_count} images)")
    print(f"total page weight {(len(html.encode()) + asset_bytes)/1e6:8.2f} MB")


if __name__ == "__main__":
    main()
