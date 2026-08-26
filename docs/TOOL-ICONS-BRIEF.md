# Tool-card icons — brief for the graphics team

Two icons for the **Productivity & Tools** cards on sme327.com. Interim versions are live (`assets/draft_room_icon.png`, `assets/keeper_tool_icon.png`, generated line art); these are drop-in replacements — same filenames, same size — and the page needs no code change when they land.

## The look (match `assets/next_icon.png`, the existing tool icon)

- **Format:** PNG, **256×256** rendered for a 128×128 tile (2×), true alpha outside the tile. Ceiling 60 KB each.
- **Tile:** rounded square (radius ≈ 20% of width), dark navy gradient `#1b2230 → #0b0f17`, a 1px `rgba(255,255,255,.08)` inner rim. The card shows it at 42×42 px, so the subject must read at that size — **one strong silhouette, no fine detail, no text**.
- **Line art:** single-weight strokes (≈ 3.4 units at 128), rounded caps, with a soft glow in the accent colour. One accent per icon, plus at most two small secondary dots.
- **Football feel:** each icon includes a football (laced, on a diagonal) as a secondary element — the site's tools are all fantasy football, and the ball is what ties the two together visually. The ball is line art in the accent colour, not a photoreal ball, not an emoji.
- No NFL/team marks, no league names, no words.

## Icon 1 — `draft_room_icon.png` · "{insert witty name here} Draft Room"

- Accent: **green `#22c55e`** (the card's accent; matches the existing card border).
- Subject: a **draft board** — a clipboard/board with 3–4 ranked rows (small coloured dots for player slots: green, orange `#f97316`, blue `#4db8ff`) and a football tucked at the lower right.
- Reads as: "the board on draft night."

## Icon 2 — `keeper_tool_icon.png` · "A New Dynasty Keeper Tool"

- Accent: **antique gold `#d4af37`** (the museum's gold — the tool and the museum are siblings).
- Subject: a **keeper price tag** — a hanging tag with a ring hole, a bold `$` on its face, two short lines beneath (the price ledger), and a football at the lower right. It's the same "keeper tag" object the museum uses on its Keeper Hall chains, so the two sites rhyme.
- Reads as: "what it costs to keep him."

## QA (what we check before wiring in)

1. Dimensions 256×256, alpha outside the tile, ≤ 60 KB.
2. Legible at 42 px on the dark card background `#0c1426` — the silhouette must survive.
3. Palette: only the tile navy, the accent, `#f97316`/`#4db8ff` dots on the draft board, and white ≤ 10%.
4. No text or league marks baked in.

Deliver both files to `assets/`; run `python build.py`; commit. The interim icons are the reference for composition, not for finish.
