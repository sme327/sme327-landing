import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="sme327 | Project Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── App Configuration ─────────────────────────────────────────────────────────

WORLD_CUP_APP_URL  = "https://espinosa-world-cup.streamlit.app"
FANTASY_APP_URL    = "https://insertwittynamehere.streamlit.app"
DYNASTY_APP_URL    = "https://anewdynasty.streamlit.app"

PROJECTS = [
    {
        "title":       "World Cup Family HQ",
        "description": "Our family's World Cup central hub. Pools, passports, match tracking, leaderboards, and more.",
        "url":         WORLD_CUP_APP_URL,
        "thumbnail":   "assets/worldcup_hq_image.png",
        "icon":        "⚽",
        "obj_pos":     "center center",
        "fallback_gradient": "linear-gradient(160deg, #0a2010 0%, #1a4a20 45%, #0d3515 100%)",
    },
    {
        "title":       "{insert witty name here} Museum",
        "description": "Explore 25 seasons of league history, analytics, records, and memories.",
        "url":         FANTASY_APP_URL,
        "thumbnail":   "assets/25_FFL.png",
        "icon":        "🏈",
        "obj_pos":     "center center",
        "fallback_gradient": "linear-gradient(160deg, #1a0800 0%, #3d1500 45%, #1a0800 100%)",
    },
    {
        "title":       "A New Dynasty FFL Museum",
        "description": "A second league, a new chapter. Track history, rivalries, and records from a fresh dynasty in the making.",
        "url":         DYNASTY_APP_URL,
        "thumbnail":   "assets/dynasty_thumbnail.png",
        "icon":        "🏆",
        "obj_pos":     "center center",
        "fallback_gradient": "linear-gradient(160deg, #0a0a2a 0%, #1a1a4a 45%, #0a0a2a 100%)",
    },
]

_TROPHY_SVG = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M19 5h-2V3H7v2H5C3.9 5 3 5.9 3 7v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v1c0 .34.03.67.08 1H5.08C5.03 8.67 5 8.34 5 8zm7 6c-1.65 0-3-1.35-3-3V5h6v6c0 1.65-1.35 3-3 3zm7-6c0 .34-.03.67-.08 1h-2.08c.05-.33.08-.66.08-1V7h2v1z"/></svg>'
_MUSIC_SVG  = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>'
_GAME_SVG   = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5S14.67 12 15.5 12s1.5.67 1.5 1.5S16.33 15 15.5 15zm3-3c-.83 0-1.5-.67-1.5-1.5S17.67 10 18.5 10s1.5.67 1.5 1.5S19.33 12 18.5 12z"/></svg>'

