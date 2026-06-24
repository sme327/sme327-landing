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

WORLD_CUP_APP_URL = "PASTE_WORLD_CUP_LINK_HERE"
FANTASY_APP_URL = "PASTE_FANTASY_LINK_HERE"

TAG_STYLE = {
    "Streamlit":        ("rgba(96,165,250,0.12)",  "rgba(96,165,250,0.35)",  "#60a5fa"),
    "Sports":           ("rgba(52,211,153,0.12)",  "rgba(52,211,153,0.35)",  "#34d399"),
    "Family":           ("rgba(192,132,252,0.12)", "rgba(192,132,252,0.35)", "#c084fc"),
    "Fantasy Football": ("rgba(52,211,153,0.12)",  "rgba(52,211,153,0.35)",  "#34d399"),
    "Analytics":        ("rgba(192,132,252,0.12)", "rgba(192,132,252,0.35)", "#c084fc"),
    "Data":             ("rgba(251,191,36,0.12)",  "rgba(251,191,36,0.35)",  "#fbbf24"),
}

PROJECTS = [
    {
        "title": "World Cup Family HQ",
        "description": "Our family's World Cup central hub. Pools, passports, match tracking, leaderboards, and more.",
        "tags": ["Streamlit", "Sports", "Family"],
        "url": WORLD_CUP_APP_URL,
        "thumbnail": "assets/world_cup_thumbnail.png",
        "icon": "⚽",
        "fallback_gradient": "linear-gradient(160deg, #0a2010 0%, #1a4a20 45%, #0d3515 100%)",
    },
    {
        "title": "25-Year Fantasy Football Museum",
        "description": "Explore 25 seasons of league history, analytics, records, and memories.",
        "tags": ["Streamlit", "Fantasy Football", "Analytics"],
        "url": FANTASY_APP_URL,
        "thumbnail": "assets/fantasy_thumbnail.png",
        "icon": "🏈",
        "fallback_gradient": "linear-gradient(160deg, #1a0800 0%, #3d1500 45%, #1a0800 100%)",
    },
]

_TROPHY_SVG = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M19 5h-2V3H7v2H5C3.9 5 3 5.9 3 7v1c0 2.55 1.92 4.63 4.39 4.94.63 1.5 1.98 2.63 3.61 2.96V19H7v2h10v-2h-4v-3.1c1.63-.33 2.98-1.46 3.61-2.96C19.08 12.63 21 10.55 21 8V7c0-1.1-.9-2-2-2zM5 8V7h2v1c0 .34.03.67.08 1H5.08C5.03 8.67 5 8.34 5 8zm7 6c-1.65 0-3-1.35-3-3V5h6v6c0 1.65-1.35 3-3 3zm7-6c0 .34-.03.67-.08 1h-2.08c.05-.33.08-.66.08-1V7h2v1z"/></svg>'
_MUSIC_SVG  = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/></svg>'
_GAME_SVG   = '<svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor"><path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5S14.67 12 15.5 12s1.5.67 1.5 1.5S16.33 15 15.5 15zm3-3c-.83 0-1.5-.67-1.5-1.5S17.67 10 18.5 10s1.5.67 1.5 1.5S19.33 12 18.5 12z"/></svg>'

