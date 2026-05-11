#!/usr/bin/env python3
"""
"SKAY's Lab" — pixel art room scene for skayy47 GitHub profile.
Style: developer room interior (inspired by gamer-room pixel art aesthetic).
Unique: AI-themed — AURA monitor, nexus data, circuit floor, AI bots on shelves.
Canvas: 800x480px (200x120 logical @ PS=4), 60 frames, 80ms/frame.
"""
import os, math, random
from PIL import Image, ImageDraw

PS     = 4
LW, LH = 200, 120
FRAMES = 60
MS     = 80
OUT    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "ai-lab.gif")

# ── Palette ────────────────────────────────────────────────────────────────────
WALL   = (10,  13,  28)
WALL_L = (14,  18,  38)
WALL_D = (7,    9,  19)
FLOOR  = (8,   10,  21)
FLOOR_H= (12,  14,  28)
DESK_C = (18,  13,  36)
DESK_H = (26,  20,  50)
SHELF_C= (20,  15,  40)
SHELF_H= (30,  22,  56)
CHAIR_C= (14,  10,  28)
CHAIR_H= (22,  16,  42)
MON_F  = (13,  10,  27)
SCRN   = (4,    3,  11)
WIN_F  = (18,  26,  56)
WIN_S  = (7,   11,  30)
WIN_C  = (10,  17,  42)
AMB    = ( 26,  26,  46)
AMB_L  = ( 50,  50,  80)
AMB_D  = ( 15,  15,  30)
STEEL  = ( 91, 123, 158)
STEEL_L= (140, 170, 200)
STEEL_D= ( 50,  60, 100)
VIO    = (224, 224, 240)
GRN    = ( 28, 175,  75)
GRN_D  = ( 18, 108,  46)
RED    = (195,  40,  40)
WHT    = (238, 236, 248)
GRY    = ( 88,  80, 112)
GOLD   = (200, 162,  38)
GOLD_L = (230, 200,  70)
GOLD_D = (130, 100,  18)
HAIR   = ( 20,  15,  34)
HAIR_H = ( 36,  28,  56)
SKIN   = (200, 163, 118)
SKIN_D = (155, 118,  76)
HOOD   = ( 28,  20,  52)
HOOD_H = ( 42,  32,  70)
HOOD_D = ( 20,  14,  38)
BK_D   = ( 22,  32,  76)  # steel-blue dark (book/device)
BK_L   = ( 38,  52,  98)  # steel-blue lighter

# ── Helpers ────────────────────────────────────────────────────────────────────
def px(d, x, y, c):
    if 0 <= x < LW and 0 <= y < LH:
        d.rectangle([x*PS, y*PS, (x+1)*PS-1, (y+1)*PS-1], fill=c)

def rect(d, x, y, w, h, c):
    for dy in range(h):
        for dx in range(w):
            px(d, x+dx, y+dy, c)

def hl(d, x, y, w, c):  rect(d, x, y, w, 1, c)
def vl(d, x, y, h, c):  rect(d, x, y, 1, h, c)

def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def dim(c, f): return tuple(max(0, int(v*f)) for v in c)
def sn(v, lo=0.0, hi=1.0): return lo + (hi-lo)*(0.5+0.5*math.sin(v))
def ell(x, y, cx, cy, rx, ry): return ((x-cx)/rx)**2+((y-cy)/ry)**2 <= 1.0

# ── Sprite engine ──────────────────────────────────────────────────────────────
def put(d, sprite, x, y, pal):
    for ry, row in enumerate(sprite):
        for rx, ch in enumerate(row):
            c = pal.get(ch)
            if c:
                px(d, x+rx, y+ry, c)

P = {
    '.': None,
    'A': AMB,    'L': AMB_L,   'a': AMB_D,
    'S': STEEL,  'l': STEEL_L, 's': STEEL_D,
    'V': VIO,    'G': GRN,     'g': GRN_D,
    'R': RED,    'W': WHT,     'y': GRY,
    'T': GOLD,   't': GOLD_L,  'u': GOLD_D,
    'H': HAIR,   'h': HAIR_H,  'K': SKIN,   'k': SKIN_D,
    'O': HOOD,   'o': HOOD_H,  'q': HOOD_D,
    'D': SHELF_C,'d': SHELF_H, 'M': MON_F,  'E': SCRN,
    'B': BK_D,   'b': BK_L,   'C': CHAIR_C,'c': CHAIR_H,
    'N': (18,40,88), 'n': (28,58,115),
    'Z': dim(WHT,0.28),
}