COMING_SOON = [
    {"svg": _TROPHY_SVG, "title": "Fantasy League 3",       "subtitle": "Coming soon", "color": "#a855f7", "bg": "rgba(168,85,247,0.15)"},
    {"svg": _MUSIC_SVG,  "title": "Seattle Concert Finder", "subtitle": "Coming soon", "color": "#22c55e", "bg": "rgba(34,197,94,0.15)"},
    {"svg": _GAME_SVG,   "title": "Strategy Game Prototype","subtitle": "Coming soon", "color": "#f59e0b", "bg": "rgba(245,158,11,0.15)"},
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def img_to_data_uri(path: str) -> str | None:
    try:
        p = Path(path)
        ext = p.suffix.lstrip(".").lower()
        if ext == "jpg":
            ext = "jpeg"
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{ext};base64,{b64}"
    except FileNotFoundError:
        return None


def project_card_html(p: dict) -> str:
    uri = img_to_data_uri(p["thumbnail"])
    obj_pos = p.get("obj_pos", "center center")
    if uri:
        thumb = (
            f'<img src="{uri}" alt="{p["title"]}" '
            f'style="width:100%;height:100%;object-fit:cover;object-position:{obj_pos};display:block;">'
        )
    else:
        thumb = (
            f'<div style="width:100%;height:100%;background:{p["fallback_gradient"]};'
            f'display:flex;align-items:center;justify-content:center;font-size:80px;">'
            f'{p["icon"]}</div>'
        )

    disabled   = p["url"].startswith("PASTE")
    btn_href   = "#" if disabled else p["url"]
    btn_target = "" if disabled else 'target="_blank" rel="noopener noreferrer"'
    btn_bg     = "background:#4a6fa5;cursor:not-allowed;" if disabled else "background:#2d7ef8;"

    return f"""
<div class="proj-card">
  <div class="proj-thumb">{thumb}</div>
  <div class="proj-body">
    <div class="proj-icon">{p["icon"]}</div>
    <div class="proj-title">{p["title"]}</div>
    <div class="proj-desc">{p["description"]}</div>
    <a href="{btn_href}" {btn_target} class="proj-btn" style="{btn_bg}">Launch App →</a>
  </div>
</div>"""


def coming_soon_card_html(item: dict) -> str:
    return f"""
<div class="cs-card">
  <div class="cs-icon" style="background:{item['bg']};color:{item['color']};">{item['svg']}</div>
  <div>
    <div class="cs-title">{item['title']}</div>
    <div class="cs-sub">{item['subtitle']}</div>
  </div>
</div>"""


# ── Main Render ───────────────────────────────────────────────────────────────

def render():
    hero_uri = img_to_data_uri("assets/seattle_hero.png")
    hero_bg_css = (
        f"background-image:url('{hero_uri}');background-size:cover;background-position:center top;"
        if hero_uri
        else "background:linear-gradient(135deg,#080d1a 0%,#0b1530 20%,#0f2044 38%,#080d1a 100%);"
    )

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ── Strip Streamlit chrome ── */
#MainMenu,footer,
[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],[data-testid="stHeader"],
header,.stDeployButton
{{display:none!important;visibility:hidden!important;}}

/* ── App background ── */
.stApp{{background:#080d1a!important;}}

/* ── Remove all default Streamlit padding/gaps ── */
.main,.main>div{{padding:0!important;}}
.block-container{{padding:0!important;max-width:100%!important;margin:0!important;}}
[data-testid="stMainBlockContainer"]{{padding:0!important;max-width:100%!important;}}
[data-testid="stMain"]{{padding:0!important;}}
.stMarkdown,[data-testid="stMarkdownContainer"]{{margin:0!important;padding:0!important;}}
div[data-testid="stVerticalBlock"]{{gap:0!important;}}
div[data-testid="stVerticalBlock"]>div{{margin:0!important;padding:0!important;}}

/* ── Base font ── */
*,*::before,*::after{{box-sizing:border-box;}}
body,.stMarkdown p,.stMarkdown div,.stMarkdown span{{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif!important;
}}

/* ══════════════════════════════════════════════════════
   HERO — cleaner, slightly shorter
══════════════════════════════════════════════════════ */
.hero{{
  position:relative;height:550px;
  {hero_bg_css}
  display:flex;align-items:flex-start;overflow:hidden;
}}
.hero-overlay{{
  position:absolute;inset:0;
  background:
    linear-gradient(to right,  rgba(8,13,26,.90) 0%, rgba(8,13,26,.65) 40%, rgba(8,13,26,.12) 65%, transparent 100%),
    linear-gradient(to bottom, transparent 50%, rgba(8,13,26,0.82) 100%);
}}
.hero-content{{position:relative;z-index:2;padding:72px 3rem 0;max-width:640px;}}
.hero-title{{font-size:86px;font-weight:900;line-height:1;letter-spacing:-3px;margin-bottom:16px;}}
.hero-white{{color:#fff;}}
.hero-blue{{color:#3b82f6;}}
.hero-tagline{{font-size:19px;font-weight:500;color:rgba(255,255,255,0.78);line-height:1.5;max-width:480px;}}

/* ══════════════════════════════════════════════════════
   FEATURED PROJECTS — floats over bottom of hero
══════════════════════════════════════════════════════ */
.proj-section{{
  position:relative;z-index:5;
  margin-top:-115px;
  padding:0 3rem;
  background:transparent;
}}
.sec-hdr{{
  display:flex;align-items:center;gap:12px;
  padding:0 0 20px;
  font-size:20px;font-weight:700;color:#fff;
  text-shadow:0 2px 12px rgba(0,0,0,0.8);
}}
.sec-bar{{width:4px;height:24px;background:#3b82f6;border-radius:2px;flex-shrink:0;}}

/* ══════════════════════════════════════════════════════
   PROJECT CARDS
══════════════════════════════════════════════════════ */
.proj-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding-bottom:0;}}
.proj-card{{
  background:rgba(12,20,38,0.97);
  border:1px solid rgba(59,130,246,0.22);
  border-radius:16px;overflow:hidden;
  display:flex;height:260px;
  transition:border-color .3s,transform .25s,box-shadow .3s;
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
}}
.proj-card:hover{{
  border-color:rgba(59,130,246,.6);
  transform:translateY(-3px);
  box-shadow:0 24px 64px rgba(0,0,0,0.5),0 0 0 1px rgba(59,130,246,0.15);
}}
.proj-thumb{{flex:0 0 48%;position:relative;overflow:hidden;}}
.proj-body{{
  flex:1;padding:26px 26px 22px;
  display:flex;flex-direction:column;
}}
.proj-icon{{font-size:20px;margin-bottom:10px;}}
.proj-title{{font-size:20px;font-weight:700;color:#fff;margin-bottom:10px;line-height:1.25;}}
.proj-desc{{font-size:13.5px;color:#94a3b8;line-height:1.6;flex-grow:1;margin-bottom:18px;}}
.proj-btn{{
  display:inline-flex;align-items:center;gap:8px;
  color:#fff!important;text-decoration:none!important;
  font-size:14px;font-weight:700;padding:10px 22px;
  border-radius:8px;width:fit-content;letter-spacing:0.2px;
  transition:filter .2s,transform .15s;
}}
.proj-btn:hover{{filter:brightness(1.2);transform:translateX(3px);}}

/* ══════════════════════════════════════════════════════
   GENERAL SECTION (coming soon, etc.)
══════════════════════════════════════════════════════ */
.section{{padding:0 3rem;background:#080d1a;}}
.section-hdr{{
  display:flex;align-items:center;gap:12px;
  padding:44px 0 24px;
  font-size:20px;font-weight:700;color:#fff;
}}

/* ══════════════════════════════════════════════════════
   COMING SOON CARDS
══════════════════════════════════════════════════════ */
.cs-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;padding-bottom:52px;}}
.cs-card{{
  background:rgba(15,23,42,0.5);
  border:1.5px dashed rgba(100,116,139,0.3);
  border-radius:12px;padding:24px 20px;
  display:flex;align-items:center;gap:14px;
  transition:border-color .3s,background .3s;
}}
.cs-card:hover{{
  border-color:rgba(59,130,246,0.4);
  background:rgba(15,23,42,0.75);
}}
.cs-icon{{
  width:50px;height:50px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}}
.cs-title{{font-size:14px;font-weight:600;color:#fff;margin-bottom:3px;}}
.cs-sub{{font-size:12px;color:#64748b;}}

/* ══════════════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════════════ */
.footer{{
  border-top:1px solid rgba(255,255,255,0.07);
  padding:26px 3rem;
  display:flex;align-items:center;justify-content:center;
  gap:20px;background:#080d1a;
}}
.footer-text{{font-size:14px;color:#64748b;}}
.footer-divider{{width:1px;height:18px;background:rgba(255,255,255,0.12);}}
.footer-icons{{display:flex;align-items:center;gap:20px;}}
.footer-icon{{color:#64748b;text-decoration:none;transition:color .2s;display:flex;align-items:center;}}
.footer-icon:hover{{color:#fff;}}

/* ══════════════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════════════ */
@media(max-width:1024px){{
  .proj-grid{{grid-template-columns:1fr;}}
  .proj-card{{height:auto;min-height:220px;}}
  .proj-section{{margin-top:-60px;}}
}}
@media(max-width:960px){{
  .cs-grid{{grid-template-columns:1fr 1fr;}}
  .proj-card{{flex-direction:column;}}
  .proj-thumb{{flex:0 0 200px;}}
  .hero-title{{font-size:60px;}}
  .hero{{height:460px;}}
  .hero-content{{padding-top:60px;}}
  .nav,.proj-section,.section,.footer{{padding-left:1.5rem!important;padding-right:1.5rem!important;}}
}}
@media(max-width:600px){{
  .cs-grid{{grid-template-columns:1fr;}}
  .hero-title{{font-size:46px;}}
  .hero{{height:380px;}}
  .hero-content{{padding-top:50px;}}
  .proj-section{{margin-top:-60px;}}
}}
</style>
""", unsafe_allow_html=True)

    # ── Hero (clean — title + one tagline only) ──────────────────────────────
    st.markdown("""
<div class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-title">
      <span class="hero-white">sme</span><span class="hero-blue">327</span>
    </div>
    <div class="hero-tagline">Exploring the world together through sports, data, and curiosity.</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Featured Projects (floats over hero bottom) ──────────────────────────
    cards_html = "\n".join(project_card_html(p) for p in PROJECTS)
    st.markdown(f"""
<div class="proj-section" id="projects">
  <div class="sec-hdr">
    <div class="sec-bar"></div>
    Featured Projects
  </div>
  <div class="proj-grid">
    {cards_html}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Coming Soon ──────────────────────────────────────────────────────────
    cs_html = "\n".join(coming_soon_card_html(c) for c in COMING_SOON)
    st.markdown(f"""
<div class="section" id="coming-soon">
  <div class="section-hdr">
    <div class="sec-bar"></div>
    🚀 More Projects Coming Soon
  </div>
  <div class="cs-grid">
    {cs_html}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown("""
<div class="footer">
  <span class="footer-text">Thanks for checking out my work!</span>
  <div class="footer-divider"></div>
  <div class="footer-icons">
    <a href="https://github.com/sme327" target="_blank" rel="noopener noreferrer"
       class="footer-icon" title="GitHub">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385
                 .6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235
                 -3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695
                 -.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23
                 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605
                 -2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225
                 -.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23
                 .96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23
                 .66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225
                 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22
                 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57
                 A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
      </svg>
    </a>
    <a href="https://www.linkedin.com/in/shawn-espinosa-b1240514/" target="_blank" rel="noopener noreferrer"
       class="footer-icon" title="LinkedIn">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037
                 -1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046
                 c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286z
                 M5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065z
                 m1.782 13.019H3.555V9h3.564v11.452z
                 M22.225 0H1.771C.792 0 0 .774 0 1.729v20.542
                 C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271
                 V1.729C24 .774 23.2 0 22.222 0h.003z"/>
      </svg>
    </a>
    <a href="mailto:sme327@gmail.com" class="footer-icon" title="Email">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2"
           stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
        <polyline points="22,6 12,13 2,6"/>
      </svg>
    </a>
  </div>
</div>
""", unsafe_allow_html=True)


render()
