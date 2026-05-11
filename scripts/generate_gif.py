#!/usr/bin/env python3
"""
"The AI Engineer's World" — Mario-style side-scrolling pixel art scene.
Unique & creative: data-tower city, circuit-board ground, walking SKAY + AI bots.
Canvas: 800x320px (200x80 logical @ PS=4), 72 frames, 80ms/frame.

Run:  python scripts/generate_gif.py
"""

import os, math, random
from PIL import Image, ImageDraw

PS     = 4
LW, LH = 200, 80
FRAMES = 72
MS     = 80
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ai-lab.gif")

# ── Palette ────────────────────────────────────────────────────────────────────
SKY1   = (5,  5, 14)    # sky top
SKY2   = (9,  8, 22)    # sky bottom
STAR   = (238, 235, 248)

TWR1   = (9,   7,  21)  # tallest towers (back)
TWR2   = (13, 10,  28)  # mid towers
TWR3   = (17, 13,  36)  # front towers
WIN_A  = (245, 158, 11) # amber window
WIN_S  = ( 80, 150, 230)# steel window
WIN_D  = ( 30,  22,  48)# dark/off window

GND    = (11,  9,  22)  # ground base
GND_H  = (15, 12,  30)  # ground highlight
TR_A   = (245, 158, 11) # amber trace
TR_S   = ( 80, 150, 230)# steel trace
TR_D   = (150,  92,   6)# dim amber

PLAT_D = (20, 15, 38)   # platform dark
PLAT_L = (28, 22, 50)   # platform light
PLAT_T = (38, 30, 62)   # platform top

AMB    = (245, 158,  11)
AMB_L  = (255, 210,  70)
STEEL  = ( 80, 150, 230)
STEEL_L= (160, 210, 255)
VIO    = (100,  40, 210)
WHT    = (240, 238, 250)

HAIR   = ( 20,  15,  34)
HAIR_H = ( 38,  30,  60)
SKIN   = (200, 163, 118)
SKIN_D = (155, 118,  76)
HOOD   = ( 24,  19,  44)
HOOD_H = ( 36,  28,  58)
PANTS  = ( 28,  22,  48)
SHOE   = ( 18,  13,  30)
SHOE_L = ( 30,  24,  50)

BOT_B  = ( 22,  35,  60)
BOT_H  = ( 38,  58,  95)
BOT_E  = ( 80, 150, 230)
BOT_A  = (245, 158,  11)

# ── Helpers ────────────────────────────────────────────────────────────────────
def px(d, x, y, c):
    if 0 <= x < LW and 0 <= y < LH:
        d.rectangle([x*PS, y*PS, (x+1)*PS-1, (y+1)*PS-1], fill=c)

def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w):
            px(d, x+dx, y+dy, c)

def hl(d, x, y, w, c): rect(d, x, y, w, 1, c)
def vl(d, x, y, h, c): rect(d, x, y, 1, h, c)

def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def dim(c, f): return tuple(max(0, int(v*f)) for v in c)
def sn(v, lo=0.0, hi=1.0): return lo + (hi-lo)*(0.5+0.5*math.sin(v))

# ── Sky ────────────────────────────────────────────────────────────────────────
_STARS = [(random.Random(i).randint(0,LW-1), random.Random(i+200).randint(0,38))
          for i in range(55)]

def draw_sky(d, f):
    for y in range(60):
        c = lerp(SKY1, SKY2, y/60)
        hl(d, 0, y, LW, c)
    for i,(sx,sy) in enumerate(_STARS):
        br = sn(f*0.08 + i*0.4, lo=0.15, hi=1.0)
        c  = lerp(dim(STAR,0.15), STAR, br)
        px(d, sx, sy, c)

