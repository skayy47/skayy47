#!/usr/bin/env python3
"""
Hero banner for the skayy47 GitHub profile — light + dark, SMIL-animated.

WHY SMIL AND NOT CSS KEYFRAMES
------------------------------
The first version of this banner animated with CSS @keyframes. GitHub serves
the file intact, but a README embeds it as <img>, and the animation never
visibly ran — the banner read as completely static.

SMIL (<animate>, <animateMotion>) is the primitive that demonstrably works in
that context: readme-typing-svg, which sat on this very profile for months and
visibly animated for everyone, is SMIL. So every moving part here is SMIL, and
CSS is used only for the static paint.

WHAT MOVES
----------
Three packets travel root -> specialist -> sink, continuously and staggered.
That is not decoration: it is the orchestration DAG the profile is about, so
the one animated element on the page depicts the thing being claimed.

Run from repo root:  python scripts/generate_hero.py
"""
import os

MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "dark": dict(
        bg1="#0B0F1A", bg2="#0E1524", bg3="#111C2E",
        ink1="#FFFFFF", ink2="#D7E4F5", ink3="#9FC0E4",
        sub="#8296B0", accent="#6E9FD4", edge="#3E5F8A", sink="#D7E4F5",
        grid_op="0.06", glow_op="0.30",
    ),
    "light": dict(
        bg1="#FCFDFF", bg2="#F4F8FC", bg3="#E8F0F9",
        ink1="#0B1524", ink2="#17304F", ink3="#2C5F94",
        sub="#566880", accent="#2C5F94", edge="#7FA3C9", sink="#0F1B2D",
        grid_op="0.07", glow_op="0.13",
    ),
}

# DAG geometry: one planner -> three specialists -> one synthesis
ROOT = (760, 110)
MIDS = [(840, 62), (840, 110), (840, 158)]
SINK = (920, 110)
CYCLE = 3.6          # seconds for one packet to cross the graph
STAGGER = CYCLE / 3  # packets evenly spaced so the graph is never idle


def build(t: dict) -> str:
    routes = []
    for i, (mx, my) in enumerate(MIDS):
        begin = f"{i * STAGGER:.2f}s"
        path = f"M{ROOT[0]},{ROOT[1]} L{mx},{my} L{SINK[0]},{SINK[1]}"
        routes.append(f'''
    <circle r="3.6" fill="{t['accent']}" opacity="0">
      <animateMotion path="{path}" dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.12;0.88;1"
               dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite"/>
    </circle>''')

    # each specialist brightens as its packet arrives (half a cycle in)
    nodes = []
    for i, (mx, my) in enumerate(MIDS):
        begin = f"{i * STAGGER:.2f}s"
        nodes.append(f'''
    <circle cx="{mx}" cy="{my}" r="5" fill="{t['accent']}" opacity="0.35">
      <animate attributeName="opacity" values="0.35;1;0.35" keyTimes="0;0.5;1"
               dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite"/>
      <animate attributeName="r" values="5;6.4;5" keyTimes="0;0.5;1"
               dur="{CYCLE}s" begin="{begin}" repeatCount="indefinite"/>
    </circle>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 220" width="1000" height="220" role="img" aria-label="Oussama Skia — AI Engineer, Data Scientist, Production AI Systems">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{t['bg1']}"/>
      <stop offset="55%" stop-color="{t['bg2']}"/>
      <stop offset="100%" stop-color="{t['bg3']}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset="18%" stop-color="{t['accent']}" stop-opacity="1"/>
      <stop offset="62%" stop-color="{t['edge']}" stop-opacity="0.78"/>
      <stop offset="100%" stop-color="{t['edge']}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="ink" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="{t['ink1']}"/>
      <stop offset="70%" stop-color="{t['ink2']}"/>
      <stop offset="100%" stop-color="{t['ink3']}"/>
    </linearGradient>
    <linearGradient id="sheen" x1="0" y1="0" x2="0" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t['accent']}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
      <animate attributeName="x1" values="-300;1000" dur="7s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="-100;1200" dur="7s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M28 0H0V28" fill="none" stroke="{t['accent']}" stroke-opacity="{t['grid_op']}" stroke-width="1"/>
    </pattern>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0%" stop-color="{t['accent']}" stop-opacity="{t['glow_op']}"/>
      <stop offset="100%" stop-color="{t['accent']}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <rect width="1000" height="220" fill="url(#bg)"/>
  <rect width="1000" height="220" fill="url(#grid)"/>
  <ellipse cx="845" cy="110" rx="190" ry="120" fill="url(#glow)"/>

  <text x="64" y="94" font-family="{MONO}" font-size="46" font-weight="700" letter-spacing="3" fill="url(#ink)">OUSSAMA SKIA</text>
  <!-- a slow light sweep across the wordmark, so the type is alive without moving -->
  <text x="64" y="94" font-family="{MONO}" font-size="46" font-weight="700" letter-spacing="3" fill="url(#sheen)">OUSSAMA SKIA</text>

  <text x="66" y="126" font-family="{MONO}" font-size="14" font-weight="500" letter-spacing="4.4" fill="{t['sub']}">AI ENGINEER &#183; DATA SCIENTIST &#183; PRODUCTION AI SYSTEMS</text>

  <rect x="66" y="144" width="430" height="2" fill="url(#rule)">
    <animate attributeName="width" values="0;430" dur="1.1s" begin="0s" fill="freeze"/>
  </rect>

  <text x="66" y="176" font-family="{MONO}" font-size="13" font-weight="500" letter-spacing="1.1" fill="{t['accent']}">Models hallucinate. Systems shouldn&#8217;t.</text>

  <g stroke="{t['edge']}" stroke-width="1.25" fill="none" opacity="0.85">
    <path d="M760 110 L840 62"/><path d="M760 110 L840 110"/><path d="M760 110 L840 158"/>
    <path d="M840 62 L920 110"/><path d="M840 110 L920 110"/><path d="M840 158 L920 110"/>
  </g>
{"".join(nodes)}
  <circle cx="{ROOT[0]}" cy="{ROOT[1]}" r="7" fill="{t['accent']}"/>
  <circle cx="{SINK[0]}" cy="{SINK[1]}" r="7" fill="{t['sink']}"/>
{"".join(routes)}
</svg>
'''


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    for name, t in THEMES.items():
        p = os.path.join(out, f"hero-{name}.svg")
        with open(p, "w", encoding="utf-8") as f:
            f.write(build(t))
        print(f"wrote {os.path.basename(p)}  ({os.path.getsize(p)} bytes)")
