# sme327 | Project Hub

Personal landing page for [sme327.streamlit.app](https://sme327.streamlit.app) — a dark, polished portfolio hub linking to all of Shawn's Streamlit projects.

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## Current Projects

Cards render in this order (auto-fitting grid, left to right):

| Card | URL Variable | Live URL |
|---|---|---|
| Sports Today | `SPORTS_TODAY_URL` | _not set — link disabled_ |
| Espinosa FFL Clubhouse | `CLUBHOUSE_APP_URL` | espinosaffl.streamlit.app |
| {insert witty name here} FFL Museum | `FANTASY_APP_URL` | insertwittynamehere.streamlit.app |
| A New Dynasty FFL Museum | `DYNASTY_APP_URL` | anewdynasty.streamlit.app |
| FFL Draft Room | `DRAFT_ROOM_URL` | _not set — link disabled_ |
| My Concert Atlas | `CONCERT_ATLAS_URL` | show-history-archive.sme327.chatgpt.site |
| World Cup Family HQ | `WORLD_CUP_APP_URL` | espinosa-world-cup.streamlit.app |

## Also Built

The `SHOWCASE` list holds projects that are real but not publicly hosted. Entries
use the same fields as `PROJECTS`, except they **omit `url`** and add a `label`,
which renders as a muted chip where the launch link would be:

```python
{
    "title":       "Next",
    "description": "A project tracker for the AI tools I'm building.",
    "label":       "Private build",
    "thumbnail":   "assets/next.png",
    "icon":        "🗂️",
    "obj_pos":     "center center",
    "fallback_gradient": "linear-gradient(160deg, #0b0a1f 0%, #2a1b5e 45%, #0b0a1f 100%)",
},
```

If one of these later becomes publicly reachable, move the dict to `PROJECTS`,
swap `label` for `url`, and optionally set `cta` (e.g. `"View code →"`).

Coming soon placeholders: **Fantasy League 3**, **Seattle Concert Finder**

---

## Add a New Project

Add an entry to the `PROJECTS` list in `streamlit_app.py`:

```python
{
    "title":       "My New App",
    "description": "Short description here.",
    "url":         MY_APP_URL,            # define at the top of the file
    "thumbnail":   "assets/my_app.png",  # drop image in assets/
    "icon":        "🔥",                 # fallback if image is missing
    "obj_pos":     "center center",      # CSS object-position for the 4:3 crop
    "fallback_gradient": "linear-gradient(160deg, #100010 0%, #2d002d 100%)",
},
```

Then define the URL constant at the top of the file alongside the others:

```python
MY_APP_URL = "https://my-app.streamlit.app"
```

Drop a thumbnail image into `assets/`. Thumbnails are cropped to `4/3` at the top
of the card, so a roughly 4:3–3:2 source works best (~1200×900). The card handles
missing images gracefully with the gradient fallback.

To add a Coming Soon placeholder instead, append to `COMING_SOON`.

---

## Replace / Add Images

| File | Used by |
|---|---|
| `assets/seattle_hero.png` | Hero background (wide, 1920×800+ recommended) |
| `assets/sports_today.png` | Sports Today thumbnail |
| `assets/espinosa_ffl2.png` | Espinosa FFL Clubhouse thumbnail |
| `assets/25_FFL_2.png` | {insert witty name here} FFL Museum thumbnail |
| `assets/FFL_AND.png` | A New Dynasty FFL Museum thumbnail |
| `assets/concert_atlas.png` | My Concert Atlas thumbnail |
| `assets/worldcup_hq_image.png` | World Cup card thumbnail |

All images are base64-encoded at runtime — no CDN needed. Missing images fall
back to CSS gradients automatically. Keep thumbnails under ~500KB to avoid slow
cold starts on Streamlit Cloud.

---

## Static Build (sme327.com)

The page has no widgets or callbacks, so it can be served as flat files with no
Python runtime. `build.py` stubs out `streamlit`, imports the app, captures what
it passed to `st.markdown()`, and writes `dist/`:

```bash
python build.py        # → dist/index.html + dist/assets/
open dist/index.html   # verify locally before deploying
```

There's one source of truth: edit `streamlit_app.py` and both the Streamlit
deploy and the static site pick up the change. `build.py` is standard library
only, so the host's build step needs nothing installed.

`dist/` is gitignored — the host rebuilds it on each push.

### Images

The app inlines images as base64, which is fine for Streamlit but wasteful over
a CDN; `build.py` extracts them back out to real files so the browser can cache
them separately. Sources are compressed ahead of time:

```bash
pip install pillow
python optimize_assets.py   # assets/*.png → assets/*.webp
```

Cards reference the `.webp` files, so after dropping a new PNG into `assets/`,
run `optimize_assets.py`. Originals are left in place as masters. Together these
take the page from ~21MB to ~1.4MB.

### Hosting (Cloudflare Pages)

| Setting | Value |
|---|---|
| Build command | `python build.py` |
| Output directory | `dist` |
| Framework preset | None |

---

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app**.
3. Set **Main file path** → `streamlit_app.py`.
4. Deploy — images in `assets/` are bundled with the repo and served automatically.

Streamlit Cloud redeploys automatically on every push to `main`.