COMING_SOON = [
    {"svg": _TROPHY_SVG, "title": "Fantasy League 2",      "subtitle": "Coming soon", "color": "#3b82f6", "bg": "rgba(59,130,246,0.15)"},
    {"svg": _TROPHY_SVG, "title": "Fantasy League 3",      "subtitle": "Coming soon", "color": "#a855f7", "bg": "rgba(168,85,247,0.15)"},
    {"svg": _MUSIC_SVG,  "title": "Seattle Concert Finder","subtitle": "Coming soon", "color": "#22c55e", "bg": "rgba(34,197,94,0.15)"},
    {"svg": _GAME_SVG,   "title": "Strategy Game Prototype","subtitle":"Coming soon", "color": "#f59e0b", "bg": "rgba(245,158,11,0.15)"},
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


def tag_html(label: str) -> str:
    bg, border, color = TAG_STYLE.get(label, ("rgba(148,163,184,0.12)", "rgba(148,163,184,0.35)", "#94a3b8"))
    return (
        f'<span style="background:{bg};border:1px solid {border};color:{color};'
        f'padding:4px 12px;border-radius:100px;font-size:12px;font-weight:500;">'
        f'{label}</span>'
    )


def project_card_html(p: dict) -> str:
    uri = img_to_data_uri(p["thumbnail"])
    if uri:
        thumb = f'<img src="{uri}" alt="{p["title"]}" style="width:100%;height:100%;object-fit:cover;display:block;">'
    else:
        thumb = (
            f'<div style="width:100%;height:100%;background:{p["fallback_gradient"]};'
            f'display:flex;align-items:center;justify-content:center;font-size:80px;">'
            f'{p["icon"]}</div>'
        )

    tags = " ".join(tag_html(t) for t in p["tags"])

    disabled = p["url"].startswith("PASTE")
    btn_href   = "#" if disabled else p["url"]
    btn_target = "" if disabled else 'target="_blank" rel="noopener noreferrer"'
    btn_style  = "background:#374151;cursor:not-allowed;" if disabled else "background:#3b82f6;"

    return f"""
<div class="proj-card">
  <div class="proj-thumb">{thumb}</div>
  <div class="proj-body">
    <div style="font-size:22px;margin-bottom:12px;">{p["icon"]}</div>
    <div class="proj-title">{p["title"]}</div>
    <div class="proj-desc">{p["description"]}</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px;">{tags}</div>
    <a href="{btn_href}" {btn_target} class="proj-btn" style="{btn_style}">Open App →</a>
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
    if hero_uri:
        hero_bg_css = f"background-image:url('{hero_uri}');background-size:cover;background-position:center top;"
    else:
        hero_bg_css = (
            "background:linear-gradient(135deg,"
            "#080d1a 0%,#0b1530 20%,#0f2044 38%,"
            "#0d1a35 55%,#080d1a 100%);"
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

/* ── Remove all default padding from Streamlit containers ── */
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
   NAV BAR
══════════════════════════════════════════════════════ */
.nav{{
  position:sticky;top:0;z-index:1000;
  background:rgba(8,13,26,0.97);
  backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(59,130,246,0.18);
  padding:0 3rem;height:65px;
  display:flex;align-items:center;justify-content:space-between;
}}
.nav-brand{{display:flex;align-items:center;gap:12px;text-decoration:none;}}
.nav-rocket{{font-size:26px;line-height:1;}}
.nav-name{{font-size:20px;font-weight:800;color:#fff;letter-spacing:-0.5px;line-height:1.1;}}
.nav-sub{{font-size:10px;font-weight:600;color:#64748b;letter-spacing:2.5px;text-transform:uppercase;}}
.nav-links{{display:flex;align-items:center;gap:4px;}}
.nav-link{{
  color:#94a3b8;text-decoration:none;font-size:15px;font-weight:500;
  padding:8px 16px;border-radius:6px;position:relative;transition:color .2s;
}}
.nav-link:hover{{color:#fff;}}
.nav-link.active{{color:#fff;}}
.nav-link.active::after{{
  content:'';position:absolute;bottom:4px;left:16px;right:16px;
  height:2px;background:#3b82f6;border-radius:2px;
}}
.nav-contact{{
  display:flex;align-items:center;gap:7px;
  color:#fff;text-decoration:none;font-size:14px;font-weight:600;
  padding:8px 18px;border:1.5px solid rgba(255,255,255,0.25);
  border-radius:8px;margin-left:8px;transition:all .2s;
}}
.nav-contact:hover{{border-color:#3b82f6;color:#60a5fa;}}

/* ══════════════════════════════════════════════════════
   HERO
══════════════════════════════════════════════════════ */
.hero{{
  position:relative;min-height:430px;
  {hero_bg_css}
  display:flex;align-items:center;overflow:hidden;
}}
.hero-overlay{{
  position:absolute;inset:0;
  background:linear-gradient(
    to right,
    rgba(8,13,26,.94) 0%,
    rgba(8,13,26,.75) 38%,
    rgba(8,13,26,.25) 62%,
    rgba(8,13,26,.08) 100%
  );
}}
.hero-content{{position:relative;z-index:2;padding:64px 3rem;max-width:680px;}}
.hero-title{{font-size:84px;font-weight:900;line-height:1;letter-spacing:-3px;margin-bottom:22px;}}
.hero-white{{color:#fff;}}
.hero-blue{{color:#3b82f6;}}
.hero-sub{{font-size:22px;font-weight:700;color:#fff;line-height:1.35;margin-bottom:14px;}}
.hero-body{{font-size:15px;color:#94a3b8;line-height:1.75;margin-bottom:32px;}}
.pills{{display:flex;flex-wrap:nowrap;gap:8px;}}
.pill{{
  display:flex;align-items:center;gap:5px;
  background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.14);
  border-radius:100px;padding:6px 13px;
  font-size:13px;font-weight:500;color:#e2e8f0;white-space:nowrap;
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
}}

/* ══════════════════════════════════════════════════════
   SECTIONS
══════════════════════════════════════════════════════ */
.section{{padding:0 3rem;background:#080d1a;}}
.sec-hdr{{
  display:flex;align-items:center;gap:12px;
  padding:42px 0 28px;
  font-size:22px;font-weight:700;color:#fff;
}}
.sec-bar{{width:4px;height:26px;background:#3b82f6;border-radius:2px;flex-shrink:0;}}

/* ══════════════════════════════════════════════════════
   PROJECT CARDS
══════════════════════════════════════════════════════ */
.proj-grid{{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding-bottom:16px;}}
.proj-card{{
  background:rgba(15,23,42,0.96);
  border:1px solid rgba(59,130,246,0.2);
  border-radius:16px;overflow:hidden;
  display:flex;min-height:265px;
  transition:border-color .3s,transform .25s,box-shadow .3s;
}}
.proj-card:hover{{
  border-color:rgba(59,130,246,.55);
  transform:translateY(-3px);
  box-shadow:0 20px 60px rgba(59,130,246,0.12);
}}
.proj-thumb{{flex:0 0 42%;position:relative;overflow:hidden;}}
.proj-body{{flex:1;padding:28px 28px 24px;display:flex;flex-direction:column;}}
.proj-title{{font-size:22px;font-weight:700;color:#fff;margin-bottom:12px;line-height:1.25;}}
.proj-desc{{font-size:14px;color:#94a3b8;line-height:1.65;margin-bottom:20px;flex-grow:1;}}
.proj-btn{{
  display:inline-flex;align-items:center;gap:8px;
  color:#fff!important;text-decoration:none!important;
  font-size:15px;font-weight:600;padding:11px 24px;
  border-radius:8px;width:fit-content;
  transition:filter .2s,transform .15s;
}}
.proj-btn:hover{{filter:brightness(1.18);transform:translateX(2px);}}

/* ══════════════════════════════════════════════════════
   COMING SOON CARDS
══════════════════════════════════════════════════════ */
.cs-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;padding-bottom:52px;}}
.cs-card{{
  background:rgba(15,23,42,0.5);
  border:1.5px dashed rgba(100,116,139,0.3);
  border-radius:12px;padding:26px 22px;
  display:flex;align-items:center;gap:16px;
  transition:border-color .3s,background .3s;
}}
.cs-card:hover{{
  border-color:rgba(59,130,246,0.4);
  background:rgba(15,23,42,0.75);
}}
.cs-icon{{
  width:52px;height:52px;border-radius:12px;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}}
.cs-title{{font-size:15px;font-weight:600;color:#fff;margin-bottom:3px;}}
.cs-sub{{font-size:13px;color:#64748b;}}

/* ══════════════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════════════ */
.footer{{
  border-top:1px solid rgba(255,255,255,0.08);
  padding:28px 3rem;
  display:flex;align-items:center;justify-content:center;
  gap:20px;background:#080d1a;
}}
.footer-text{{font-size:14px;color:#64748b;}}
.footer-divider{{width:1px;height:18px;background:rgba(255,255,255,0.15);}}
.footer-icons{{display:flex;align-items:center;gap:22px;}}
.footer-icon{{color:#64748b;text-decoration:none;transition:color .2s;display:flex;align-items:center;}}
.footer-icon:hover{{color:#fff;}}

/* ══════════════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════════════ */
@media(max-width:960px){{
  .proj-grid{{grid-template-columns:1fr;}}
  .cs-grid{{grid-template-columns:1fr 1fr;}}
  .proj-card{{flex-direction:column;min-height:auto;}}
  .proj-thumb{{flex:0 0 220px;}}
  .hero-title{{font-size:58px;}}
  .nav,.section,.footer{{padding-left:1.5rem!important;padding-right:1.5rem!important;}}
}}
@media(max-width:600px){{
  .cs-grid{{grid-template-columns:1fr;}}
  .hero-title{{font-size:44px;}}
  .nav-links .nav-link:not(.active){{display:none;}}
}}
</style>
""", unsafe_allow_html=True)

    # ── Navigation ──────────────────────────────────────────────────────────
    st.markdown("""
<nav class="nav">
  <a href="#" class="nav-brand">
    <span class="nav-rocket">🚀</span>
    <div>
      <div class="nav-name">sme327</div>
      <div class="nav-sub">Project Hub</div>
    </div>
  </a>
  <div class="nav-links">
    <a href="#" class="nav-link active">Home</a>
    <a href="#projects" class="nav-link">Projects</a>
    <a href="#about" class="nav-link">About Me</a>
    <a href="#tech" class="nav-link">Tech Stack</a>
    <a href="mailto:sme327@gmail.com" class="nav-contact">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
           stroke="currentColor" stroke-width="2.5"
           stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
        <polyline points="22,6 12,13 2,6"/>
      </svg>
      Contact
    </a>
  </div>
</nav>
""", unsafe_allow_html=True)

    # ── Hero ────────────────────────────────────────────────────────────────
    st.markdown("""
<div class="hero">
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-title">
      <span class="hero-white">sme</span><span class="hero-blue">327</span>
    </div>
    <div class="hero-sub">
      Projects, dashboards, and tools<br>built with data, code, and curiosity.
    </div>
    <div class="hero-body">
      Explore my collection of interactive apps and tools.<br>
      More projects and experiments coming soon!
    </div>
    <div class="pills">
      <span class="pill">👑 Streamlit</span>
      <span class="pill">🐍 Python</span>
      <span class="pill">📊 Data</span>
      <span class="pill">⚽ Sports</span>
      <span class="pill">📈 Analytics</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Featured Projects ────────────────────────────────────────────────────
    cards_html = "\n".join(project_card_html(p) for p in PROJECTS)
    st.markdown(f"""
<div class="section" id="projects">
  <div class="sec-hdr">
    <div class="sec-bar"></div>
    Featured Projects
  </div>
  <div class="proj-grid">
    {cards_html}
  </div>
</div>
""", unsafe_allow_html=True)

    # ── Coming Soon ─────────────────────────────────────────────────────────
    cs_html = "\n".join(coming_soon_card_html(c) for c in COMING_SOON)
    st.markdown(f"""
<div class="section" id="coming-soon">
  <div class="sec-hdr">
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
    <a href="https://linkedin.com/in/sme327" target="_blank" rel="noopener noreferrer"
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
