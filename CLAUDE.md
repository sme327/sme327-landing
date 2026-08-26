# CLAUDE.md — sme327 Project Hub

## Design Goal

Dark, polished personal portfolio landing page for Shawn Espinosa. Feels like a
premium personal data/code hub — not a corporate site, not a generic dashboard.
The Seattle skyline photo (Space Needle + Mount Rainier at dusk) is the hero and
the emotional anchor of the page. Visual reference: `docs/landing-page-reference.png`.

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
2. **Featured Projects** — auto-fitting grid of portrait cards, floats 115px over
   the hero bottom
3. **Also Built** — same card shape, for real projects that aren't publicly
   hosted. No launch link; a muted "Private build" chip instead
4. **Coming Soon** — auto-sizing row of dashed placeholder cards
5. **Footer** — centered, minimal icon links

---

## Visual Style Rules

- **Hero text is positioned near the top** (`padding-top: 72px`) so the skyline
  and Rainier are visible in the middle and bottom of the image.
- **Cards float over the hero** via `margin-top: -115px` on `.proj-section`. Do
  not remove this — it's what gives the page its layered, cinematic feel.
- **Cards are portrait panels — artwork on top, text below.** The thumbnail is a
  full-width `4/3` block (~70–75% of the card) with the content area beneath it.
  Do not go back to the side-by-side landscape layout.
- **The artwork is the primary focus.** Content area stays compact: one title
  line (emoji + name), a one-sentence description, and the launch link. No
  paragraph-length copy, no large empty padding under the text.
- **Launch is a plain text link, not a button** — accent blue `#3b82f6`, 13.5px,
  no background or outline. It should read as secondary to the image.
- **Grid is `repeat(auto-fit,minmax(300px,1fr))`** — never hardcode a column
  count. Cards wrap on available width (≈4 desktop, 2 tablet, 1 mobile).
- **Coming soon cards** use dashed borders and muted styling — they should feel
  like honest placeholders, not broken features.
- **Hover effects** on project cards: subtle lift (`translateY(-3px)`) +
  brightened border + box shadow + 3% zoom on the thumbnail.
- **Link text defaults to "Visit Site →"**. A
  card may override it with an optional `cta` field (e.g. `"View code →"`) when
  the destination isn't a launchable app.
- **Disabled links** (URL set to `"PASTE_..._HERE"`) render grey automatically.
- **Three card states, and the distinction matters:** a live link, a grey
  *temporarily* pending link, and a showcase card with no link at all. Never
  park a finished-but-private project on the grey pending state — it reads as
  broken. Put it in `SHOWCASE` instead.

---

## Project Data Structure

All live projects live in `PROJECTS` (list of dicts); projects that exist but
aren't publicly hosted live in `SHOWCASE`. Both are rendered by
`project_card_html()`, which branches on whether the dict has a `url` key —
`url` present renders the launch link, absent renders the `label` chip. Fields:

| Field | Purpose |
|---|---|
| `title` | Card heading |
| `description` | 1–2 sentence card body |
| `url` | Launch link destination; set to `"PASTE_..._HERE"` to disable. Omit entirely for `SHOWCASE` cards |
| `cta` | *Optional.* Overrides the default `"Launch App →"` link text |
| `label` | `SHOWCASE` only — chip text shown in place of the link (e.g. `"Private build"`) |
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
| Sports Today | Daily sports companion (MLB/WNBA opportunities). URL still pending. |
| My Concert Archive | Personal concert history — every show attended, by band/venue/year/state. |
| Espinosa FFL Clubhouse | Family fantasy football hub |
| {insert witty name here} FFL Museum | **This is the real league name** — 25-year history. Not a placeholder. |
| A New Dynasty FFL Museum | Keeper/dynasty league, est. 2016. Still on Streamlit; port pending. Note `dynasty.sme327.com` is taken by Sleeper Dynasty FFL, so this needs a different subdomain. |
| World Cup Family HQ | 2026 FIFA World Cup family tracker |
| Sleeper Dynasty FFL | Graduated from Coming Soon. Awaiting artwork — the dict has no `thumbnail` key, so it renders the violet gradient placeholder. Drop in `assets/sleeper_dynasty.webp` and add the key to finish it. |

Productivity & Tools (`TOOLS`): **{insert witty name here} Draft Room** — draft board + queue + keeper tool, live; **A New Dynasty Keeper Tool** — andkeepers.sme327.com, 2026 keeper selections, live (both use illustrated `icon_asset` tiles, brief in `docs/TOOL-ICONS-BRIEF.md`);
**Next** — project tracker for AI builds, no public link (renders a "Private build" chip)

Coming soon: **NFL Playoff Pool**, **Women's World Cup**

---

## How to Add a Future Project

1. Add URL constant at the top of `streamlit_app.py`
2. Add dict to `PROJECTS` list (see README for field reference)
3. Drop thumbnail in `assets/` — wide crop, keep under ~500KB
4. Set `obj_pos` to position the crop — the thumbnail is cropped to `4/3`, so
   keep the focal point in frame (e.g. `"center top"`, `"left center"`)
5. If URL isn't ready, set it to `"PASTE_..._HERE"` — link auto-disables

The grid auto-fits, so cards flow into additional rows on their own — no layout
changes are needed when adding a 7th or 8th card.

---

## Preserve These Behaviors

- All CSS lives in a single `<style>` block at the top of `render()` — keep it together
- Hero background is computed at runtime (image file → base64 data URI) — do not hardcode
- **The page must stay free of widgets.** `build.py` renders it to static HTML
  for sme327.com by stubbing Streamlit and capturing `st.markdown()` calls.
  Adding `st.button`/`st.selectbox`/session state would silently vanish from the
  static build and break that hosting story. If real interactivity is ever
  needed, that's a hosting decision, not just a code change.
- Thumbnails are `.webp` generated by `optimize_assets.py` from the PNG masters
  in `assets/` — update paths together if you add an image
- `gap:0!important` on Streamlit's vertical block removes whitespace between sections
- `margin-top:-115px` on `.proj-section` creates the hero overlap — do not remove
- `backdrop-filter:blur(12px)` on cards makes them readable over the hero image
