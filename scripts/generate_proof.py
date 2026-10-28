#!/usr/bin/env python3
"""
Self-hosted proof panel for the skayy47 profile README.

Replaces github-readme-stats / top-langs / activity-graph, which were returning
503 / 503 / 402 (Payment Required) and rendering as broken images.

Every number here is traceable to a repo:
  84  -> maestro/README.md  ("Tests-84_passing" badge, 15 Vitest suites)
  147 -> nexus/README.md    ("147 tests pass, 7 skipped", re-run 2026-10-28)
  55  -> AURA/README.md     ("Last result: 55/55 passed (100%)" overtest, 5 datasets)
  0.7748 AUC -> credit-risk-prediction (Champion v2, LightGBM + 31 relational features)
  2.17% MAPE -> walmart-sales-forecasting (Prophet + Optuna)

Run from repo root:  python scripts/generate_proof.py
"""
import os

THEMES = {
    "dark": dict(
        bg="#0B0F1A", bg2="#111C2E", card="#0F1726", border="#1E2A3D",
        value="#E6EDF7", label="#8296B0", accent="#6E9FD4", grid_op="0.06",
    ),
    "light": dict(
        bg="#FCFDFF", bg2="#E8F0F9", card="#FFFFFF", border="#DCE6F2",
        value="#0F1B2D", label="#566880", accent="#2C5F94", grid_op="0.07",
    ),
}

TILES = [
    ("3",      "LIVE PRODUCTION SYSTEMS"),
    ("286",    "TESTS + E2E CHECKS PASSING"),
    ("0.775",  "AUC · CREDIT RISK MODEL"),
    ("2.17%",  "MAPE · DEMAND FORECASTING"),
]

W, H = 1000, 156
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def build(t: dict) -> str:
    pad, gap = 22, 16
    n = len(TILES)
    cw = (W - pad * 2 - gap * (n - 1)) / n
    cards = []
    for i, (val, lab) in enumerate(TILES):
        x = pad + i * (cw + gap)
        cx = x + cw / 2
        cards.append(f'''
  <g>
    <rect x="{x:.1f}" y="26" width="{cw:.1f}" height="104" rx="10"
          fill="{t['card']}" stroke="{t['border']}" stroke-width="1"/>
    <rect x="{x:.1f}" y="26" width="{cw:.1f}" height="2.5" rx="1.25" fill="{t['accent']}" opacity="0.85"/>
    <text x="{cx:.1f}" y="88" text-anchor="middle" font-family="{MONO}"
          font-size="34" font-weight="700" fill="{t['value']}" letter-spacing="1">{val}</text>
    <text x="{cx:.1f}" y="111" text-anchor="middle" font-family="{MONO}"
          font-size="9.5" font-weight="500" fill="{t['label']}" letter-spacing="1.5">{lab}</text>
  </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Proof: 3 live production systems, 286 tests and end-to-end checks passing, 0.775 AUC credit risk model, 2.17 percent MAPE demand forecasting">
  <defs>
    <linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{t['bg']}"/>
      <stop offset="100%" stop-color="{t['bg2']}"/>
    </linearGradient>
    <pattern id="pgrid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{t['accent']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{W}" height="{H}" rx="12" fill="url(#pbg)"/>
  <rect width="{W}" height="{H}" rx="12" fill="url(#pgrid)"/>
  <text x="{pad}" y="17" font-family="{MONO}" font-size="9.5" font-weight="600"
        fill="{t['label']}" letter-spacing="2.6">VERIFIED PROOF &#183; EVERY NUMBER TRACEABLE TO A REPO</text>
{"".join(cards)}
  <text x="{W - pad}" y="147" text-anchor="end" font-family="{MONO}" font-size="8.5"
        fill="{t['label']}" letter-spacing="1" opacity="0.75">MAESTRO 84 &#183; nexus 147 &#183; AURA 55</text>
</svg>
'''


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    for name, t in THEMES.items():
        p = os.path.join(out, f"proof-{name}.svg")
        with open(p, "w", encoding="utf-8") as f:
            f.write(build(t))
        print(f"wrote {os.path.basename(p)}  ({os.path.getsize(p)} bytes)")