# ── Sprites ─────────────────────────────────────────────────────────────────────

# Large AURA diamond on left wall (21x19) — replaces big X
AURA_DIAMOND = [
    "..........L..........",
    ".........LAL.........",
    "........LAAAL........",
    ".......LAAAALLL......",
    "......LAAAAALLL......",
    ".....LAAAAAALLL......",
    "....LAAAAAAALLL......",
    "...LAAAAAAAALLL......",
    "..LAAAAAAAAALLL......",
    ".LAAAAAAAAAALLL......",
    "..LAAAAAAAAALLL......",
    "...LAAAAAAAALLL......",
    "....LAAAAAAALLL......",
    ".....LAAAAAALLL......",
    "......LAAAAALLL......",
    ".......LAAALLL.......",
    "........LAALL........",
    ".........LLL.........",
    "..........L..........",
]

# Neural brain (8x6)
BRAIN = [
    ".SSSSSS.",
    "SS....SS",
    "S.SlSl.S",
    "S.SlSl.S",
    "SS....SS",
    ".SSSSSS.",
]

# Small robot (6x9)
ROBOT = [
    ".SSSS.",
    "SALASS",
    "S.SS.S",
    ".SSSS.",
    ".AAAA.",
    ".BBBB.",
    ".B..B.",
    ".B..B.",
    ".uu.uu",
]

# Isometric data cube (9x7)
CUBE = [
    "....l....",
    "...lSl...",
    "..lSSl...",
    ".lSSSsSS.",
    "lSSSSsss.",
    ".SSSssss.",
    "..SSsss..",
]

# GPU / device (10x5)
GPU = [
    "BBBBBBBBBB",
    "BbbbbbbbbB",
    "B.b.bb.bsB",
    "BbbbbbbbbB",
    "BBBBBBBBBB",
]

# Laptop closed (10x6)
LAPTOP = [
    ".SSSSSSSS.",
    "SllllllllS",
    "SlSSSSSSls",
    "Sl......ls",
    ".ssssssss.",
    "SSSSssSSss",
]

# Trophy (7x9)
TROPHY = [
    ".TTTTT.",
    "TtLLLtT",
    "TtLLLtT",
    ".TTTTT.",
    "..TTT..",
    "...T...",
    "..uuu..",
    ".uuuuu.",
    ".uuuuu.",
]

# Potted plant (7x8)
PLANT = [
    "..GGG..",
    ".GGGGG.",
    "GGGgGGG",
    ".GgGgG.",
    "..yGy..",
    "..yyy..",
    "..yyy..",
    "..yyy..",
]

# Mini wall portrait frame (8x7)
PORTRAIT = [
    "yyyyyyyy",
    "y......y",
    "y.SSAS.y",
    "y.SAAS.y",
    "y.SSAS.y",
    "y......y",
    "yyyyyyyy",
]

# NEXUS cube icon (8x7)
NEXUS_ICON = [
    "...NN...",
    "..NNNN..",
    ".NNnnNN.",
    "NNnnnnNN",
    ".NNnnNN.",
    "..NNNN..",
    "...NN...",
]

# Mug (5x6)
MUG = [
    "DDDDD",
    "D...D",
    "DA.AD",
    "D...y",
    "DDDDD",
    ".ddd.",
]

# Book stack (10x8)
BOOKS = [
    "BBBBBBBBB.",
    "bbbbbbbbb.",
    "SSSSSSSSS.",
    "sssssssss.",
    "AAAAAAAAAA",
    "aaaaaaaaa.",
    "VVVVVVVVVV",
    "vvvvvvvvv.",
]

# ── Room base ─────────────────────────────────────────────────────────────────
def draw_room(d):
    rect(d, 0,   0, LW, LH,    WALL)
    rect(d, 0,  87, LW, LH-87, FLOOR)
    hl(d,  0,  87, LW, FLOOR_H)
    hl(d,  0,   0, LW, WALL_D)         # ceiling
    vl(d,  0,   0, 87, WALL_L)         # left wall edge
    vl(d,  1,   0, 87, dim(WALL_L,0.6))
    vl(d,  LW-1,0, 87, WALL_L)         # right wall edge
    vl(d,  LW-2,0, 87, dim(WALL_L,0.6))

