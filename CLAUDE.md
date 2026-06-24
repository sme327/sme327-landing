# CLAUDE.md — sme327 Project Hub

## Design Goal

Dark, polished personal portfolio landing page. Feels like a premium personal data/code hub, not a corporate site. Visual reference: the mockup image saved as `example.png`.

**Color palette:**
- Page background: `#080d1a` (near-black navy)
- Card background: `rgba(15,23,42,0.96)` (dark slate)
- Accent blue: `#3b82f6`
- Text primary: `#ffffff`
- Text secondary: `#94a3b8`
- Border: `rgba(59,130,246,0.2)` (subtle blue glow)

## Visual Style Rules

- **No Streamlit default chrome.** Nav, footer, padding are all fully custom via `st.markdown(..., unsafe_allow_html=True)`.
- **Hero background** comes from `assets/seattle_hero.png` (Space Needle + Mount Rainier at dusk). Falls back to a dark blue CSS gradient if image is missing.
- **Cards are large and horizontal** — thumbnail fills the left 42%, text/button fills the right 58%.
- **Coming soon cards** use dashed borders, colored icon circles, and muted styling — they should feel like placeholders, not broken.
- **Hover effects** on project cards: subtle lift (`translateY(-3px)`) + brightened border.
- **Responsive breakpoints** at 960px (stack project cards) and 600px (simplify nav).

## Project Data Structure

All projects live in `PROJECTS` (list of dicts). Fields:
- `title`, `description`, `tags` — display copy
- `url` — link for "Open App →" button (set to `"PASTE_..._HERE"` to disable)
- `thumbnail` — path relative to app root; missing = CSS gradient fallback
- `icon` — emoji shown as fallback and in card header
- `fallback_gradient` — CSS gradient string for when thumbnail is absent

Tag colors are defined in `TAG_STYLE`. Add new tags there when needed.

Coming soon items live in `COMING_SOON` (list of dicts with `svg`, `title`, `subtitle`, `color`, `bg`).

## Current Projects

1. **World Cup Family HQ** — family 2026 FIFA World Cup tracker
2. **25-Year Fantasy Football Museum** — 25-season FFL history and analytics

## How to Add a Future Project

1. Add a dict to `PROJECTS` in `streamlit_app.py`
2. Drop a thumbnail in `assets/`
3. If URL is not ready, set it to `"PASTE_..._HERE"` — button auto-disables
4. Add any new tag colors to `TAG_STYLE`
5. Do NOT redesign the layout — the grid is intentionally fixed at 2 columns (desktop)

## Preserve These Behaviors

- All CSS is injected in a single `<style>` block at the top of `render()` — keep it together
- The hero background CSS is computed at runtime (reads image file → base64) — do not hardcode
- `gap:0!important` on Streamlit's vertical block is required to prevent whitespace between sections
- `position:sticky;top:0` on `.nav` makes the nav stick as the user scrolls
