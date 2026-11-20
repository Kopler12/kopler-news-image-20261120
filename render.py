#!/usr/bin/env python3
"""Render the make.fun news-image-20261120 entry poster (1024x1024 PNG)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- palette ----------
PAPER   = (247, 242, 232)   # warm newsprint cream
INK     = (20, 33, 61)      # deep navy ink
INK_SOFT= (58, 68, 92)
RED     = (192, 57, 43)     # headline red
GOLD    = (201, 162, 39)
NAVY    = (20, 33, 61)
TEAL    = (23, 107, 110)
SKY     = (174, 214, 224)
WHITE   = (255, 255, 255)
CREAM   = (247, 242, 232)
GREY    = (120, 120, 116)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ---------- text helpers ----------
def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, x, y, lines, fnt, fill, max_w=None, align="left", spacing=4):
    for ln in lines:
        w = fnt.getlength(ln)
        lx = x if align == "left" else x + (max_w - w) // 2 if align == "center" else x
        draw.text((lx, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y

def panel(x, y, w, h, fill=WHITE, outline=INK, lw=2):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=lw)

# =========================================================
# MASTHEAD
# =========================================================
d.rectangle([0, 0, W, 8], fill=RED)
d.text((28, 20), "ONE DAY  ·  ONE IMAGE  ·  THE WORLD IN BRIEF",
       font=font(F_SANSB, 15), fill=INK_SOFT)
d.text((W - 28 - font(F_SANSB, 15).getlength("FRIDAY EDITION  •  No. 324"),
        20), "FRIDAY EDITION  •  No. 324", font=font(F_SANSB, 15), fill=INK_SOFT)

title_f = font(F_SERIF, 72)
title = "THE WORLD TODAY"
tw = title_f.getlength(title)
d.text(((W - tw) / 2, 44), title, font=title_f, fill=INK)

date_f = font(F_SANSB, 36)
date = "FRIDAY  ·  20 NOVEMBER 2026"
dw = date_f.getlength(date)
# red rules flanking the date
d.line([28, 138, (W - dw) / 2 - 18, 138], fill=RED, width=3)
d.line([(W + dw) / 2 + 18, 138, W - 28, 138], fill=RED, width=3)
d.text(((W - dw) / 2, 118), date, font=date_f, fill=RED)
d.line([28, 156, W - 28, 156], fill=INK, width=2)

# =========================================================
# LEAD ROW  y 168 .. 486
# =========================================================
LY, LH = 168, 318

# ---------- Lead 1: Trump / Iran (left, wide) ----------
lx, lw_ = 28, 592
panel(lx, LY, lw_, LH, fill=NAVY)
# White House silhouette (cream) on the left
hx, hy = lx + 26, LY + 96
d.rectangle([hx, hy + 40, hx + 210, hy + 118], fill=CREAM)          # main block
d.polygon([(hx + 20, hy + 40), (hx + 105, hy - 6), (hx + 190, hy + 40)], fill=CREAM)  # pediment
d.ellipse([hx + 88, hy - 34, hx + 122, hy + 2], fill=CREAM)         # dome
d.rectangle([hx + 100, hy - 52, hx + 110, hy - 32], fill=CREAM)     # dome spike
for i in range(5):                                                    # columns
    cx = hx + 18 + i * 38
    d.rectangle([cx, hy + 52, cx + 14, hy + 118], fill=NAVY)
d.rectangle([hx + 88, hy + 88, hx + 122, hy + 118], fill=NAVY)      # door
# gold "2027" on the right
f2027 = font(F_SERIF, 92)
d.text((lx + 300, LY + 52), "2027", font=f2027, fill=GOLD)
# small clock
cx0, cy0, r = lx + 520, LY + 52, 26
d.ellipse([cx0 - r, cy0 - r, cx0 + r, cy0 + r], outline=GOLD, width=4)
d.line([cx0, cy0, cx0, cy0 - 16], fill=GOLD, width=4)
d.line([cx0, cy0, cx0 + 12, cy0 + 6], fill=GOLD, width=4)
d.text((lx + 300, LY + 150), "NO RUSH", font=font(F_SANSB, 26), fill=(255, 255, 255))
d.text((lx + 26, LY + 222), "TRUMP PUTS IRAN WAR", font=font(F_SERIF, 34), fill=WHITE)
d.text((lx + 26, LY + 260), "DECISION OFF TO 2027", font=font(F_SERIF, 34), fill=WHITE)
d.text((lx + 26, LY + 300),
       "“No rush,” he says — he will “see what happens” after 1 January.",
       font=font(F_SANS, 17), fill=(214, 220, 232))

# ---------- Lead 2: GTA 6 (right) ----------
gx, gw = 636, 360
panel(gx, LY, gw, LH, fill=(26, 16, 46))
# neon sunset sky: gradient bands
sun_top = LY + 8
sun_h = 168
cols = [(43, 16, 74), (94, 28, 110), (168, 52, 120), (232, 84, 84), (255, 140, 66), (255, 183, 77)]
for i in range(sun_h):
    t = i / sun_h
    ci = min(int(t * (len(cols) - 1)), len(cols) - 2)
    f = t * (len(cols) - 1) - ci
    c = tuple(int(cols[ci][k] + (cols[ci + 1][k] - cols[ci][k]) * f) for k in range(3))
    d.line([gx + 2, sun_top + i, gx + gw - 2, sun_top + i], fill=c)
# sun disc
sx, sy, sr = gx + gw // 2, sun_top + 92, 46
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 120))
# skyline silhouettes
import random
random.seed(7)
base = sun_top + sun_h
skyline_col = (30, 12, 52)
bx = gx + 2
while bx < gx + gw - 2:
    bw = random.randint(18, 42)
    bh = random.randint(28, 78)
    d.rectangle([bx, base - bh, bx + bw, base], fill=skyline_col)
    bx += bw + random.randint(2, 8)
# palm trees
def palm(px, py, s, col=(74, 38, 96)):
    d.line([px, py, px + 4 * s, py - 34 * s], fill=col, width=max(2, 3 * s))
    tx, ty = px + 4 * s, py - 34 * s
    for ang in (-70, -35, 0, 35, 70):
        import math
        a = math.radians(ang - 90)
        ex = tx + int(20 * s * math.cos(a))
        ey = ty + int(20 * s * math.sin(a)) + 8 * s
        d.arc([tx - 20 * s, ty - 6 * s, tx + 20 * s, ty + 22 * s], 200 + ang, 340 + ang, fill=col, width=3)
palm(gx + 30, base + 4, 1)
palm(gx + gw - 52, base + 4, 1)
# road + car silhouette
d.rectangle([gx + 2, base, gx + gw - 2, LY + LH - 96], fill=(14, 8, 30))
d.line([gx + 2, base + 26, gx + gw - 2, base + 26], fill=(255, 183, 77), width=2)
# car
carx, cary = gx + gw // 2 - 62, base + 6
d.polygon([(carx, cary + 14), (carx + 16, cary), (carx + 88, cary),
           (carx + 108, cary + 14), (carx + 124, cary + 14), (carx + 124, cary + 26),
           (carx, cary + 26)], fill=(8, 4, 18))
d.ellipse([carx + 18, cary + 22, carx + 38, cary + 34], fill=(8, 4, 18))
d.ellipse([carx + 86, cary + 22, carx + 106, cary + 34], fill=(8, 4, 18))
# headline + caption
gy = LY + LH - 96
gt_lines = ["GTA 6 PASSES $1.8BN —", "OUTGROSSES THE ODYSSEY"]
gt_size = 24
while gt_size > 14:
    gt_f = font(F_SERIF, gt_size)
    if max(gt_f.getlength(gl) for gl in gt_lines) <= gw - 28:
        break
    gt_size -= 1
for i, gl in enumerate(gt_lines):
    d.text((gx + 14, gy + i * (gt_size + 6)), gl, font=gt_f, fill=(255, 214, 120))
d.text((gx + 14, gy + 62), "Sales top the $1.80bn global run of The Odyssey.",
       font=font(F_SANS, 14), fill=(226, 214, 235))

# =========================================================
# GRID  3 cols x 3 rows   y 498 .. 1000
# =========================================================
GY, GH = 498, 502
cols_x = [28, 356, 684]
cw, ch, gap = 312, 160, 11
rows_y = [GY, GY + ch + gap, GY + 2 * (ch + gap)]

HF = font(F_SERIF, 18)     # grid headline
CF = font(F_SANS, 13)      # grid caption
KF = font(F_SANSB, 11)     # kicker

def story_panel(x, y, kicker, headline, caption, draw_art):
    panel(x, y, cw, ch, fill=WHITE)
    d.rectangle([x + 2, y + 2, x + cw - 2, y + 62], fill=(238, 234, 222))
    draw_art(x + 2, y + 2, cw - 4, 60)
    d.text((x + 10, y + 70), kicker, font=KF, fill=RED)
    hl = wrap(headline, HF, cw - 20)
    yy = draw_lines(d, x + 10, y + 86, hl[:2], HF, INK, spacing=1)
    cl = wrap(caption, CF, cw - 20)
    draw_lines(d, x + 10, y + 128, cl[:2], CF, INK_SOFT, spacing=1)

# --- art helpers ---
def art_cyclone(x, y, w, h):
    import math
    cx, cy = x + w // 2 + 30, y + h // 2 + 2
    for i, r in enumerate(range(4, 34, 5)):
        col = (23, 107, 110) if i % 2 == 0 else (174, 214, 224)
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + i * 55, 300 + i * 55, fill=col, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.line([x + 12, y + h - 8, x + w - 12, y + h - 8], fill=(23, 107, 110), width=3)
    d.text((x + 12, y + 6), "ODISHA", font=font(F_SANSB, 11), fill=INK_SOFT)

def art_voyager(x, y, w, h):
    import math, random
    random.seed(3)
    d.rectangle([x, y, x + w, y + h], fill=(12, 18, 40))
    for _ in range(26):
        px, py = x + random.randint(2, w - 2), y + random.randint(2, h - 2)
        d.ellipse([px, py, px + 2, py + 2], fill=WHITE)
    cx, cy = x + w // 2 - 10, y + h // 2
    d.rectangle([cx - 18, cy - 9, cx + 18, cy + 9], fill=(200, 200, 200))  # bus
    d.polygon([(cx + 18, cy - 16), (cx + 44, cy - 28), (cx + 44, cy + 4)], outline=(255, 214, 120), width=2)  # dish
    d.line([cx + 18, cy - 6, cx + 44, cy - 16], fill=(255, 214, 120), width=2)
    d.line([cx - 18, cy - 9, cx - 46, cy - 30], fill=(200, 200, 200), width=3)  # boom
    d.line([cx, cy + 9, cx, cy + 26], fill=(200, 200, 200), width=2)
    d.text((x + 10, y + 6), "1 LIGHT-DAY", font=font(F_SANSB, 12), fill=(255, 214, 120))

def art_hayabusa(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 28, 34))
    cx, cy = x + 56, y + h // 2
    d.ellipse([cx - 27, cy - 20, cx + 27, cy + 20], fill=(150, 140, 128))
    d.ellipse([cx - 14, cy - 9, cx - 3, cy + 2], fill=(110, 100, 90))
    d.ellipse([cx + 7, cy + 5, cx + 16, cy + 14], fill=(110, 100, 90))
    px, py = x + w - 78, y + 12
    d.rectangle([px, py + 8, px + 34, py + 22], fill=(210, 210, 210))
    d.polygon([(px + 34, py + 4), (px + 52, py + 15), (px + 34, py + 26)], outline=(255, 214, 120), width=2)
    d.polygon([(px + 6, py + 30), (px + 12, py + 44), (px + 16, py + 30)], fill=(255, 120, 60))
    d.polygon([(px + 20, py + 30), (px + 26, py + 46), (px + 30, py + 30)], fill=(255, 180, 60))
    d.text((x + 10, y + 6), "ENGINE TROUBLE", font=font(F_SANSB, 11), fill=(255, 120, 60))

def art_europe(x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx = cx + int(22 * math.cos(a)); sy = cy + int(22 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    d.text((x + 10, y + 6), "TALKS", font=font(F_SANSB, 12), fill=WHITE)
    d.rectangle([x + w - 52, y + h - 18, x + w - 10, y + h - 6], fill=WHITE)
    d.rectangle([x + w - 52, y + h - 14, x + w - 10, y + h - 10], fill=(0, 57, 166))
    d.rectangle([x + w - 52, y + h - 10, x + w - 10, y + h - 6], fill=(213, 0, 50))

def art_cop(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 236, 214))
    cx, cy = x + w // 2, y + h // 2 + 2
    d.ellipse([cx - 22, cy - 20, cx + 22, cy + 20], fill=(46, 139, 87))
    d.arc([cx - 14, cy - 12, cx + 14, cy + 12], 200, 340, fill=WHITE, width=3)
    d.arc([cx - 14, cy - 12, cx + 14, cy + 12], 20, 160, fill=WHITE, width=3)
    d.ellipse([cx + 12, cy - 30, cx + 26, cy - 14], fill=(46, 139, 87))  # leaf
    d.text((x + 10, y + 6), "COP31", font=font(F_SANSB, 12), fill=(23, 80, 40))

def art_boat(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(174, 214, 224))
    for wy in (y + 34, y + 46):
        for wx in range(x, x + w, 26):
            d.arc([wx, wy - 6, wx + 26, wy + 8], 180, 360, fill=(23, 107, 110), width=3)
    # tilted boat
    d.polygon([(x + 90, y + 22), (x + 190, y + 30), (x + 170, y + 44), (x + 110, y + 40)],
              fill=(120, 72, 20))
    d.line([x + 140, y + 22, x + 140, y + 4], fill=(90, 60, 20), width=3)
    # life ring
    rx, ry = x + 44, y + 30
    d.ellipse([rx - 14, ry - 14, rx + 14, ry + 14], outline=RED, width=6)
    d.ellipse([rx - 5, ry - 5, rx + 5, ry + 5], outline=RED, width=2)

def art_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 139, 87))
    d.rectangle([x + 8, y + 24, x + w - 8, y + 44], fill=(196, 164, 110))  # pitch strip
    for i in range(3):  # stumps
        sx = x + w - 72 + i * 12
        d.rectangle([sx, y + 6, sx + 6, y + 28], fill=(255, 220, 100))
    d.rectangle([x + w - 72, y + 4, x + w - 36, y + 7], fill=(255, 220, 100))  # bails
    d.line([x + 30, y + 46, x + 78, y + 12], fill=(220, 190, 140), width=8)  # bat
    d.ellipse([x + 96, y + 30, x + 110, y + 44], fill=RED)  # ball
    d.text((x + 10, y + 4), "100*", font=font(F_SANSB, 14), fill=WHITE)

def art_tanker(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 40, 66))
    d.rectangle([x, y + 34, x + w, y + h], fill=(16, 60, 90))
    # ship hull
    d.polygon([(x + 60, y + 30), (x + 250, y + 30), (x + 230, y + 48), (x + 80, y + 48)], fill=(90, 90, 96))
    d.rectangle([x + 150, y + 14, x + 190, y + 30], fill=(120, 120, 126))
    # explosion starburst
    ex, ey = x + 110, y + 22
    for a in range(0, 360, 30):
        import math
        r = 16 if a % 60 == 0 else 9
        d.line([ex, ey, ex + int(r * math.cos(math.radians(a))),
                ey + int(r * math.sin(math.radians(a)))], fill=(255, 180, 60), width=3)
    d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 220, 120))
    # projectile streaks
    d.line([x + 40, y + 6, x + 96, y + 18], fill=(255, 255, 255), width=2)
    d.line([x + 250, y + 4, x + 200, y + 14], fill=(255, 255, 255), width=2)

stories = [
    ("CYCLONE  •  INDIA", "CYCLONE AKVAN BEARS DOWN ON ODISHA",
     "About 300,000 evacuated as landfall nears today.", art_cyclone),
    ("SPACE  •  NASA", "VOYAGER 1 REACHES ONE LIGHT-DAY",
     "from Earth — the farthest human-made object keeps going.", art_voyager),
    ("SPACE  •  JAPAN", "HAYABUSA2 ENGINE TROUBLE AXES LANDING",
     "Asteroid touchdown abandoned; mission replanned.", art_hayabusa),
    ("EUROPE  •  UKRAINE", "EUROPE READY FOR TALKS WITH RUSSIA",
     "Leaders say Europe will negotiate to end the war.", art_europe),
    ("CLIMATE  •  COP31", "COP31 DRAFT DROPS FOSSIL-FUEL REFERENCE",
     "IEA: data-centre power use could double by 2030.", art_cop),
    ("SENEGAL", "MIGRANT BOAT SINKS OFF SENEGAL",
     "Dozens missing after the vessel goes down.", art_boat),
    ("CRICKET  •  WELLINGTON", "NICHOLLS’ UNBEATEN CENTURY ON DAY ONE",
     "New Zealand bat first against India in the Test.", art_cricket),
    ("BLACK SEA  •  BULGARIA", "SUNK LPG TANKER ‘HIT BY PROJECTILES’",
     "Officials say the vessel was struck before sinking.", art_tanker),
]

positions = [(cols_x[c], rows_y[r]) for r in range(3) for c in range(3)]
for (kicker, head, cap, art), (px, py) in zip(stories, positions):
    story_panel(px, py, kicker, head, cap, art)

# ---------- 9th cell: by the numbers ----------
nx, ny = positions[8]
panel(nx, ny, cw, ch, fill=INK)
d.text((nx + 12, ny + 10), "THE DAY IN NUMBERS", font=font(F_SANSB, 13), fill=GOLD)
nums = [("300,000", "evacuated in Odisha"),
        ("1 light-day", "Voyager 1 from Earth"),
        ("$1.80bn", "The Odyssey’s global run"),
        ("100*", "Nicholls, not out")]
yy = ny + 34
num_f = font(F_SERIF, 19)
for big, small in nums:
    bw = num_f.getlength(big)
    d.text((nx + 12, yy), big, font=num_f, fill=WHITE)
    sm = wrap(small, font(F_SANS, 13), cw - 24 - bw - 12)
    draw_lines(d, nx + 24 + bw, yy + 3, sm[:1], font(F_SANS, 13), (200, 208, 224), spacing=1)
    yy += 30

# footer
d.line([28, 1008, W - 28, 1008], fill=INK, width=1)
d.text((28, 1012), "Sources: Reuters · BBC · The Hindu · NASA · Space.com — 20 November 2026",
       font=font(F_SANS, 11), fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
