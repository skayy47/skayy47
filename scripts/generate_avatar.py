#!/usr/bin/env python3
"""
Pixel art avatar generator — skayy47 GitHub profile.
Mario-RPG-style bust portrait, 400x400px.
Extracted accent color:  Steel Blue  #5096E6  (eyes) → replaces pink in README/GIF.

Run from repo root:  python scripts/generate_avatar.py
"""

import os, math
from PIL import Image, ImageDraw

PS   = 5        # logical → real pixel scale
LW   = LH = 80  # 80x80 logical = 400x400 real
FRAMES = 18     # subtle eye-glow animation
MS   = 100
OUT  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "avatar.gif")

# ── Palette ────────────────────────────────────────────────────────────────────
BG1    = (6,   8,  16)    # outer bg
BG2    = (12,  20,  44)   # inner glow bg
HAIR   = (20,  15,  34)   # dark hair
HAIR_H = (36,  28,  58)   # hair highlight
SKIN   = (200, 163, 118)  # face skin
SKIN_D = (158, 120,  78)  # skin shadow
HOODIE = (24,  19,  44)   # dark hoodie
HOOD_H = (34,  27,  56)   # hoodie highlight
HOOD_P = (18,  14,  32)   # hoodie pocket border
EYE_C  = (80,  150, 230)  # ★ STEEL BLUE — extracted accent replacing pink
EYE_L  = (160, 210, 255)  # eye shine
EYE_P  = (8,    8,  20)   # pupil
BROW   = (18,  13,  30)   # eyebrows
LIP    = (155,  90,  65)  # mouth
LIP_D  = (120,  65,  45)  # mouth dark
AMB    = (245, 158,  11)  # amber screen glow (kept)
AMB_L  = (255, 200,  70)  # amber light
EAR    = (175, 135,  90)  # ear shadow

# ── Helpers ────────────────────────────────────────────────────────────────────
def px(d, x, y, c):
    if 0 <= x < LW and 0 <= y < LH:
        d.rectangle([x*PS, y*PS, (x+1)*PS-1, (y+1)*PS-1], fill=c)

def rect(d, x, y, w, h, c):
    for dy in range(h): [px(d, x+dx, y+dy, c) for dx in range(w)]

def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def dim(c, f):
    return tuple(max(0, int(v*f)) for v in c)

def ell(x, y, cx, cy, rx, ry):
    return ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1.0

def sn(f, lo=0.0, hi=1.0, per=1.0):
    v = 0.5 + 0.5*math.sin(2*math.pi*f/per)
    return lo + (hi-lo)*v

# ── Scene layers ───────────────────────────────────────────────────────────────
def draw_bg(d):
    for y in range(LH):
        for x in range(LW):
            dist = math.sqrt((x-40)**2 + (y-38)**2)
            t = max(0.0, 1.0 - dist/44.0)
            c = lerp(BG1, BG2, t*0.9)
            px(d, x, y, c)

def draw_screen_glow(d):
    # Warm amber glow rising from bottom (open laptop/screens below)
    for y in range(60, LH):
        for x in range(8, 72):
            edge = abs(x-40)/32.0
            t = ((y-60)/20.0) * max(0, 1.0-edge*1.2)
            if t > 0.01:
                c = lerp(BG2, AMB, t*0.45)
                px(d, x, y, c)
    # Subtle amber reflection on chin area
    for y in range(48, 54):
        for x in range(32, 48):
            t = max(0, (y-48)/6.0) * max(0, 1.0-abs(x-40)/8.0) * 0.18
            if t > 0:
                s = lerp(SKIN, AMB_L, t)
                px(d, x, y, s)

def draw_hair(d):
    for y in range(LH):
        for x in range(LW):
            if ell(x, y, 40, 26, 19, 13):
                hy = (26-y)/13.0
                hx = abs(x-40)/19.0
                # highlight at crown
                t = max(0, hy) * max(0, 1.0-hx*1.4)
                c = lerp(HAIR, HAIR_H, t*0.55)
                px(d, x, y, c)
    # A few stray pixel-art hair strands at top
    for x, y in [(36,12),(39,11),(43,11),(46,12),(40,10),(37,13),(43,13)]:
        px(d, x, y, HAIR)
    for x, y in [(38,11),(42,11),(40,9)]:
        px(d, x, y, dim(HAIR,0.6))