# ── Background city towers ─────────────────────────────────────────────────────
_TOWERS = [
    # (x, y_top, width, height, layer, windows)
    (  2, 4,  14, 55, 0, [(3,10),(3,16),(3,22),(3,28),(8,10),(8,16),(8,22),(8,28)]),
    ( 20, 9,  10, 50, 0, [(1,12),(1,18),(1,24),(5,12),(5,18),(5,24)]),
    ( 34, 6,  18, 53, 1, [(2,10),(2,16),(2,22),(2,28),(8,10),(8,16),(8,22),(8,28),(14,10),(14,16)]),
    ( 56, 12, 10, 47, 1, [(1,14),(1,20),(1,26),(5,14),(5,20),(5,26)]),
    ( 70, 4,  22, 55, 2, [(2,8),(2,14),(2,20),(2,26),(8,8),(8,14),(8,20),(8,26),(14,8),(14,14),(14,20),(17,8),(17,14)]),
    ( 98, 8,  16, 51, 1, [(2,12),(2,18),(2,24),(7,12),(7,18),(7,24),(12,12),(12,18)]),
    (118, 5,  12, 54, 2, [(1,10),(1,16),(1,22),(1,28),(6,10),(6,16),(6,22),(6,28)]),
    (134, 10, 14, 49, 1, [(2,14),(2,20),(2,26),(7,14),(7,20),(7,26)]),
    (152, 3,  20, 56, 0, [(2,8),(2,14),(2,20),(2,26),(8,8),(8,14),(8,20),(8,26),(14,8),(14,14),(14,20)]),
    (176, 7,  10, 52, 1, [(1,12),(1,18),(1,24),(1,30),(5,12),(5,18),(5,24)]),
    (190, 4,  12, 55, 0, [(1,10),(1,16),(1,22),(1,28),(7,10),(7,16),(7,22),(7,28)]),
]

