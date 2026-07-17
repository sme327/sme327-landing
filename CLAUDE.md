# CLAUDE.md — sme327 Project Hub

## Design Goal

Dark, polished personal portfolio landing page for Shawn Espinosa. Feels like a
premium personal data/code hub — not a corporate site, not a generic dashboard.
The Seattle skyline photo (Space Needle + Mount Rainier at dusk) is the hero and
the emotional anchor of the page. Visual reference: `example.png` in the repo root.

**Color palette:**
- Page background: `#080d1a` (near-black navy)
- Card background: `rgba(12,20,38,0.97)` (dark slate, with blur)
- Accent blue: `#3b82f6` / button blue: `#2d7ef8`
- Text primary: `#ffffff`
- Text secondary: `#94a3b8`
- Border: `rgba(59,130,246,0.22)` (subtle blue glow)

---

## Layout Overview

**No top navigation.** The project cards are the primary navigation; the footer
handles secondary links (GitHub, LinkedIn, email). Do not add a nav bar back.

1. **Hero** — full-width Seattle image (550px tall), title + tagline in upper-left
2. **Featured Projects** — 2-column card grid, floats 115px over the hero bottom
3. **More Projects Coming Soon** — auto-sizing row of dashed placeholder cards
4. **Footer** — centered, minimal icon links

---

## Visual Style Rules

- **Hero text is positioned near the top** (`padding-top: 72px`) so the skyline
  and Rainier are visible in the middle and bottom of the image.
- **Cards float over the hero** via `margin-top: -115px` on `.proj-section`. Do
  not remove this — it's what gives the page its layered, cinematic feel.
- **Cards are large horizontal panels** — thumbnail fills the left 48%, text
  fills the right 52%. Fixed height of 260px on desktop.
- **Coming soon cards** use dashed borders and muted styling — they should feel
  like honest placeholders, not broken features.
- **Hover effects** on project cards: subtle lift (`translateY(-3px)`) +
  brightened border + box shadow.
- **Button text is "Launch App →"** — do not change back to "Open App".
- **Disabled buttons** (URL set to `"PASTE_..._HERE"`) render grey automatically.

---

## Project Data Structure

All live projects live in `PROJECTS` (list of dicts). Fields:

| Field | Purpose |
|---|---|
| `title` | Card heading |
| `description` | 1–2 sentence card body |
| `url` | Launch button destination; set to `"PASTE_..._HERE"` to disable |
| `thumbnail` | Path to image in `assets/`; missing = gradient fallback |
| `icon` | Emoji shown in card body (above title) |
| `obj_pos` | CSS `object-position` for thumbnail crop (e.g. `"center top"`) |
| `fallback_gradient` | CSS gradient string shown when thumbnail is absent |

> **Note:** A `tags` field and `TAG_STYLE` dict exist in the code but tags are
> NOT displayed on cards. They were removed for visual simplicity. Do not add
> them back to the card HTML without a design discussion.

Coming soon items live in `COMING_SOON` (list of dicts: `svg`, `title`,
`subtitle`, `color`, `bg`).

---

## Current Projects

Listed in render order:

| Title | Notes |
|---|---|
| My Concert Atlas | Personal concert history — every show attended, by band/venue/year/state. Source data: `~/Documents/Projects/concert history`. Distinct from the Seattle Concert Finder placeholder below. Thumbnail + URL pending. |
| Sports Today | Daily sports companion (MLB/WNBA opportunities). URL still pending. |
| World Cup Family HQ | 2026 FIFA World Cup family tracker |
| Espinosa FFL Clubhouse | Family fantasy football hub |
| {insert witty name here} FFL Museum | **This is the real league name** — 25-year history. Not a placeholder. |
| A New Dynasty FFL Museum | Keeper/dynasty league, est. 2016 |

Coming soon: **Fantasy League 3**, **Seattle Concert Finder**

---

## How to Add a Future Project

1. Add URL constant at the top of `streamlit_app.py`
2. Add dict to `PROJECTS` list (see README for field reference)
3. Drop thumbnail in `assets/` — wide crop, keep under ~500KB
4. Set `obj_pos` to position the crop (e.g. `"center top"` to show the top
   of the image rather than the center)
5. If URL isn't ready, set it to `"PASTE_..._HERE"` — button auto-disables

The grid is 2 columns on desktop. Cards flow into additional rows naturally —
no layout changes needed when adding a 5th or 6th card.

---

## Preserve These Behaviors

- All CSS lives in a single `<style>` block at the top of `render()` — keep it together
- Hero background is computed at runtime (image file → base64 data URI) — do not hardcode
- `gap:0!important` on Streamlit's vertical block removes whitespace between sections
- `margin-top:-115px` on `.proj-section` creates the hero overlap — do not remove
- `backdrop-filter:blur(12px)` on cards makes them readable over the hero image