def draw_face(d):
    for y in range(LH):
        for x in range(LW):
            if ell(x, y, 40, 37, 15, 14) and not ell(x, y, 40, 26, 19, 13):
                dx_n = (x-40)/15.0
                shadow = dx_n*dx_n * 0.4
                c = lerp(SKIN, SKIN_D, shadow)
                px(d, x, y, c)
    # Ears
    for y in range(34, 43):
        for x in range(24, 28):
            if not ell(x, y, 40, 37, 15, 14):
                px(d, x, y, EAR)
        for x in range(53, 57):
            if not ell(x, y, 40, 37, 15, 14):
                px(d, x, y, EAR)
    # Neck
    rect(d, 36, 50, 8, 5, SKIN_D)
    rect(d, 37, 50, 6, 4, lerp(SKIN, SKIN_D, 0.5))

def draw_eyebrows(d):
    # Slightly arched — pixel art style
    for x in range(30, 37):
        t = (x-30)/6.0
        by = 30 if t < 0.5 else 31
        px(d, x, by,   BROW)
        px(d, x, by+1, dim(BROW, 0.4))
    for x in range(43, 50):
        t = (x-43)/6.0
        by = 30 if t > 0.5 else 31
        px(d, x, by,   BROW)
        px(d, x, by+1, dim(BROW, 0.4))

def draw_eyes(d, f=0):
    # Animated: subtle glow pulse on iris
    glow_t = sn(f, lo=0.0, hi=0.45, per=FRAMES)
    eye_c = lerp(EYE_C, EYE_L, glow_t)

    for (cx, cy) in [(34, 36), (46, 36)]:
        for y in range(cy-3, cy+3):
            for x in range(cx-4, cx+4):
                if ell(x, y, cx, cy, 3.8, 2.6):
                    if ell(x, y, cx, cy, 1.8, 1.8):
                        px(d, x, y, EYE_P)   # pupil
                    else:
                        px(d, x, y, eye_c)   # iris
        # eyelid top shadow
        for x in range(cx-4, cx+4):
            px(d, x, cy-3, dim(BROW, 0.7))
        # eye shine (1 logical pixel)
        px(d, cx-2, cy-1, lerp(EYE_L, (255,255,255), glow_t))

def draw_nose(d):
    px(d, 38, 42, dim(SKIN_D, 0.9))
    px(d, 42, 42, dim(SKIN_D, 0.9))
    px(d, 39, 43, dim(SKIN_D, 0.75))
    px(d, 41, 43, dim(SKIN_D, 0.75))
    px(d, 40, 44, dim(SKIN_D, 0.6))

def draw_mouth(d):
    # Neutral, slight closed smile
    for x in range(35, 45):
        px(d, x, 47, LIP)
    px(d, 34, 48, dim(LIP,0.8)); px(d, 45, 48, dim(LIP,0.8))
    for x in range(35, 45):
        px(d, x, 48, LIP_D)
    # Slight upward corners
    px(d, 34, 47, dim(LIP,0.5))
    px(d, 45, 47, dim(LIP,0.5))

def draw_body(d):
    # Hoodie — trapezoid, wider at bottom
    for y in range(54, LH):
        spread = int((y-54)*0.45)
        lx = max(0,  16-spread)
        rx = min(LW-1, 64+spread)
        for x in range(lx, rx+1):
            hx = abs(x-40)/(rx-lx+1)*2.0
            hy = (y-54)/26.0
            c = lerp(HOOD_H, HOODIE, hx*0.5 + hy*0.5)
            # Amber glow from screen below
            ag = max(0, (y-66)/14.0)*max(0, 1.0-abs(x-40)/24.0)*0.35
            c = lerp(c, AMB, ag)
            px(d, x, y, c)
    # Hoodie center zipper line
    for y in range(56, 68):
        px(d, 40, y, dim(HOOD_P, 1.2))
    # Hood seam V
    for i in range(5):
        px(d, 40-i-1, 54+i, HOOD_P)
        px(d, 40+i+1, 54+i, HOOD_P)
    # Hoodie pocket
    for y in range(68, 76):
        for x in range(32, 49):
            if y in (68, 75) or x in (32, 48):
                px(d, x, y, dim(HOOD_H, 0.8))

# ── Frame renderer ─────────────────────────────────────────────────────────────
def render(f=0):
    img  = Image.new("RGB", (LW*PS, LH*PS), BG1)
    draw = ImageDraw.Draw(img)
    draw_bg(draw)
    draw_screen_glow(draw)
    draw_hair(draw)
    draw_face(draw)
    draw_eyebrows(draw)
    draw_nose(draw)
    draw_mouth(draw)
    draw_body(draw)
    draw_eyes(draw, f)   # animated
    return img

# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
    print(f"Rendering {FRAMES} frames (400x400px pixel art portrait)...")
    frames = [render(f) for f in range(FRAMES)]
    frames[0].save(OUT, save_all=True, append_images=frames[1:],
                   loop=0, duration=MS, optimize=False)
    kb = os.path.getsize(OUT)//1024
    print(f"Done -> {OUT}  ({kb} KB)")
