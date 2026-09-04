# Publishing on sme327.com

For an agent working in *any* project folder that needs to get something onto
sme327.com. You do not need to read `streamlit_app.py` end to end — this file
has the parts that matter and the mistakes that are easy to make.

Two different things get called "publishing" here. Do the one you need:

| You want to… | Go to |
|---|---|
| Put a project **card** on the sme327.com hub | [A. Add a card](#a-add-a-card-to-the-hub) |
| Ship a change to the hub page itself | [B. Deploy the hub](#b-deploy-the-hub) |
| Stand up a **new site** at `something.sme327.com` | [C. A new subdomain](#c-a-new-subdomain) |

`sme327.com` is the hub: a single static page listing every project. It lives in
`sme327/Landing/` (repo `sme327/sme327-landing`). Every other site is its own
repo on its own subdomain. All of it is Cloudflare, all under the `sme327.com`
zone, on the account wrangler is already logged into locally.

---

## A. Add a card to the hub

Everything is data at the top of `streamlit_app.py`. Pick the list that fits:

| List | Renders as | Use for |
|---|---|---|
| `PROJECTS` | Large portrait card, artwork on top | A project with its own site and its own artwork |
| `FOOTBALL_TOOLS` | Compact icon card, under the league museums | A fantasy-football tool |
| `TOOLS` | Compact icon card, its own section | Any other working tool |
| `COMING_SOON` | Dashed placeholder | Something real but not deployed |

### A `PROJECTS` entry

```python
{
    "section":     "personal",              # football | family | personal
    "title":       "My Concert Archive",
    "description": "Every show I've been to, mapped by band, venue, and year.",
    "url":         CONCERT_ATLAS_URL,       # a constant at the top of the file
    "thumbnail":   "assets/concert_archive.webp",
    "icon":        "🎵",
    "obj_pos":     "center center",         # object-position; thumb is cropped 4/3
    "fallback_gradient": "linear-gradient(160deg, #1a0a2a 0%, #3d1a5c 45%, #1a0a2a 100%)",
},
```

`cta` optionally overrides the link text (default `"Visit Site →"`). Omit `url`
entirely and add `label` instead to render a chip rather than a link.

`section` only selects among sections that already exist. A **new** section
means editing `render()`, which is a design decision — ask first.

### A `TOOLS` / `FOOTBALL_TOOLS` entry

No thumbnail; an icon tile instead.

```python
{
    "title":       "Our Home",
    "description": "Everything that needs doing around one house, on one shared list.",
    "url":         OUR_HOME_URL,
    "cta":         "Public version coming soon",
    "icon":        "🛋️",                     # fallback if icon_asset is missing
    "icon_asset":  "assets/our_home_icon.png",
    "accent":      "#a3e635",               # tints the tile; take it from the artwork
},
```

If the app has its own PWA/favicon icon, **use it** — copy it into `assets/`,
downscale to 128px and palette-quantise (the tile renders at 42px and the PNG is
inlined into the HTML, so a 512px original is tens of KB of page weight for
nothing).

### The three link states, and picking the right one

This is the rule most often got wrong:

1. **Live link** — a real, public URL. Anyone can open it and see the thing.
2. **Pending** — set the URL constant to `"PASTE_SOMETHING_HERE"`. Any URL
   starting with `PASTE` renders grey and unclickable, automatically. Pair it
   with a `cta` that says *why* (e.g. `"Public version coming soon"`), so it
   reads as pending rather than broken.
3. **No link at all** — omit `url`, add `label` (e.g. `"Private build"`).

**A card must never send a visitor to a login screen.** If the project is
PIN-gated or behind Cloudflare Access, do one of:

- link to its **public surface** if it has one (Asst Coach's card points at
  `practice.sme327.com`, not `coach.sme327.com`);
- use state 3 if it will never be public;
- use state 2 if a public/demo version is genuinely planned.

### Artwork

Masters are PNGs in `assets/`; cards reference the `.webp`.

```bash
# drop the PNG master in assets/, then:
python optimize_assets.py       # needs Pillow; authoring-only, not a build dep
```

It converts every PNG whose `.webp` is missing or stale, and skips anything with
"icon" in its name (those are referenced as `.png`). Thumbnails are cropped to
`4/3` — set `obj_pos` so the subject stays in frame. Keep masters reasonable;
the whole page ships as one document plus extracted images.

### Then

```bash
python build.py                 # writes dist/; standard library only
```

and follow **B** below. Sanity-check `dist/index.html` for your new card before
pushing.

---

## B. Deploy the hub

**Cloudflare Pages builds on push. There is no deploy command to run.**

```bash
python build.py                 # optional locally; the host runs it too
git add -A && git commit && git push origin main
```

Pages is git-connected to `sme327/sme327-landing` with build command
`python build.py` and output directory `dist`. A push to `main` is live in
roughly **3–5 minutes**. Verify rather than assume:

```bash
curl -s https://sme327.com/ | grep -o 'Your New Card'
```

`dist/` is gitignored — the host rebuilds it. Don't commit it.

### Two rules that will silently break the build

- **No Streamlit widgets. Ever.** `build.py` renders the page by stubbing the
  `streamlit` module and capturing `st.markdown()` calls. `st.button`,
  `st.selectbox`, session state and callbacks all vanish from the static build
  without erroring. If real interactivity is needed, that's a hosting decision,
  not a code change.
- **All the CSS lives inside an f-string.** Literal CSS braces must be doubled
  (`.hero{{…}}`), and a value interpolated *into* that f-string must use single
  braces, because it is inserted verbatim and not re-parsed. Getting this wrong
  emits `.hero{{…}}` into the stylesheet, which the browser silently ignores.
  Always grep the built file for the rule you added.

---

## C. A new subdomain

The house pattern is a Cloudflare Worker with a custom-domain route:

```jsonc
// wrangler.jsonc
{
  "name": "my-project",
  "main": "...",
  "compatibility_date": "2026-08-01",
  "compatibility_flags": ["nodejs_compat"],
  "routes": [{ "pattern": "myproject.sme327.com", "custom_domain": true }],
  "observability": { "enabled": true }
}
```

`npx wrangler deploy` creates the DNS record and the route. A purely static site
can use Pages instead (`npx wrangler pages deploy dist --project-name <name>`).
`custom_domain: true` is what makes the subdomain resolve — without it the
Worker only answers on `*.workers.dev`.

Check the subdomain you want is free first; several are taken by projects whose
name doesn't match (`dynasty.sme327.com` is Dynasty 22, while A New Dynasty is
on `and.sme327.com`).

### Wire it into Status

`status.sme327.com` (in `sme327/Status/`) discovers sites from the analytics
data itself, so a new site appears **automatically** once it has a Cloudflare
Web Analytics beacon — no code change needed. Add an entry to `KNOWN` in
`Status/src/config.ts` only to give it a proper name, colour and blurb.

One Worker serving two hostnames needs a beacon token per hostname, chosen in
the browser (see `Tools/soccer-coach/app/layout.tsx` for that pattern).

### Secrets

API tokens are Worker secrets (`npx wrangler secret put NAME`) — never in
source, `vars`, or a committed `.dev.vars`.

---

## Checklist for a newly launched project

1. Site deployed and reachable at its subdomain (**C**)
2. Web Analytics beacon added; entry in `Status/src/config.ts` `KNOWN`
3. Artwork in `Landing/assets/` + `python optimize_assets.py`
4. Card added to the right list, with the right link state (**A**)
5. `python build.py`, then push (**B**), then curl the live site
6. Update `Landing/CLAUDE.md`'s project table and `Projects/README.md`'s
   deployed-sites list — both go stale fast, and a stale table is worse than
   none because the next agent believes it