def draw_floor_pattern(d, f):
    # Circuit board floor
    for fy in range(88, LH, 6):
        for fx in range(LW):
            t = sn(fx*0.07+fy*0.05+f*0.04, lo=0.0, hi=0.45)
            c = lerp(FLOOR, dim(STEEL if (fx+fy)%3 else AMB, 0.35), t*0.55)
            if t > 0.22:
                px(d, fx, fy, c)
    # Nodes
    for nx in range(8, LW, 20):
        for ny in range(90, LH, 12):
            if random.Random(nx*31+ny).random() > 0.45:
                nc = AMB if (nx+ny)%2==0 else STEEL
                px(d, nx, ny, lerp(FLOOR, nc, sn(f*0.12+nx*0.06+ny*0.08, lo=0.3, hi=0.9)*0.65))

# ── Circular window ────────────────────────────────────────────────────────────
WCX, WCY, WR = 165, 44, 30

def draw_window(d, f):
    for y in range(max(0,WCY-WR-2), min(LH,WCY+WR+2)):
        for x in range(max(0,WCX-WR-2), min(LW,WCX+WR+2)):
            dist = math.sqrt((x-WCX)**2+(y-WCY)**2)
            if dist <= WR:
                if dist > WR-2:
                    px(d, x, y, WIN_F)    # window frame
                else:
                    # Night sky gradient inside
                    t = (y-WCY+WR)/(2*WR)
                    c = lerp(WIN_S, WIN_C, t*0.8)
                    px(d, x, y, c)
    # Stars in window
    wstars = [(WCX-20+i*9, WCY-18+i%4*4) for i in range(7)]
    for sx, sy in wstars:
        if math.sqrt((sx-WCX)**2+(sy-WCY)**2) < WR-3:
            br = sn(f*0.10+(sx+sy)*0.25, lo=0.15, hi=1.0)
            px(d, sx, sy, lerp(dim(WHT,0.1), WHT, br))
    # City silhouette at bottom of window
    for bx in range(WCX-26, WCX+27):
        dist = math.sqrt((bx-WCX)**2+(WCY+15-WCY)**2)
        if dist < WR-2:
            bh = 3 + random.Random(bx*97+13).randint(0, 5)
            for bby in range(WCY+15-bh, WCY+15):
                if math.sqrt((bx-WCX)**2+(bby-WCY)**2) < WR-1:
                    px(d, bx, bby, lerp(WIN_C, dim(STEEL_D,0.6), 0.5))
    # City lights
    for lx in range(WCX-24, WCX+25, 5):
        ly = WCY + 12
        if math.sqrt((lx-WCX)**2+(ly-WCY)**2) < WR-3:
            br = sn(f*0.18+lx*0.28, lo=0.0, hi=0.9)
            lc = AMB if lx%10 < 5 else STEEL
            px(d, lx, ly, lerp(dim(lc,0.05), lc, br*0.55))

# ── AURA diamond (left wall) ──────────────────────────────────────────────────
def draw_aura_wall(d, f):
    pulse = sn(f*0.07, lo=0.65, hi=1.0)
    P['L'] = lerp(AMB_D, AMB_L, pulse)
    P['A'] = lerp(dim(AMB,0.5), AMB, pulse)
    put(d, AURA_DIAMOND, 2, 3, P)
    # Reset for other uses
    P['L'] = AMB_L; P['A'] = AMB

# ── "NEXUS" sign on wall (like "KART SPEC" in Daniel's scene) ─────────────────
def draw_nexus_sign(d, f):
    # Small sign plaque
    rect(d, 25, 57, 22, 14, (14,10,28))
    hl(d,  25, 57, 22, (20,14,38))
    # NEXUS text (pixel art, 3px per char, 5 chars)
    label_c = lerp(dim(STEEL,0.4), STEEL, sn(f*0.09, lo=0.5, hi=1.0))
    for i,ch in enumerate("NEXUS"):
        px(d, 27+i*4, 59, label_c)
        px(d, 27+i*4, 60, label_c)
        px(d, 28+i*4, 61, dim(label_c,0.7))
    # Amber dot indicator
    px(d, 43, 59, lerp(dim(AMB,0.4), AMB, sn(f*0.14, lo=0.3, hi=1.0)))

