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

Cards render in this order (2-column grid, left to right):

| Card | URL Variable | Live URL |
|---|---|---|
| My Concert Atlas | `CONCERT_ATLAS_URL` | _not set — button disabled_ |
| Sports Today | `SPORTS_TODAY_URL` | _not set — button disabled_ |
| World Cup Family HQ | `WORLD_CUP_APP_URL` | espinosa-world-cup.streamlit.app |
| Espinosa FFL Clubhouse | `CLUBHOUSE_APP_URL` | espinosaffl.streamlit.app |
| {insert witty name here} FFL Museum | `FANTASY_APP_URL` | insertwittynamehere.streamlit.app |
| A New Dynasty FFL Museum | `DYNASTY_APP_URL` | anewdynasty.streamlit.app |

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
    "obj_pos":     "center center",      # CSS object-position for thumbnail crop
    "fallback_gradient": "linear-gradient(160deg, #100010 0%, #2d002d 100%)",
},
```

Then define the URL constant at the top of the file alongside the others:

```python
MY_APP_URL = "https://my-app.streamlit.app"
```

Drop a thumbnail image into `assets/` (wide crop, ~1200×600 recommended). The card
handles missing images gracefully with the gradient fallback.

To add a Coming Soon placeholder instead, append to `COMING_SOON`.

---

## Replace / Add Images

| File | Used by |
|---|---|
| `assets/seattle_hero.png` | Hero background (wide, 1920×800+ recommended) |
| `assets/worldcup_hq_image.png` | World Cup card thumbnail |
| `assets/espinosa_ffl2.png` | Espinosa FFL Clubhouse thumbnail |
| `assets/25_FFL.png` | {insert witty name here} FFL Museum thumbnail |
| `assets/FFL_AND.png` | A New Dynasty FFL Museum thumbnail |

All images are base64-encoded at runtime — no CDN needed. Missing images fall
back to CSS gradients automatically. Keep thumbnails under ~500KB to avoid slow
cold starts on Streamlit Cloud.

---

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app**.
3. Set **Main file path** → `streamlit_app.py`.
4. Deploy — images in `assets/` are bundled with the repo and served automatically.

Streamlit Cloud redeploys automatically on every push to `main`.
