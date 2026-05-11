#!/usr/bin/env python3
"""
AI Lab pixel art GIF generator — skayy47 GitHub profile.
Run from repo root:  python scripts/generate_gif.py
Requires:           pip install Pillow
Output:             assets/ai-lab.gif  (640×320 px, 48 frames, ~70 ms/frame)
"""

import os, math, random
from PIL import Image, ImageDraw

# ── Config ─────────────────────────────────────────────────────────────────────
PS     = 4          # logical → real pixel scale (each "pixel" = 4×4 real px)
LW, LH = 160, 80   # logical canvas dimensions
FRAMES = 48
MS     = 80         # ms per frame  (~12.5 fps)
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ai-lab.gif")

# ── Colour palette ─────────────────────────────────────────────────────────────
BG     = (7,   6,  17)   # void
WALL   = (11,  9,  23)   # back wall
FLR    = (15, 11,  29)   # floor
DSK    = (23, 17,  43)   # desk body
DSK_H  = (33, 25,  55)   # desk highlight
MON    = (17, 13,  33)   # monitor bezel
SCRN   = (4,   3,  11)   # screen bg
STD    = (21, 15,  39)   # monitor stand

AMB    = (245, 158,  11)  # amber
AMB_L  = (255, 210,  80)  # amber light
AMB_D  = (140,  85,   4)  # amber dark
PINK   = (236,  72, 153)  # pink
PINK_L = (255, 160, 200)  # pink light
PINK_D = (130,  28,  80)  # pink dark
VIO    = (108,  46, 218)  # violet
VIO_D  = ( 68,  18, 148)  # violet dark
TG     = (  0, 195,  85)  # terminal green
TG_D   = (  0, 105,  45)  # terminal green dark
CYN    = (  0, 195, 230)  # cyan
WHT    = (238, 236, 248)  # white
GRY    = ( 95,  86, 120)  # mid-grey
DGR    = ( 38,  32,  58)  # dark grey

CB     = ( 46,  36,  70)  # char body
CH     = ( 19,  14,  32)  # char hair
CS     = (188, 148, 108)  # char skin

# ── Drawing primitives ─────────────────────────────────────────────────────────
def px(d, x, y, c):
    if 0 <= x < LW and 0 <= y < LH:
        d.rectangle([x*PS, y*PS, (x+1)*PS-1, (y+1)*PS-1], fill=c)

def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w):
            px(d, x+dx, y+dy, c)

def hl(d, x, y, w, c):   rect(d, x, y, w, 1, c)
def vl(d, x, y, h, c):   rect(d, x, y, 1, h, c)

def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def dim(c, f):
    return tuple(max(0, int(v*f)) for v in c)

def sn(f, per=1.0, lo=0.0, hi=1.0):
    v = 0.5 + 0.5*math.sin(2*math.pi*f/per)
    return lo + (hi-lo)*v

# ── Scene geometry ─────────────────────────────────────────────────────────────
# Left monitor   : bezel x=4-39,   y=8-55   screen x=6-37,   y=10-53
# Centre monitor : bezel x=52-107, y=4-55   screen x=54-105, y=6-53
# Right monitor  : bezel x=115-155 y=8-55   screen x=117-153 y=10-53
# Desk surface   : y=56-62
# Floor          : y=63-79
# Character      : x=41-52, y=38-57
# Keyboard       : x=55-104, y=56-57
# Mug            : x=107-114, y=51-57

# ── Neural-net wall art ────────────────────────────────────────────────────────
_NODES = [(15,14),(26,9),(26,19),(38,6),(38,14),(38,22),(49,11),(49,19)]
_EDGES = [(0,1),(0,2),(1,3),(1,4),(2,4),(2,5),(3,6),(4,6),(4,7),(5,7)]

def draw_wall(d, f):
    rect(d, 0, 0, LW, 56, WALL)
    # edges + pulses
    for ei,(a,b) in enumerate(_EDGES):
        x1,y1 = _NODES[a]; x2,y2 = _NODES[b]
        steps = max(abs(x2-x1), abs(y2-y1)) + 1
        # static dim line
        for s in range(steps):
            t = s/max(steps-1,1)
            px(d, round(x1+(x2-x1)*t), round(y1+(y2-y1)*t), dim(VIO,0.22))
        # travelling pulse
        ppos = (f*2 + ei*5) % (steps*2)
        if ppos < steps:
            t = ppos/max(steps-1,1)
            pc = AMB if ei%2==0 else PINK
            px(d, round(x1+(x2-x1)*t), round(y1+(y2-y1)*t), pc)
            if ppos > 0:
                t2 = (ppos-1)/max(steps-1,1)
                px(d, round(x1+(x2-x1)*t2), round(y1+(y2-y1)*t2), dim(pc,0.35))
    # nodes
    for ni,(nx,ny) in enumerate(_NODES):
        glows = [AMB, PINK, VIO]
        g = glows[ni%3]
        pulse = sn(f*0.18 + ni*0.9, lo=0.35, hi=1.0)
        nc = dim(g, pulse)
        rect(d, nx-1, ny-1, 2, 2, nc)