# ── Left shelf (upper) ────────────────────────────────────────────────────────
def draw_left_shelf(d):
    # Brackets
    rect(d, 3,  26, 2, 12, SHELF_C); rect(d, 78, 26, 2, 12, SHELF_C)
    # Board
    rect(d, 3,  36, 78, 4, SHELF_H); hl(d, 3, 36, 78, dim(WHT,0.11))
    # Shadow under shelf
    hl(d, 3, 40, 78, dim(SHELF_C,0.5))
    # Items on shelf
    put(d, BRAIN,      5,  29, P)   # neural brain
    put(d, ROBOT,     16,  27, P)   # mini robot
    put(d, CUBE,      26,  29, P)   # data cube
    put(d, BOOKS,     37,  28, P)   # book stack
    put(d, NEXUS_ICON,50,  28, P)   # nexus icon
    put(d, PLANT,     62,  28, P)   # plant
    put(d, TROPHY,    72,  27, P)   # trophy

# ── Right shelf ───────────────────────────────────────────────────────────────
def draw_right_shelf(d):
    rect(d, 124, 30, 2, 15, SHELF_C); rect(d, 197, 30, 2, 15, SHELF_C)
    rect(d, 124, 43, 75, 4, SHELF_H); hl(d, 124, 43, 75, dim(WHT,0.10))
    hl(d, 124, 47, 75, dim(SHELF_C,0.45))
    # Items
    put(d, PORTRAIT,  126, 33, P)
    put(d, GPU,       138, 38, P)
    put(d, MUG,       152, 37, P)
    put(d, LAPTOP,    160, 37, P)
    put(d, CUBE,      174, 36, P)

