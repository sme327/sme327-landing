# sme327 | Project Hub

Personal landing page for [sme327.streamlit.app](https://sme327.streamlit.app) — a dark, polished portfolio hub linking to all of Shawn's Streamlit projects.

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## Add a New Project

Open `streamlit_app.py` and add an entry to the `PROJECTS` list:

```python
{
    "title": "My New App",
    "description": "Short description here.",
    "tags": ["Streamlit", "Data"],       # picks from TAG_STYLE for colors
    "url": "https://your-app.streamlit.app",
    "thumbnail": "assets/my_app_thumbnail.png",
    "icon": "🔥",                        # shown as fallback when no thumbnail
    "fallback_gradient": "linear-gradient(160deg, #100010 0%, #2d002d 100%)",
},
```

Drop a thumbnail image (any size — 800×500 is ideal) into `assets/` and point `"thumbnail"` at it. The card handles missing images gracefully with the gradient fallback.

To add a new "coming soon" placeholder, append to `COMING_SOON` instead.

---

## Replace URLs

At the top of `streamlit_app.py`:

```python
WORLD_CUP_APP_URL = "PASTE_WORLD_CUP_LINK_HERE"   # ← replace
FANTASY_APP_URL   = "PASTE_FANTASY_LINK_HERE"      # ← replace
```

Buttons render as disabled (grey) until a real URL is pasted in.

---

## Add / Replace Images

| File | Purpose |
|---|---|
| `assets/seattle_hero.png` | Hero background (wide, 1920×800+ recommended) |
| `assets/world_cup_thumbnail.png` | World Cup card left panel |
| `assets/fantasy_thumbnail.png` | Fantasy Football card left panel |

All images are base64-encoded at runtime — no CDN or external hosting needed. Missing images fall back to CSS gradients automatically.

---

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Set **Main file path** → `streamlit_app.py`.
4. Deploy — images in `assets/` are bundled with the repo.
