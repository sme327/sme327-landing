# sme327 | Project Hub

Personal landing page for [sme327.com](https://sme327.com) — a dark, polished portfolio hub linking to Shawn's projects. Written as a Streamlit script, built to static files by `build.py`, and hosted on Cloudflare Pages. (The old `sme327.streamlit.app` deployment was deleted 2026-09-13; `streamlit run` is now only a local preview.)

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
| {insert witty name here} FFL Museum | `FANTASY_APP_URL` | iwnh.sme327.com |
| A New Dynasty FFL Museum | `DYNASTY_APP_URL` | and.sme327.com |
| Dynasty 22 | `DYNASTY_22_URL` | dynasty.sme327.com |
| Espinosa FFL Clubhouse | `CLUBHOUSE_APP_URL` | espinosaFFL.sme327.com |
| World Cup Family HQ | `WORLD_CUP_APP_URL` | espinosa-world-cup.streamlit.app (the one project still on Streamlit Cloud — stays there until it's migrated to sme327.com, owner decision 2026-09-13) |
| Sports Today | `SPORTS_TODAY_URL` | sports.sme327.com |
| My Concert Archive | `CONCERT_ATLAS_URL` | concerts.sme327.com |
| 20 Years of Listening | `MUSIC_URL` | music.sme327.com |

Compact tool cards (`FOOTBALL_TOOLS`, then `TOOLS`):

| Card | URL Variable | Live URL |
|---|---|---|
| {insert witty name here} Draft Room | `DRAFT_ROOM_URL` | iwnh-draft-2026.sme327.chatgpt.site |
| A New Dynasty Keeper Tool | `KEEPER_TOOL_URL` | andkeepers.sme327.com |
| My FFL (formerly Draft Queue) | `MY_FFL_URL` | _PIN-gated at myffl.sme327.com / queue.sme327.com — link disabled until a public version ships_ |
| Next | — | _no link; "Private build" chip_ |
| Asst Coach | `PRACTICE_PLANS_URL` | practice.sme327.com (the sign-in-free surface of coach.sme327.com) |
| Our Home | `OUR_HOME_URL` | _PIN-gated at ourhome.sme327.com — link disabled until a public version ships_ |

> **Publishing?** `PUBLISHING.md` is the short version: how to add a card, how the hub
> deploys, how to stand up a new `*.sme327.com` subdomain. Start there.

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

Coming soon placeholders: **NFL Playoff Pool**, **Women's World Cup**,
**Champions Hall**, and **meow**.

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
MY_APP_URL = "https://myapp.sme327.com"
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
| `assets/sleeper_dynasty.png` | Sleeper Dynasty FFL thumbnail |
| `assets/concert_archive.png` | My Concert Archive thumbnail |
| `assets/worldcup_hq_image.png` | World Cup card thumbnail |

All images are base64-encoded at runtime — no CDN needed. Missing images fall
back to CSS gradients automatically. Keep thumbnail masters under ~500KB so the
local preview stays quick and the build has little to compress.

---

## Static Build (sme327.com)

The page has no widgets or callbacks, so it can be served as flat files with no
Python runtime. `build.py` stubs out `streamlit`, imports the app, captures what
it passed to `st.markdown()`, and writes `dist/`:

```bash
python build.py        # → dist/index.html + dist/assets/
open dist/index.html   # verify locally before deploying
```

There's one source of truth: edit `streamlit_app.py` and both the local
`streamlit run` preview and the static site pick up the change. `build.py` is standard library
only, so the host's build step needs nothing installed.

`dist/` is gitignored — the host rebuilds it on each push. Alongside the HTML it
writes `robots.txt` and a `_headers` file that Cloudflare Pages reads:

- **Caching** — extracted images get a content hash in the filename
  (`concert_atlas.32750c24.webp`), so they're cached for a year as immutable
  while the HTML revalidates on every request. Change an image and its URL
  changes with it; no stale cache, no manual purge.
- **Security headers** — `nosniff`, a referrer policy, and a CSP. The static
  page contains no JavaScript, so the CSP denies scripts outright.

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

## Deployment

Push to `main`; Cloudflare Pages runs `python build.py` and publishes `dist/` to
sme327.com in a few minutes. The full steps and the verification check are in
`PUBLISHING.md` §B.

The Streamlit Community Cloud deployment (`sme327.streamlit.app`) was deleted on
2026-09-13 — don't recreate it; Cloudflare is the only host.