# ── Desk & floor ───────────────────────────────────────────────────────────────
def draw_desk(d):
    hl(d, 0, 56, LW, DSK_H)
    rect(d, 0, 57, LW, 5, DSK)
    rect(d, 0, 62, LW, 2, dim(DSK, 0.65))
    rect(d, 0, 64, LW, LH-64, FLR)
    hl(d, 0, 64, LW, dim(DSK, 0.45))

# ── Monitor helper ─────────────────────────────────────────────────────────────
def draw_bezel(d, bx, by, bw, bh):
    rect(d, bx, by, bw, bh, MON)
    hl(d, bx, by, bw, dim(WHT, 0.10))
    vl(d, bx, by, bh, dim(WHT, 0.07))
    rect(d, bx+2, by+2, bw-4, bh-4, SCRN)
    # stand
    sx = bx + bw//2 - 2
    rect(d, sx, by+bh, 4, 3, STD)
    hl(d, sx-3, by+bh+3, 10, STD)
    return bx+2, by+2, bw-4, bh-4   # inner screen area

# ── Terminal (left monitor) ────────────────────────────────────────────────────
_TERM_LINES = [
    # (bar_width_fraction, colour, indent)
    (0.90, TG,          0),
    (0.60, AMB,         1),
    (0.80, dim(TG,0.7), 0),
    (0.45, dim(PINK,0.65), 2),
    (0.95, TG,          0),
    (0.55, dim(VIO,0.80), 1),
    (0.70, dim(TG,0.75), 0),
    (0.85, AMB,         1),
    (0.50, dim(TG,0.60), 2),
    (0.78, dim(TG,0.85), 0),
    (0.40, dim(AMB,0.70),1),
    (0.88, TG,          0),
]