# ── Secondary monitor (left) ─────────────────────────────────────────────────
def draw_left_monitor(d, f):
    rect(d, 46, 48, 32, 38, MON_F)
    hl(d,  46, 48, 32, dim(WHT,0.10))
    rect(d, 48, 50, 28, 34, SCRN)
    # Title bar
    rect(d, 48, 50, 28, 2, (9,6,20))
    px(d, 49,51,(180,48,48)); px(d,51,51,(180,150,32)); px(d,53,51,(38,160,58))
    # Terminal content
    scroll = f // 5
    lines = [0.88,0.55,0.80,0.42,0.72,0.95,0.50,0.68,0.84,0.38]
    for li in range(8):
        lw = max(1, int(lines[(scroll+li)%len(lines)] * 22))
        ly = 53+li*4
        px(d, 48, ly, AMB_D)
        bc = lerp(dim(GRN,0.35), GRN, sn(f*0.11+li*0.55)) if li%3!=0 else \
             lerp(dim(AMB,0.35), AMB, sn(f*0.09+li*0.7))
        hl(d, 50, ly, lw, bc)
    if (f//4)%2==0:
        px(d, 48, 53+7*4, GRN)
    # Stand + base
    rect(d, 59, 86, 5, 4, SHELF_C); hl(d, 54, 90, 15, SHELF_C)

# ── Main monitor (AURA interface) ─────────────────────────────────────────────
def draw_main_monitor(d, f):
    rect(d, 73, 22, 72, 64, MON_F)
    hl(d,  73, 22, 72, dim(WHT,0.12))
    rect(d, 75, 24, 68, 60, SCRN)
    # Title bar
    rect(d, 75, 24, 68, 3, (9,6,20))
    px(d,76,25,(180,48,48)); px(d,78,25,(180,150,32)); px(d,80,25,(38,160,58))
    for i,ch in enumerate("AURA  AI ENGINE"):
        xc = 84+i*3
        if xc < 140:
            tc = AMB if i < 4 else dim(GRY,0.7)
            px(d, xc, 25, lerp(dim(tc,0.4), tc, sn(f*0.06+i*0.3)))
    # Left icon panel
    rect(d, 75, 28, 9, 54, (7,5,15))
    for si in range(4):
        rect(d, 76, 29+si*13, 7, 11, (12,8,24))
        ic = [AMB, STEEL, VIO, GRN][si]
        px(d, 79, 34+si*13, lerp(dim(ic,0.3), ic, sn(f*0.09+si*1.2)))
    # Chart area
    cx, cy, cw, ch = 85, 28, 57, 54
    rect(d, cx, cy, cw, ch, (5,3,13))
    # Grid lines
    for gy in range(0, ch, ch//4): hl(d, cx, cy+gy, cw, dim(GRY,0.22))
    # Animated bar chart (dataset)
    nb = cw//3
    for bi in range(nb):
        t_c = bi/nb
        bh = max(1, int((0.18 + 0.72*abs(math.sin(f*0.13+bi*0.48))) * ch))
        bc = lerp(STEEL, AMB, t_c)
        bc = lerp(dim(bc,0.3), bc, sn(f*0.11+bi*0.35))
        bx = cx + bi*3
        rect(d, bx, cy+ch-bh, 2, bh, dim(bc,0.5))
        px(d, bx, cy+ch-bh, bc)  # bright cap
    # Stats bar at bottom
    sb_y = cy+ch-5
    rect(d, cx, sb_y, cw, 5, (8,5,18))
    prog = sn(f*0.09, lo=0.1, hi=0.95)
    for bxi in range(int(prog*cw)):
        px(d, cx+bxi, sb_y+2, lerp(AMB, STEEL, bxi/cw))
    # Stand + base
    rect(d, 105, 86, 8, 4, SHELF_C); hl(d, 98, 90, 22, SHELF_C)

# ── Character (from behind, seated) ──────────────────────────────────────────
def draw_character(d, f):
    bob = 1 if (f//14)%2 == 0 else 0
    cx, cy = 109, 62
    # Back of head (hair)
    rect(d, cx-6, cy-8+bob, 12, 9, HAIR)
    hl(d,  cx-6, cy-8+bob, 12, HAIR_H)
    px(d,  cx-6, cy-3+bob, dim(SKIN,0.7))   # ear hint L
    px(d,  cx+5, cy-3+bob, dim(SKIN,0.7))   # ear hint R
    # Hoodie shoulders (wide)
    rect(d, cx-14, cy,     28, 8,  HOOD)
    hl(d,  cx-14, cy,     28,     HOOD_H)
    rect(d, cx-16, cy+4,  32, 9,  HOOD_D)
    rect(d, cx-12, cy+1,  24, 5,  HOOD)     # mid area (body)
    # Small AURA logo on back of hoodie
    px(d, cx,    cy+3, dim(AMB,0.55))
    px(d, cx-1,  cy+4, dim(AMB,0.45)); px(d, cx+1, cy+4, dim(AMB,0.45))
    px(d, cx,    cy+5, dim(AMB,0.35))
    # Arms extending to keyboard
    rect(d, cx-20, cy+8, 7, 5, HOOD_D)   # left arm
    rect(d, cx+13, cy+8, 7, 5, HOOD_D)   # right arm
    # Chair back visible behind
    rect(d, cx-19, cy+13, 38, 4, CHAIR_H)
    rect(d, cx-19, cy+17, 38, 10, CHAIR_C)

# ── Desk ──────────────────────────────────────────────────────────────────────
def draw_desk(d, f=0):
    hl(d,  38, 83, 132, DESK_H)
    rect(d, 38, 84, 132, 5, DESK_C)
    rect(d, 38, 89, 132, 2, dim(DESK_C,0.55))
    # Legs
    rect(d, 40,  91, 5, LH-91, DESK_C)
    rect(d, 163, 91, 5, LH-91, DESK_C)
    # RGB underglow strip on desk edge
    for rx in range(38, 170, 2):
        t = (rx/132.0 + f*0.025) % 1.0
        rc = lerp(AMB, STEEL, t) if t < 0.5 else lerp(STEEL, VIO, (t-0.5)*2)
        px(d, rx, 83, dim(rc, 0.32))

# ── Desk items ─────────────────────────────────────────────────────────────────
def draw_desk_items(d, f):
    # Mug (right of monitor, on desk)
    rect(d, 148, 77, 6, 7, (52,40,72)); hl(d, 148, 77, 6, (68,52,88))
    vl(d, 154, 78, 5, (52,40,72))  # handle
    px(d, 148, 77, dim(AMB,0.45))  # coffee top
    # Steam
    sf = f % 15
    if sf < 10:
        sy2 = 74 - sf//3
        px(d, 150, sy2,   dim(WHT,0.18)); px(d, 151, sy2-1, dim(WHT,0.12))
    # Keyboard (visible either side of character)
    rect(d, 75,  83, 22, 2, (24,18,44)); hl(d, 75,  83, 22, dim(WHT,0.10))
    rect(d, 123, 83, 22, 2, (24,18,44)); hl(d, 123, 83, 22, dim(WHT,0.10))
    # Small items left side of desk
    put(d, MUG, 40, 76, P)    # second mug left
    # Sticky note on monitor side
    rect(d, 70, 65, 5, 6, dim(AMB,0.55)); hl(d, 70, 65, 5, dim(AMB_L,0.4))

# ── Floor items ───────────────────────────────────────────────────────────────
def draw_floor_items(d, f):
    # Server rack left
    rect(d, 2,  88, 32, LH-88, (12,9,24))
    hl(d,  2,  88, 32, (18,14,36))
    for ry in range(90, LH, 4):
        hl(d, 3, ry, 30, (15,11,28))
        pa = sn(f*0.18+ry*0.9, lo=0.3, hi=1.0)
        ps = sn(f*0.14+ry*1.1, lo=0.2, hi=0.8)
        px(d, 3,  ry, lerp(dim(AMB,0.2), AMB, pa*0.7))
        px(d, 4,  ry, lerp(dim(STEEL,0.2), STEEL, ps*0.6))
        px(d, 30, ry, lerp(dim(AMB,0.15), AMB, sn(f*0.22+ry*0.7, lo=0.0, hi=0.5)))
    # Computer tower right
    rect(d, 170, 90, 28, LH-90, (12,9,24))
    hl(d,  170, 90, 28, (18,14,36))
    px(d, 172, 93, dim(AMB,0.85)); px(d, 172, 97, dim(STEEL,0.75))
    px(d, 172, 101, dim(GRN,0.7))
    for dy in range(0, LH-92, 4):
        px(d, 196, 92+dy, lerp(dim(STEEL,0.1), STEEL, sn(f*0.15+dy*0.4, lo=0.15, hi=0.55)))
    # Box / crate on floor center
    rect(d, 42, 92, 20, LH-92, (16,12,32))
    hl(d,  42, 92, 20, (22,16,42))
    rect(d, 44, 94, 16, 5, (20,15,38))  # top inset

# ── Floating particles / data bits ───────────────────────────────────────────
_PDATA = [(random.Random(i*37).uniform(0,LW), random.Random(i*53).uniform(2,50),
           random.Random(i*71).uniform(-0.3,0.3), random.Random(i*89).uniform(-0.15,0.08),
           random.Random(i*97).uniform(0,6.28),
           AMB if i%3==0 else (STEEL if i%3==1 else VIO))
          for i in range(18)]

def draw_particles(d, f):
    for (x0,y0,vx,vy,ph,col) in _PDATA:
        x = int((x0+vx*f+1.5*math.sin(f*0.05+ph)) % LW)
        y = int((y0+vy*f+0.8*math.cos(f*0.04+ph)) % 50)
        br = sn(f*0.12+ph, lo=0.2, hi=1.0)
        c  = lerp(dim(col,0.1), col, br)
        px(d, x, y, c)

# ── Screen glow ───────────────────────────────────────────────────────────────
def draw_glow(d, f):
    pulse = sn(f*0.09, lo=0.8, hi=1.0)
    # Main monitor casts mixed amber/steel glow on desk + ceiling
    for gy in range(84, 92):
        for gx in range(70, 150):
            dy = gy-84; dx = abs(gx-109)/42.0
            t = max(0, (1-dy/8.0)*(1-dx))*0.3*pulse
            if t > 0:
                px(d, gx, gy, lerp(FLOOR, lerp(AMB,STEEL,0.35), t))
    for gy in range(0, 4):
        for gx in range(73, 145):
            t = (1-abs(gx-109)/38.0)*(4-gy)/4.0*0.18*pulse
            if t > 0:
                px(d, gx, gy, lerp(WALL_D, lerp(AMB,STEEL,0.3), t))

# ── Render ─────────────────────────────────────────────────────────────────────
def render(f):
    img  = Image.new("RGB", (LW*PS, LH*PS), WALL)
    draw = ImageDraw.Draw(img)
    draw_room(draw)
    draw_window(draw, f)
    draw_aura_wall(draw, f)
    draw_nexus_sign(draw, f)
    draw_left_shelf(draw)
    draw_right_shelf(draw)
    draw_particles(draw, f)
    draw_left_monitor(draw, f)
    draw_main_monitor(draw, f)
    draw_desk(draw, f)
    draw_character(draw, f)
    draw_desk_items(draw, f)
    draw_floor_items(draw, f)
    draw_floor_pattern(draw, f)
    draw_glow(draw, f)
    return img

# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    print(f"Rendering {FRAMES} frames at {LW*PS}x{LH*PS}px (SKAY's Lab room scene)...")
    frames = []
    for fi in range(FRAMES):
        frames.append(render(fi))
        if fi % 15 == 0: print(f"  {fi}/{FRAMES}")
    print(f"Saving -> {OUT}")
    frames[0].save(OUT, save_all=True, append_images=frames[1:],
                   loop=0, duration=MS, optimize=False)
    print(f"Done -> {os.path.getsize(OUT)//1024} KB")