def draw_towers(d, f):
    for (tx, ty, tw, th, layer, wins) in _TOWERS:
        base = [TWR1, TWR2, TWR3][layer]
        top  = lerp(base, (25,20,46), 0.5)
        rect(d, tx, ty, tw, th, base)
        hl(d, tx, ty, tw, top)         # top edge
        vl(d, tx, ty, th, top)         # left edge
        vl(d, tx+tw-1, ty, th, dim(base,0.7))  # right shadow
        # antenna
        vl(d, tx+tw//2, ty-3, 3, dim(AMB,0.5))
        px(d, tx+tw//2, ty-3, dim(AMB,0.9))
        # windows
        for (wx,wy) in wins:
            phase = (tx+wx+wy)*0.7
            lit = sn(f*0.12 + phase, lo=0.0, hi=1.0) > 0.35
            if lit:
                wc = WIN_A if (tx+wx+wy)%3 != 0 else WIN_S
                br = sn(f*0.10 + phase, lo=0.5, hi=1.0)
                px(d, tx+wx, ty+wy, lerp(WIN_D, wc, br))
            else:
                px(d, tx+wx, ty+wy, WIN_D)
    # Server-rack landmark: a tall "data center" tower (foreground, right)
    rect(d, 186, 32, 14, 27, (14,11,28))
    hl(d,  186, 32, 14, (24,19,44))
    for ry in range(34, 57, 3):
        hl(d, 187, ry, 12, (20,15,38))
        px(d, 187, ry, dim(AMB,0.7)); px(d, 188, ry, dim(STEEL,0.6))
        px(d, 195, ry, dim(AMB,0.5 + 0.3*sn(f*0.2+ry)))

# ── Circuit board ground ───────────────────────────────────────────────────────
_TRACES_H = [61, 63, 65, 67, 70, 73]   # horizontal amber traces at these y
_TRACES_V = list(range(0, LW, 14))     # vertical steel traces at these x
_NODES    = [(x, y) for x in range(7, LW, 14) for y in [61,65,70] if random.Random(x+y).random() > 0.45]

def draw_ground(d, f):
    rect(d, 0, 60, LW, LH-60, GND)
    hl(d, 0, 60, LW, GND_H)
    # Horizontal amber traces
    for ty in _TRACES_H:
        for x in range(LW):
            pulse = sn(f*0.06 - x*0.06, lo=0.3, hi=0.9)
            tc = lerp(dim(TR_A,0.25), TR_A, pulse*0.55)
            px(d, x, ty, lerp(GND, tc, 0.7))
    # Vertical steel traces
    for vx in _TRACES_V:
        for y in range(60, LH):
            pulse = sn(f*0.07 + vx*0.05, lo=0.2, hi=0.8)
            tc = lerp(dim(TR_S,0.2), TR_S, pulse*0.4)
            px(d, vx, y, lerp(GND, tc, 0.6))
    # Circuit nodes (junctions)
    for (nx,ny) in _NODES:
        br = sn(f*0.10 + nx*0.08 + ny*0.12, lo=0.0, hi=1.0)
        nc = AMB if (nx+ny)%2==0 else STEEL
        px(d, nx, ny, lerp(GND, nc, br*0.8))
    # Ground top highlight glow from city lights
    for x in range(LW):
        t = sn(x*0.05 + f*0.04, lo=0.0, hi=0.22)
        px(d, x, 60, lerp(GND_H, lerp(AMB,STEEL,x/LW), t))

# ── Floating platforms ─────────────────────────────────────────────────────────
_PLATS = [
    (25,  44, 12),   # (x, base_y, width)
    (80,  38, 16),
    (138, 42, 14),
]

def draw_platforms(d, f):
    for (px_p, py_p, pw) in _PLATS:
        bob = round(sn(f*0.06 + px_p*0.05, lo=-1, hi=1))
        y   = py_p + bob
        # Shadow on ground
        for sx in range(px_p+1, px_p+pw-1):
            px(d, sx, 60, lerp(GND, (0,0,0), 0.25))
        # Platform body
        rect(d, px_p, y+1, pw, 3, PLAT_D)
        hl(d,  px_p, y,   pw,    PLAT_T)    # top highlight
        # Amber circuit trace on platform top
        for ix in range(0, pw, 3):
            px(d, px_p+ix, y, lerp(PLAT_T, AMB, 0.5))
        # Steel trace
        for ix in range(1, pw, 3):
            px(d, px_p+ix, y, lerp(PLAT_T, STEEL, 0.4))
        # Floating data orb above platform
        ox = px_p + pw//2
        oy = y - 4 + round(sn(f*0.10 + px_p*0.08, lo=-1, hi=1))
        oc = AMB if (px_p//10)%2==0 else STEEL
        oc = lerp(dim(oc,0.3), oc, sn(f*0.15+px_p*0.1))
        px(d, ox,   oy,   oc)
        px(d, ox-1, oy,   dim(oc,0.5))
        px(d, ox+1, oy,   dim(oc,0.5))
        px(d, ox,   oy-1, dim(oc,0.4))
        px(d, ox,   oy+1, dim(oc,0.4))

# ── SKAY character sprite (8 wide × 12 tall) ──────────────────────────────────
N = None
def _skay_pixels(walk_f):
    # walk_f 0,1,2,3 → 4-frame cycle
    # Row layout: [hair, hair, face, face, face, chin, body, body, body, legs, legs, shoes]
    rows = [
        [N,   H,    H,    H,    H,    H,    H,    N   ],  # 0 hair
        [H,   HAIR_H,SKIN, SKIN, SKIN, SKIN, HAIR_H,H ],  # 1 forehead
        [H,   SKIN, STEEL,SKIN, SKIN, STEEL,SKIN,  H  ],  # 2 eyes
        [H,   SKIN, SKIN, SKIN, SKIN, SKIN, SKIN,  N  ],  # 3 mid-face
        [N,   H,    SKIN, SKIN, SKIN, SKIN, H,     N  ],  # 4 chin
        [N,   HOOD, HOOD, HOOD, HOOD, HOOD, HOOD,  N  ],  # 5 hoodie top
        [N,   HOOD_H,HOOD,HOOD, HOOD, HOOD, HOOD_H,N  ],  # 6 body
        [N,   HOOD, HOOD, HOOD, HOOD, HOOD, HOOD,  N  ],  # 7 body lower
    ]
    H = HAIR
    # Walk cycle legs + feet
    legs = {
        0: [[N,N,PANTS,N,PANTS,N,N,N],[N,N,PANTS,N,PANTS,N,N,N],[N,N,SHOE,N,N,SHOE_L,N,N]],
        1: [[N,N,PANTS,PANTS,N,N,N,N],[N,N,PANTS,PANTS,N,N,N,N],[N,N,SHOE,SHOE_L,N,N,N,N]],
        2: [[N,N,PANTS,N,PANTS,N,N,N],[N,N,PANTS,N,PANTS,N,N,N],[N,N,SHOE_L,N,SHOE,N,N,N]],
        3: [[N,N,N,PANTS,PANTS,N,N,N],[N,N,N,PANTS,PANTS,N,N,N],[N,N,N,SHOE_L,SHOE,N,N,N]],
    }
    return rows + legs[walk_f % 4]

def draw_skay(d, x, y, walk_f):
    H = HAIR
    # 8x12 sprite
    cols8 = [
        [N,  HAIR,  HAIR,  HAIR,  HAIR,  HAIR,  HAIR,  N   ],  # 0 hair top
        [HAIR,HAIR_H,SKIN,  SKIN,  SKIN,  SKIN, HAIR_H, HAIR],  # 1 forehead
        [HAIR, SKIN,STEEL, SKIN,  SKIN, STEEL,  SKIN,  HAIR],   # 2 eyes
        [HAIR, SKIN, SKIN,  SKIN,  SKIN,  SKIN,  SKIN,  N   ],  # 3 face
        [N,   HAIR,  SKIN,  SKIN,  SKIN,  SKIN,  HAIR,  N   ],  # 4 chin
        [N,   HOOD,  HOOD,  HOOD,  HOOD,  HOOD,  HOOD,  N   ],  # 5 hoodie
        [N,  HOOD_H, HOOD,  HOOD,  HOOD,  HOOD, HOOD_H, N   ],  # 6 body
        [N,   HOOD,  HOOD,  HOOD,  HOOD,  HOOD,  HOOD,  N   ],  # 7 body
    ]
    walk_legs = {
        0: [[N,N,PANTS,N,N,PANTS,N,N],[N,N,PANTS,N,N,PANTS,N,N],[N,SHOE,SHOE,N,SHOE,SHOE_L,N,N]],
        1: [[N,N,PANTS,PANTS,N,N,N,N],[N,N,PANTS,PANTS,N,N,N,N],[N,N,SHOE,SHOE_L,N,N,N,N]],
        2: [[N,N,PANTS,N,N,PANTS,N,N],[N,N,PANTS,N,N,PANTS,N,N],[N,N,SHOE_L,SHOE,SHOE,SHOE,N,N]],
        3: [[N,N,N,N,PANTS,PANTS,N,N],[N,N,N,N,PANTS,PANTS,N,N],[N,N,N,N,SHOE_L,SHOE,SHOE,N]],
    }
    sprite = cols8 + walk_legs[walk_f % 4]
    for row_i, row in enumerate(sprite):
        for col_i, c in enumerate(row):
            if c is not None:
                px(d, x+col_i, y+row_i, c)

# ── Robot A sprite (6 wide × 9 tall) ──────────────────────────────────────────
def draw_bot_a(d, x, y, walk_f):
    wf = walk_f % 2
    sprite = [
        [N,   BOT_H, BOT_H, BOT_H, BOT_H, N   ],  # head top
        [BOT_B,BOT_H,BOT_E, BOT_E, BOT_H,BOT_B],  # eyes (steel blue)
        [BOT_B,BOT_B,BOT_B, BOT_B, BOT_B,BOT_B],  # face
        [N,   BOT_A, BOT_B, BOT_B, BOT_A, N   ],  # antenna/chin amber
        [N,   BOT_B, BOT_B, BOT_B, BOT_B, N   ],  # neck
        [BOT_H,BOT_B,BOT_B, BOT_B, BOT_B,BOT_H],  # body
        [BOT_B,BOT_B,BOT_B, BOT_B, BOT_B,BOT_B],  # body
    ]
    legs_0 = [[N,N,SHOE,N,SHOE,N],[N,N,SHOE_L,N,SHOE_L,N]]
    legs_1 = [[N,N,N,SHOE,SHOE,N],[N,N,N,SHOE_L,SHOE_L,N]]
    sprite += (legs_0 if wf==0 else legs_1)
    for ri, row in enumerate(sprite):
        for ci, c in enumerate(row):
            if c is not None:
                px(d, x+ci, y+ri, c)

# ── Robot B sprite (5 wide × 8 tall) ──────────────────────────────────────────
def draw_bot_b(d, x, y, walk_f):
    wf = walk_f % 2
    sprite = [
        [N,   BOT_A, BOT_A, BOT_A, N   ],   # head amber accent
        [BOT_B,BOT_H, BOT_E,BOT_H,BOT_B],   # eye
        [BOT_B,BOT_B, BOT_B,BOT_B,BOT_B],
        [BOT_H,BOT_B, BOT_B,BOT_B,BOT_H],
        [BOT_B,BOT_B, BOT_B,BOT_B,BOT_B],
        [BOT_B,BOT_B, BOT_B,BOT_B,BOT_B],
    ]
    legs_0 = [[N,SHOE,N,SHOE_L,N],[N,SHOE_L,N,SHOE,N]]
    legs_1 = [[N,N,SHOE,SHOE_L,N],[N,N,SHOE_L,SHOE,N]]
    sprite += (legs_0 if wf==0 else legs_1)
    for ri, row in enumerate(sprite):
        for ci, c in enumerate(row):
            if c is not None:
                px(d, x+ci, y+ri, c)

# ── Flying data packets ────────────────────────────────────────────────────────
_PKT_SEEDS = [10, 30, 55, 75, 105, 140, 165]

def draw_packets(d, f):
    for i, seed in enumerate(_PKT_SEEDS):
        rng = random.Random(seed)
        speed = rng.uniform(1.5, 3.0)
        start_x = rng.randint(0, LW-1)
        start_y = rng.randint(10, 50)
        x = int((start_x + f * speed) % LW)
        y = start_y + round(sn(f*0.08 + i*0.6, lo=-2, hi=2))
        c = AMB if i%2==0 else STEEL
        trail_c = lerp(SKY2, c, 0.4)
        # Packet body
        rect(d, x, y, 3, 2, lerp(dim(c,0.4), c, sn(f*0.2+i)))
        px(d, x+1, y, lerp(c, WHT, 0.5))  # bright center
        # Trail
        for t in range(1, 5):
            tx = (x - t) % LW
            px(d, tx, y, lerp(SKY2, trail_c, max(0, 1-t/4)))

# ── Floating neural nodes (like coin blocks) ───────────────────────────────────
_NNODES = [(40,32),(90,26),(130,34),(170,28),(60,22),(110,30)]

def draw_neural_nodes(d, f):
    for i,(nx,ny) in enumerate(_NNODES):
        bob = round(sn(f*0.08 + i*0.9, lo=-1, hi=1))
        ry = ny + bob
        c = AMB if i%3==0 else (STEEL if i%3==1 else VIO)
        br = sn(f*0.12 + i*0.7, lo=0.4, hi=1.0)
        cc = lerp(dim(c,0.2), c, br)
        # Node diamond shape
        px(d, nx,   ry-1, cc)
        px(d, nx-1, ry,   dim(cc,0.7))
        px(d, nx,   ry,   cc)
        px(d, nx+1, ry,   dim(cc,0.7))
        px(d, nx,   ry+1, dim(cc,0.5))
        # Connector lines to nearby nodes
        if i < len(_NNODES)-1:
            nx2, ny2 = _NNODES[i+1]
            steps = max(abs(nx2-nx), abs(ny2-ny))
            for s in range(0, steps, 3):
                t = s/max(steps,1)
                lx = round(nx + (nx2-nx)*t)
                ly = round(ny + (ny2-ny)*t)
                tc = lerp(dim(c,0.08), dim(c,0.18), sn(f*0.09+s*0.2))
                px(d, lx, ly, tc)

# ── Character scroll helper ────────────────────────────────────────────────────
def scroll_x(start, speed, f, width=8):
    return int((start - f * speed) % (LW + width + 10) - width)

# ── Main renderer ──────────────────────────────────────────────────────────────
def render(f):
    img  = Image.new("RGB", (LW*PS, LH*PS), SKY1)
    draw = ImageDraw.Draw(img)

    draw_sky(draw, f)
    draw_towers(draw, f)
    draw_neural_nodes(draw, f)
    draw_packets(draw, f)
    draw_platforms(draw, f)
    draw_ground(draw, f)

    # Characters — different speeds, staggered starts
    # Robot B (smallest, furthest back in terms of size → draw first)
    xb = scroll_x(160, 1.4, f, width=5)
    draw_bot_b(draw, xb, 52, f//6)

    # Robot A
    xa = scroll_x(90, 1.8, f, width=6)
    draw_bot_a(draw, xa, 51, f//5)

    # SKAY (main character, in front)
    xs = scroll_x(40, 2.2, f, width=8)
    draw_skay(draw, xs, 48, f//4)

    # Second Robot A loop (different start offset)
    xa2 = scroll_x(190, 1.6, f, width=6)
    draw_bot_a(draw, xa2, 51, (f+12)//5)

    return img

# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    print(f"Rendering {FRAMES} frames at {LW*PS}x{LH*PS}px (Mario-style scene)...")
    frames = []
    for fi in range(FRAMES):
        frames.append(render(fi))
        if fi % 18 == 0: print(f"  {fi}/{FRAMES}")
    print(f"Saving -> {OUT}")
    frames[0].save(OUT, save_all=True, append_images=frames[1:],
                   loop=0, duration=MS, optimize=False)
    print(f"Done -> {os.path.getsize(OUT)//1024} KB")