def draw_terminal(d, sx, sy, sw, sh, f):
    # title bar
    rect(d, sx, sy, sw, 2, (10,7,22))
    px(d, sx+1, sy+1, (185,50,50));  px(d, sx+3, sy+1, (185,155,35));  px(d, sx+5, sy+1, (40,165,60))
    # prompt arrow highlight row every scroll tick
    scroll = f // 5
    rows = (sh - 3) // 4
    for li in range(min(rows, 12)):
        idx  = (scroll + li) % len(_TERM_LINES)
        frac, col, ind = _TERM_LINES[idx]
        ly   = sy + 3 + li*4
        bar_w = max(1, int(frac * (sw - 3 - ind)))
        # prompt pixel
        px(d, sx+1, ly, AMB_D)
        # bar
        hl(d, sx+2+ind, ly, bar_w, col)
    # blinking cursor
    cy = sy + 3 + (rows-1)*4
    if (f//4)%2 == 0:
        px(d, sx+1, cy, TG)

# ── Loss curve (centre monitor) ───────────────────────────────────────────────
def _loss(ep):
    return 2.45 * math.exp(-4.2 * ep) + 0.14 + 0.04*math.sin(ep*22)

def draw_training(d, sx, sy, sw, sh, f):
    # title bar
    rect(d, sx, sy, sw, 2, (10,7,22))
    px(d, sx+1, sy+1, (185,50,50));  px(d, sx+3, sy+1, (185,155,35));  px(d, sx+5, sy+1, (40,165,60))
    # "AURA · TRAINING" label
    lbl = "AURA · TRAINING"
    for i, ch in enumerate(lbl[:sw-8]):
        c = AMB if i < 4 else (GRY if ch == ' ' else dim(GRY,0.75))
        if ch not in (' ', '·'):
            px(d, sx+8+i, sy+1, c)
        elif ch == '·':
            px(d, sx+8+i, sy+1, dim(PINK,0.8))

    # plot area
    px_x, px_y = sx+2, sy+4
    pw, ph     = sw-4, sh-14
    rect(d, px_x, px_y, pw, ph, (5,4,14))
    # grid
    for gy in range(0, ph, ph//4):
        hl(d, px_x, px_y+gy, pw, dim(DGR,0.9))

    # animated progress (loops)
    prog = ((f * 1.8) % FRAMES) / FRAMES

    for xi in range(pw):
        ep = (xi / max(pw-1,1)) * prog
        loss = _loss(ep)
        yn   = 1.0 - min(1.0, max(0.0, loss/2.6))
        yi   = int(yn * (ph-1))
        if loss > 1.2:
            lc = lerp(AMB, PINK, (2.45-loss)/1.3)
        elif loss > 0.4:
            lc = lerp(PINK, TG, 1.0-(loss-0.4)/0.8)
        else:
            lc = lerp(TG, AMB_L, (0.4-loss)/0.4)
        px(d, px_x+xi, px_y+ph-1-yi, lc)
        # live-dot at frontier
        if xi == int(prog*(pw-1)):
            rect(d, px_x+xi-1, px_y+ph-2-yi, 2, 2, WHT)

    # axes
    vl(d, px_x,    px_y, ph, dim(GRY,0.35))
    hl(d, px_x, px_y+ph-1, pw, dim(GRY,0.35))

    # stats row
    sy_st = sy+sh-9
    rect(d, sx+1, sy_st, sw-2, 4, (7,5,18))
    ep_val   = int(prog*100)
    cur_loss = _loss(prog)
    stat_str = f"ep {ep_val:03d}/100  loss {cur_loss:.3f}"
    for i, ch in enumerate(stat_str[:sw-3]):
        if ch != ' ':
            sc = AMB if i < 9 else (TG if cur_loss < 0.5 else (PINK if cur_loss < 1.2 else dim(GRY,0.8)))
            px(d, sx+2+i, sy_st+1, sc)

    # progress bar
    bar_x, bar_y = sx+2, sy+sh-4
    bw = sw-4
    rect(d, bar_x, bar_y, bw, 3, (12,9,24))
    filled = int(prog*bw)
    for bxi in range(filled):
        t = bxi/max(bw-1,1)
        px(d, bar_x+bxi, bar_y,   lerp(AMB, PINK, t))
        px(d, bar_x+bxi, bar_y+1, lerp(AMB, PINK, t))
        px(d, bar_x+bxi, bar_y+2, dim(lerp(AMB,PINK,t),0.5))
    if filled > 0:
        hl(d, bar_x, bar_y, filled, lerp(WHT, AMB, 0.6))

# ── Data waveform (right monitor) ─────────────────────────────────────────────
def draw_dataflow(d, sx, sy, sw, sh, f):
    # title bar
    rect(d, sx, sy, sw, 2, (10,7,22))
    px(d, sx+1, sy+1, (185,50,50));  px(d, sx+3, sy+1, (185,155,35));  px(d, sx+5, sy+1, (40,165,60))
    lbl = "DATA·FLOW"
    for i, ch in enumerate(lbl[:sw-8]):
        c = CYN if i < 4 else (dim(GRY,0.6) if ch != '·' else dim(PINK,0.7))
        if ch not in (' ',):
            px(d, sx+8+i, sy+1, c)

    # waveform bars
    num_bars = (sw-4)//2
    ba_y = sy+4
    ba_h = sh-14
    for bi in range(num_bars):
        t   = (f + bi*2.8) / 7.0
        h_b = max(1, int((0.25 + 0.75*abs(math.sin(t + bi*0.45))) * ba_h))
        t_c = h_b / ba_h
        bc  = lerp(dim(PINK,0.5), dim(AMB,0.8), t_c)
        top = lerp(PINK_L, AMB_L, t_c)
        bxi = sx+2+bi*2
        rect(d, bxi, ba_y+ba_h-h_b, 1, h_b, bc)
        px(d,  bxi, ba_y+ba_h-h_b,     top)

    # scrolling hex strip
    hx_y = sy+sh-9
    rect(d, sx+1, hx_y, sw-2, 8, (7,5,18))
    HEX = "0123456789ABCDEF"
    for row in range(2):
        for col in range((sw-4)//2):
            ci = (f + row*11 + col*6) % 16
            if HEX[ci] != '0':
                hc = PINK if (f+row+col)%4==0 else dim(CYN,0.45)
                px(d, sx+2+col*2, hx_y+1+row*3, hc)

# ── Character ──────────────────────────────────────────────────────────────────
def draw_char(d, f):
    x, y = 41, 38
    bob  = 1 if (f//10)%2==0 else 0
    # torso
    rect(d, x, y+3+bob, 8, 9, CB)
    # head
    rect(d, x+1, y+bob,   6, 5, CS)
    # hair
    rect(d, x+1, y+bob,   6, 2, CH)
    px(d,  x,    y+1+bob,    CH)
    # face glow from screens
    fg = lerp(CS, lerp(AMB, PINK, sn(f*0.12, lo=0.0, hi=1.0)), 0.14)
    rect(d, x+2, y+1+bob, 4, 3, fg)
    # arms
    rect(d, x-1, y+6+bob, 3, 4, CB)
    rect(d, x+6, y+6+bob, 3, 4, CB)
    # hands on keyboard
    rect(d, x-1, y+10+bob, 3, 1, CS)
    rect(d, x+6, y+10+bob, 3, 1, CS)

# ── Props ──────────────────────────────────────────────────────────────────────
def draw_props(d, f):
    # keyboard
    rect(d, 55, 56, 48, 2, DGR)
    hl(d,  55, 56, 48, dim(WHT, 0.13))
    # mug body
    rect(d, 108, 52, 5, 5, (55, 42, 74))
    # mug coffee surface
    rect(d, 108, 52, 5, 1, (30, 20, 40))
    # mug handle
    vl(d, 113, 53, 3, (55,42,74))
    px(d, 113, 52, dim((55,42,74),0.7))
    # steam (3-frame cycle)
    sf = f % 18
    if sf < 12:
        sy_s = 49 - sf//4
        px(d, 109, sy_s,   dim(WHT,0.22))
        px(d, 111, sy_s-1, dim(WHT,0.16))

# ── Monitor ambient glow on desk ───────────────────────────────────────────────
def draw_glow(d, cx, color, f):
    pulse = 0.82 + 0.18*math.sin(f*0.18)
    for gy in range(56, 64):
        dist_y = gy-56
        for gx in range(max(0, cx-22), min(LW, cx+22)):
            dist = math.sqrt((gx-cx)**2 + dist_y**2)
            if dist < 22:
                a = max(0.0, (1-dist/22)*0.32*pulse)
                existing = WALL if gy < 56 else (DSK if gy < 62 else FLR)
                px(d, gx, gy, lerp(existing, color, a*0.55))

# ── Floating particles ─────────────────────────────────────────────────────────
class _Particle:
    def __init__(self, seed, col):
        r = random.Random(seed)
        self.x  = r.uniform(0, LW)
        self.y  = r.uniform(2, 54)
        self.vx = r.uniform(-0.25, 0.25)
        self.vy = r.uniform(-0.18, 0.08)
        self.ph = r.uniform(0, math.tau)
        self.sz = r.choice([1,1,1,2])
        self.col = col
    def at(self, f):
        x = (self.x + self.vx*f + 1.8*math.sin(f*0.055+self.ph)) % LW
        y = (self.y + self.vy*f + 0.9*math.cos(f*0.042+self.ph)) % 54
        return int(x), int(y)

_PARTS = (
    [_Particle(i,   AMB)  for i in range(10)] +
    [_Particle(20+i,PINK) for i in range(8)]  +
    [_Particle(40+i,VIO)  for i in range(5)]
)

def draw_particles(d, f):
    for p in _PARTS:
        x,y = p.at(f)
        br  = sn(f*0.14 + p.ph, lo=0.25, hi=1.0)
        c   = lerp(dim(p.col,0.2), p.col, br)
        if p.sz == 1:
            px(d, x, y, c)
        else:
            rect(d, x, y, 2, 2, dim(c,0.7))
            px(d, x, y, c)

# ── Frame renderer ─────────────────────────────────────────────────────────────
def render(f):
    img  = Image.new("RGB", (LW*PS, LH*PS), BG)
    draw = ImageDraw.Draw(img)

    draw_wall(draw, f)
    draw_particles(draw, f)

    # left monitor — terminal
    lsx,lsy,lsw,lsh = draw_bezel(draw, 4,  8,  36, 48)
    draw_terminal(draw, lsx, lsy, lsw, lsh, f)

    # centre monitor — training
    csx,csy,csw,csh = draw_bezel(draw, 52, 4,  56, 52)
    draw_training(draw, csx, csy, csw, csh, f)

    # right monitor — data flow
    rsx,rsy,rsw,rsh = draw_bezel(draw, 115,8,  41, 48)
    draw_dataflow(draw, rsx, rsy, rsw, rsh, f)

    draw_desk(draw)
    draw_char(draw, f)
    draw_props(draw, f)

    # desk glow from monitors
    draw_glow(draw, 22,  TG,   f)
    draw_glow(draw, 80,  AMB,  f)
    draw_glow(draw, 136, PINK, f)

    return img

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    frames = []
    print(f"Rendering {FRAMES} frames at {LW*PS}x{LH*PS}px ...")
    for fi in range(FRAMES):
        frames.append(render(fi))
        if fi % 12 == 0:
            print(f"  {fi}/{FRAMES}")
    print(f"Saving -> {OUT}")
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=MS,
        optimize=False,
    )
    kb = os.path.getsize(OUT) // 1024
    print(f"Done — {kb} KB  ({FRAMES} frames, {MS}ms/frame)")
