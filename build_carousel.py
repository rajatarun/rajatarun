#!/usr/bin/env python3
"""Generate the AIWeave cost-vs-efficiency LinkedIn carousel as a square PDF.

Square 1080x1080 pages, dark editorial aesthetic, monospace + cyan/gold accents.
LinkedIn renders multi-page PDFs as native document carousels.
"""
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- palette ---
BG      = (0x0B/255, 0x0E/255, 0x11/255)   # near-black
CYAN    = (0x22/255, 0xD3/255, 0xEE/255)
GOLD    = (0xE8/255, 0xB3/255, 0x39/255)
GRAY    = (0x9C/255, 0xA3/255, 0xAF/255)
DIM     = (0x4B/255, 0x55/255, 0x63/255)
GHOST   = (0x1A/255, 0x1F/255, 0x24/255)   # ~8% lift over bg
REDX    = (0xC0/255, 0x4B/255, 0x4B/255)

W = H = 1080
M = 96  # margin

MONO = "Mono"
MONOB = "MonoB"
pdfmetrics.registerFont(TTFont(MONO,  "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont(MONOB, "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"))

c = canvas.Canvas("aiweave-cost-vs-efficiency-carousel.pdf", pagesize=(W, H))


def bg():
    c.setFillColorRGB(*BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def wrap(text, font, size, maxw):
    return simpleSplit(text, font, size, maxw)


def draw_block(lines, x, y, font, size, color, leading=None, align="left", maxw=None):
    """Draw lines downward from y (baseline of first line). Returns y after block."""
    if leading is None:
        leading = size * 1.32
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    for ln in lines:
        if align == "center":
            c.drawCentredString(x, y, ln)
        else:
            c.drawString(x, y, ln)
        y -= leading
    return y


def headline(text, top, size=58, color=CYAN, align="center", maxw=None):
    maxw = maxw or (W - 2*M)
    lines = wrap(text, MONOB, size, maxw)
    x = W/2 if align == "center" else M
    return draw_block(lines, x, top, MONOB, size, color, leading=size*1.22, align=align, maxw=maxw)


def subcopy(text_lines, top, size=26, color=GRAY, align="center", maxw=None):
    maxw = maxw or (W - 2*M)
    x = W/2 if align == "center" else M
    y = top
    c.setFont(MONO, size)
    c.setFillColorRGB(*color)
    for t in text_lines:
        for ln in wrap(t, MONO, size, maxw):
            if align == "center":
                c.drawCentredString(x, y, ln)
            else:
                c.drawString(x, y, ln)
            y -= size * 1.4
    return y


def footer(text=" AIWeave / applied research", color=DIM):
    c.setFont(MONO, 20)
    c.setFillColorRGB(*color)
    c.drawString(M, M - 36, text)


def rule(y, x0=M, x1=W-M, color=GOLD, w=3):
    c.setStrokeColorRGB(*color)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)


def page_tag(n):
    c.setFont(MONO, 18)
    c.setFillColorRGB(*DIM)
    c.drawRightString(W - M, M - 36, f"{n:02d} / 07")


# ============================================================ SLIDE 1 — COVER
bg()
# ghost words
c.setFont(MONOB, 120)
c.setFillColorRGB(*GHOST)
c.drawString(M - 10, H - 230, "$ COST")
c.drawRightString(W - M + 10, 200, "EFFICIENCY")
# headline
y = headline("Cost cutting and efficiency are not the same thing.", H/2 + 150, size=62, color=CYAN)
rule(y + 24, x0=M+60, x1=W-M-60)
subcopy(["Most teams optimize the bill.", "The bill is the symptom."], y - 30, size=30, color=GRAY)
footer()
page_tag(1)
c.showPage()

# ============================================================ SLIDE 2
bg()
headline("Cutting cost shrinks the system.", H - 140, size=44, color=CYAN, align="left")
headline("Efficiency shrinks the waste.", H - 200, size=44, color=GOLD, align="left")
# two boxes
bx, by, bw, bh = M, 300, 380, 300
# left: COST CUT — whole box shrinks (draw outer faint + inner shrunk solid + down arrow)
c.setStrokeColorRGB(*DIM); c.setLineWidth(2)
c.rect(bx, by, bw, bh, stroke=1, fill=0)
c.setStrokeColorRGB(*GOLD); c.setLineWidth(3)
c.rect(bx+50, by+40, bw-100, bh-130, stroke=1, fill=0)
c.setFillColorRGB(*CYAN); c.setFont(MONOB, 26)
c.drawCentredString(bx+bw/2, by+bh+24, "COST CUT")
# down arrow (gold)
c.setStrokeColorRGB(*GOLD); c.setLineWidth(4)
ax = bx+bw/2
c.line(ax, by+bh-150, ax, by+60)
c.line(ax, by+60, ax-18, by+90); c.line(ax, by+60, ax+18, by+90)
c.setFillColorRGB(*DIM); c.setFont(MONO, 20)
c.drawCentredString(bx+bw/2, by-40, "system shrinks")
# right: EFFICIENCY — frame intact, inner waste block deleted
rx = W - M - bw
c.setStrokeColorRGB(*CYAN); c.setLineWidth(3)
c.rect(rx, by, bw, bh, stroke=1, fill=0)
# hatched gold waste block being deleted (dashed outline w/ X)
c.setStrokeColorRGB(*GOLD); c.setDash(6, 5); c.setLineWidth(2)
c.rect(rx+90, by+90, bw-180, bh-180, stroke=1, fill=0)
c.line(rx+90, by+90, rx+bw-90, by+bh-90)
c.line(rx+90, by+bh-90, rx+bw-90, by+90)
c.setDash()
c.setFillColorRGB(*CYAN); c.setFont(MONOB, 26)
c.drawCentredString(rx+bw/2, by+bh+24, "EFFICIENCY")
c.setFillColorRGB(*DIM); c.setFont(MONO, 20)
c.drawCentredString(rx+bw/2, by-40, "only waste removed")
# subcopy bottom
subcopy([
    "Throttle the model, cap the context, ship worse output —",
    "costs drop. So does the product.",
    "Efficiency removes work the system never needed to do.",
], 230, size=24, color=GRAY)
footer(); page_tag(2)
c.showPage()

# ============================================================ SLIDE 3 — STAT
bg()
headline("ScreenWeave: 91% cost reduction,", H - 140, size=44, color=CYAN, align="left")
headline("zero capability removed.", H - 195, size=44, color=CYAN, align="left")
# big 91%
c.setFont(MONOB, 300)
c.setFillColorRGB(*GOLD)
c.drawCentredString(W/2 - 40, H/2 - 200, "91%")
c.setFont(MONO, 30); c.setFillColorRGB(*CYAN)
c.drawCentredString(W/2 - 40, H/2 - 250, "ScreenWeave — cost per run")
# before/after bars — lower-left, clearly separated from the big stat
bx = M + 30
basey = 250
c.setFillColorRGB(*CYAN)
c.rect(bx, basey, 46, 180, stroke=0, fill=1)          # before tall
c.rect(bx+90, basey, 46, 16, stroke=0, fill=1)         # after short (~9%)
c.setFont(MONO, 18); c.setFillColorRGB(*DIM)
c.drawCentredString(bx+23, basey - 28, "before")
c.drawCentredString(bx+113, basey - 28, "after")
subcopy([
    "We didn't downgrade the model or starve the context.",
    "We cut the redundant work the agent kept repeating.",
], 230, size=26, color=GRAY)
footer(); page_tag(3)
c.showPage()

# ============================================================ SLIDE 4
bg()
headline("Where the waste actually lives.", H - 150, size=54, color=CYAN, align="left")
rows = [
    ("redundant payload", "re-sending context the model already has"),
    ("repeated step",     "re-running steps that didn't change"),
    ("tier mismatch",     "premium-tier tokens for tier-floor work"),
]
ry = H - 300
for i, (tag, _) in enumerate(rows):
    yy = ry - i*150
    # cyan pipeline
    c.setStrokeColorRGB(*CYAN); c.setLineWidth(4)
    c.line(M, yy, W - M - 360, yy)
    # gold leak node mid-pipeline
    nx = (M + (W - M - 360)) / 2
    c.setFillColorRGB(*GOLD)
    c.circle(nx, yy, 12, stroke=0, fill=1)
    c.setStrokeColorRGB(*GOLD); c.setLineWidth(2)
    c.line(nx, yy, nx, yy - 34)  # leak drip
    # annotation right margin
    c.setFont(MONO, 24); c.setFillColorRGB(*GRAY)
    c.drawString(W - M - 330, yy - 8, tag)
subcopy([
    "Re-sending context. Re-running steps.",
    "Paying premium rates for floor-level work.",
], 230, size=26, color=DIM)
footer(); page_tag(4)
c.showPage()

# ============================================================ SLIDE 5
bg()
headline("Efficiency is an architecture", H - 140, size=46, color=CYAN, align="left")
headline("decision, not a settings toggle.", H - 200, size=46, color=GOLD, align="left")
# node diagram CONTEXT -> ROUTING -> STATE
blocks = ["CONTEXT", "ROUTING", "STATE"]
cy = H/2 - 40
bw2 = 230; gap = 60
total = len(blocks)*bw2 + (len(blocks)-1)*gap
sx = (W - total)/2
for i, b in enumerate(blocks):
    x0 = sx + i*(bw2+gap)
    c.setStrokeColorRGB(*CYAN); c.setLineWidth(3)
    c.rect(x0, cy, bw2, 90, stroke=1, fill=0)
    c.setFont(MONOB, 26); c.setFillColorRGB(*CYAN)
    c.drawCentredString(x0+bw2/2, cy+34, b)
    if i < len(blocks)-1:
        c.setStrokeColorRGB(*GOLD); c.setLineWidth(4)
        ax0 = x0+bw2; ax1 = x0+bw2+gap
        c.line(ax0, cy+45, ax1, cy+45)
        c.line(ax1, cy+45, ax1-16, cy+57); c.line(ax1, cy+45, ax1-16, cy+33)
# crossed toggle "not here"
tx, ty = W/2 - 60, cy - 160
c.setStrokeColorRGB(*DIM); c.setLineWidth(3)
c.roundRect(tx, ty, 120, 50, 25, stroke=1, fill=0)
c.circle(tx+35, ty+25, 18, stroke=1, fill=0)
c.setLineWidth(3)
c.line(tx-10, ty-10, tx+130, ty+60)  # strike-through
c.setFont(MONO, 22); c.setFillColorRGB(*DIM)
c.drawCentredString(tx+60, ty-30, "not here")
subcopy([
    "You don't find 91% in a config flag.",
    "You find it in how context, routing, and state are designed.",
], 200, size=24, color=GRAY)
footer(); page_tag(5)
c.showPage()

# ============================================================ SLIDE 6
bg()
headline("The test: cut the bill,", H - 150, size=50, color=CYAN, align="left")
headline("does the output survive?", H - 210, size=50, color=GOLD, align="left")
# decision fork
ix, iy = M + 40, H/2 - 30
c.setStrokeColorRGB(*CYAN); c.setLineWidth(4)
c.line(ix, iy, ix+200, iy)
fork = ix+200
# top branch — quality drops -> cost cut (X)
c.setStrokeColorRGB(*GOLD); c.setLineWidth(4)
c.line(fork, iy, fork+120, iy+120)
c.line(fork, iy, fork+120, iy-120)
# top label
c.setFont(MONOB, 26); c.setFillColorRGB(*GRAY)
c.drawString(fork+150, iy+110, "QUALITY DROPS")
c.setFillColorRGB(*REDX); c.setFont(MONOB, 26)
c.drawString(fork+150, iy+72, "→ cost cut  ✗")
# bottom label
c.setFont(MONOB, 26); c.setFillColorRGB(*GRAY)
c.drawString(fork+150, iy-90, "QUALITY HOLDS")
c.setFillColorRGB(*CYAN); c.setFont(MONOB, 26)
c.drawString(fork+150, iy-128, "→ efficiency  ✓")
subcopy([
    "If quality drops, you cut cost.",
    "If quality holds, you cut waste.",
    "Only one of those scales.",
], 230, size=26, color=GRAY)
footer(); page_tag(6)
c.showPage()

# ============================================================ SLIDE 7 — CLOSE
bg()
rule(H - 120, color=GOLD, w=3)
rule(150, color=GOLD, w=3)
y = headline("Measure waste, not spend.", H/2 + 230, size=70, color=GOLD)
subcopy([
    "Spend tells you what you paid.",
    "Waste tells you what you can remove",
    "without losing anything.",
], y - 20, size=28, color=GRAY)
# CTA
c.setFont(MONOB, 30); c.setFillColorRGB(*CYAN)
cta = wrap("What's the most expensive redundant step in your agent pipeline right now — and is anyone measuring it?", MONOB, 30, W - 2*M - 40)
yy = H/2 - 200
for ln in cta:
    c.drawCentredString(W/2, yy, ln)
    yy -= 40
c.setFont(MONO, 22); c.setFillColorRGB(*DIM)
c.drawCentredString(W/2, 180, "AIWeave / applied research — aiweave.org")
page_tag(7)
c.showPage()

c.save()
print("wrote aiweave-cost-vs-efficiency-carousel.pdf")
