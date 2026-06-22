#!/usr/bin/env python3
"""
Context Engineering — 4-Operation Pattern
7-slide LinkedIn-compatible carousel (1080x1080 square PDF)
Dark editorial aesthetic: #0B0E11 / cyan / gold / DejaVu Sans Mono
"""
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- palette ---
BG    = (0x0B/255, 0x0E/255, 0x11/255)
CYAN  = (0x22/255, 0xD3/255, 0xEE/255)
GOLD  = (0xE8/255, 0xB3/255, 0x39/255)
WHITE = (0xF1/255, 0xF5/255, 0xF9/255)
GRAY  = (0x9C/255, 0xA3/255, 0xAF/255)
DIM   = (0x4B/255, 0x55/255, 0x63/255)
GHOST = (0x16/255, 0x1B/255, 0x22/255)
RED   = (0xC0/255, 0x4B/255, 0x4B/255)

W = H = 1080
M = 80   # margin

pdfmetrics.registerFont(TTFont("Mono",  "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("MonoB", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"))

OUT = "context-engineering-carousel.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))


# ── helpers ────────────────────────────────────────────────────────────────

def bg():
    c.setFillColorRGB(*BG); c.rect(0, 0, W, H, stroke=0, fill=1)

def rule(y, x0=M, x1=W-M, color=GOLD, w=2):
    c.setStrokeColorRGB(*color); c.setLineWidth(w); c.line(x0, y, x1, y)

def footer(slide_n, total=7, label="AIWeave / applied research"):
    c.setFont("Mono", 18); c.setFillColorRGB(*DIM)
    c.drawString(M, 46, label)
    c.drawRightString(W-M, 46, f"{slide_n:02d} / {total:02d}")

def tag(text, x, y, fg=BG, bg_col=CYAN):
    c.setFont("MonoB", 20)
    tw = c.stringWidth(text, "MonoB", 20)
    pad = 14
    c.setFillColorRGB(*bg_col)
    c.roundRect(x-pad, y-6, tw+pad*2, 34, 6, stroke=0, fill=1)
    c.setFillColorRGB(*fg)
    c.drawString(x, y+4, text)

def wrapped_text(text, x, y, font, size, color, maxw, leading=None):
    if leading is None: leading = size * 1.38
    lines = simpleSplit(text, font, size, maxw)
    c.setFont(font, size); c.setFillColorRGB(*color)
    for ln in lines:
        c.drawString(x, y, ln); y -= leading
    return y

def centered_text(text, y, font, size, color, maxw=None):
    maxw = maxw or (W - 2*M)
    lines = simpleSplit(text, font, size, maxw)
    c.setFont(font, size); c.setFillColorRGB(*color)
    leading = size * 1.3
    for ln in lines:
        c.drawCentredString(W/2, y, ln); y -= leading
    return y

def operation_badge(label, x, y, active=True):
    """Small pill badge for slide 6 table."""
    col = CYAN if active else DIM
    c.setFont("MonoB", 22)
    tw = c.stringWidth(label, "MonoB", 22)
    pad = 12
    c.setStrokeColorRGB(*col); c.setLineWidth(2)
    c.roundRect(x-pad, y-8, tw+pad*2, 38, 8, stroke=1, fill=0)
    c.setFillColorRGB(*col)
    c.drawString(x, y+4, label)


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — HOOK
# ══════════════════════════════════════════════════════════════════════════════
bg()

# ghost number in background
c.setFont("MonoB", 340); c.setFillColorRGB(*GHOST)
c.drawCentredString(W/2 + 20, 120, "4")

# top rule
rule(H - 110, color=CYAN, w=3)

# main headline — two visual lines
c.setFont("MonoB", 42); c.setFillColorRGB(*WHITE)
y = H - 175
for line in ["Prompt engineering is dead.", "Everyone agrees."]:
    c.drawString(M, y, line); y -= 54

c.setFont("MonoB", 38); c.setFillColorRGB(*GRAY)
c.drawString(M, y, "Almost no one has noticed that"); y -= 50

# highlight block
c.setFont("MonoB", 38); c.setFillColorRGB(*CYAN)
y2 = wrapped_text(
    '"context engineering" is just four operations',
    M, y, "MonoB", 38, CYAN, W - 2*M - 20, leading=48
)
y = y2 - 12

c.setFont("MonoB", 34); c.setFillColorRGB(*WHITE)
c.drawString(M, y, "— write, select, compress, isolate —"); y -= 48

c.setFont("MonoB", 34); c.setFillColorRGB(*GOLD)
wrapped_text("and that three of them belong to a router, not a human.",
             M, y, "MonoB", 34, GOLD, W - 2*M, leading=42)

# subtitle
rule(168, color=GOLD, w=2)
c.setFont("Mono", 22); c.setFillColorRGB(*GRAY)
c.drawString(M, 130, "What we built to prove it.")

footer(1)
c.showPage()


# ══════════════════════════════════════════════════════════════════════════════
# SLIDES 2–5 — One operation each
# ══════════════════════════════════════════════════════════════════════════════

ops = [
    {
        "n": 2,
        "op": "WRITE",
        "label": "Operation 01",
        "color": GOLD,
        "subtitle": "The human gate.",
        "body": [
            "WRITE is what you still do: author the system message,",
            "the user query, the few-shot examples.",
            "",
            "This is intent capture — you're encoding what the model",
            "should care about. It's not automatable because semantic",
            "intent requires a human who knows the domain.",
            "",
            "This is where most teams stop. They write a prompt,",
            "call it engineering, ship it.",
            "",
            "They're one operation in. There are three more.",
        ],
        "verdict": "STAYS HUMAN",
        "verdict_color": GOLD,
    },
    {
        "n": 3,
        "op": "SELECT",
        "label": "Operation 02",
        "color": CYAN,
        "subtitle": "The router wakes up.",
        "body": [
            "SELECT picks the minimal context that answers this query.",
            "",
            "This is RAG, semantic search, graph traversal — any filter",
            "that says 'include this chunk, exclude that one.'",
            "",
            "Most teams stop here too. They call this 'done.'",
            "The LLM still sees bloat. Latency still scales with corpus",
            "size, not query specificity.",
            "",
            "SELECT is necessary. It is not sufficient.",
        ],
        "verdict": "AUTOMATES",
        "verdict_color": CYAN,
    },
    {
        "n": 4,
        "op": "COMPRESS",
        "label": "Operation 03",
        "color": CYAN,
        "subtitle": "Where token spend collapses.",
        "body": [
            "COMPRESS removes redundancy within the selected chunks.",
            "",
            "Strip boilerplate. Summarize repeated patterns. Extract",
            "only the signal — 'line 247 is the function you need,'",
            "not the whole 500-line file.",
            "",
            "Compression ratio on typical doc/code sets: 3:1 to 8:1.",
            "This is where ContextWeave enters.",
            "",
            "Most teams skip this. 'LLMs are cheap now.' They're not.",
        ],
        "verdict": "AUTOMATES",
        "verdict_color": CYAN,
    },
    {
        "n": 5,
        "op": "ISOLATE",
        "label": "Operation 04",
        "color": CYAN,
        "subtitle": "The guard rail. Almost never built.",
        "body": [
            "ISOLATE injects metadata barriers so the model can't",
            "conflate contexts from different sources.",
            "",
            "Example: 'best practices from doc A' and 'your codebase",
            "from doc B' need explicit namespace tags. Without them,",
            "the model hallucinates 'best practice X applies to your",
            "code' — when it doesn't.",
            "",
            "ISOLATE = semantic namespace enforcement.",
            "Costs nearly nothing. Catches 60%+ of confabulation",
            "errors in multi-context settings. Underrated.",
        ],
        "verdict": "AUTOMATES",
        "verdict_color": CYAN,
    },
]

for op in ops:
    bg()

    # left accent bar
    c.setFillColorRGB(*op["color"])
    c.rect(M, 130, 6, H - 230, stroke=0, fill=1)

    # operation label (small, top)
    c.setFont("Mono", 20); c.setFillColorRGB(*DIM)
    c.drawString(M + 26, H - 100, op["label"])

    # big operation name
    c.setFont("MonoB", 86); c.setFillColorRGB(*op["color"])
    c.drawString(M + 20, H - 190, op["op"])

    # subtitle
    c.setFont("Mono", 28); c.setFillColorRGB(*GRAY)
    c.drawString(M + 20, H - 235, op["subtitle"])

    rule(H - 258, x0=M+20, x1=W-M, color=DIM, w=1)

    # body text
    y = H - 298
    for line in op["body"]:
        if line == "":
            y -= 16; continue
        c.setFont("Mono", 26); c.setFillColorRGB(*WHITE)
        lines = simpleSplit(line, "Mono", 26, W - M - 120)
        for ln in lines:
            c.drawString(M + 20, y, ln); y -= 36

    # verdict badge (bottom right)
    tag(op["verdict"], W - M - 220, 80, fg=BG, bg_col=op["verdict_color"])

    footer(op["n"])
    c.showPage()


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — THE SPLIT
# ══════════════════════════════════════════════════════════════════════════════
bg()
rule(H - 110, color=GOLD, w=3)

c.setFont("MonoB", 52); c.setFillColorRGB(*WHITE)
c.drawString(M, H - 172, "The automation boundary.")

c.setFont("Mono", 26); c.setFillColorRGB(*GRAY)
c.drawString(M, H - 214, "Which operations belong to a router. Which stay human.")

rule(H - 236, color=DIM, w=1)

# two-column table
col1x = M + 20
col2x = W // 2 + 20
row_h = 90

# headers
c.setFont("MonoB", 26)
c.setFillColorRGB(*GOLD); c.drawString(col1x, H - 290, "STAYS HUMAN")
c.setFillColorRGB(*CYAN); c.drawString(col2x, H - 290, "AUTOMATES")

rule(H - 306, color=DIM, w=1)

# rows
human_ops  = [("WRITE",    "Intent is human-defined.\nCan't commoditize context.",)]
auto_ops   = [
    ("SELECT",   "Semantic relevance is\nmeasurable."),
    ("COMPRESS", "Redundancy detection\nis algorithmic."),
    ("ISOLATE",  "Tagging schema defined\nonce, applied at scale."),
]

row_h = 100
y = H - 340
for op_name, reason in human_ops:
    c.setFont("MonoB", 30); c.setFillColorRGB(*GOLD)
    c.drawString(col1x, y, op_name)
    c.setFont("Mono", 22); c.setFillColorRGB(*GRAY)
    for i, ln in enumerate(reason.split("\n")):
        c.drawString(col1x, y - 36 - i*28, ln)
    y -= row_h * 3

y = H - 340
for op_name, reason in auto_ops:
    c.setFont("MonoB", 30); c.setFillColorRGB(*CYAN)
    c.drawString(col2x, y, op_name)
    c.setFont("Mono", 22); c.setFillColorRGB(*GRAY)
    for i, ln in enumerate(reason.split("\n")):
        c.drawString(col2x, y - 36 - i*28, ln)
    y -= row_h

# vertical divider
mid = W // 2
rule(H - 290, x0=mid, x1=mid, color=DIM, w=1)
c.setStrokeColorRGB(*DIM); c.setLineWidth(1)
c.line(mid, 130, mid, H - 306)

# bottom callout
rule(160, color=CYAN, w=2)
c.setFont("MonoB", 26); c.setFillColorRGB(*CYAN)
c.drawString(M, 120, "ContextWeave (Apache 2.0, aiweave.org) — implements all three.")

footer(6)
c.showPage()


# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — RECAP + QUESTION + CTA
# ══════════════════════════════════════════════════════════════════════════════
bg()
rule(H - 110, color=GOLD, w=3)
rule(110, color=GOLD, w=3)

# recap label
c.setFont("Mono", 20); c.setFillColorRGB(*DIM)
c.drawString(M, H - 155, "The framework")

c.setFont("MonoB", 48); c.setFillColorRGB(*WHITE)
c.drawString(M, H - 210, "Context engineering =")
c.setFont("MonoB", 48); c.setFillColorRGB(*CYAN)
c.drawString(M, H - 262, "a system you can meter.")

rule(H - 286, color=DIM, w=1)

# four ops summary strip
strip_y = H - 340
strip_w = (W - 2*M - 30) // 4
labels  = ["WRITE", "SELECT", "COMPRESS", "ISOLATE"]
colors  = [GOLD,    CYAN,     CYAN,       CYAN]
for i, (lbl, col) in enumerate(zip(labels, colors)):
    sx = M + i * (strip_w + 10)
    c.setFillColorRGB(*GHOST); c.rect(sx, strip_y - 44, strip_w, 60, stroke=0, fill=1)
    c.setFont("MonoB", 20); c.setFillColorRGB(*col)
    c.drawCentredString(sx + strip_w//2, strip_y - 22, lbl)

# body
body = [
    "Prompt engineering was always a proxy for 'get the context right.'",
    "Now the three mechanical operations can be automated.",
    "SELECT, COMPRESS, ISOLATE belong to the router.",
    "WRITE — the only one that requires your intent — stays yours.",
    "",
    "91% token reduction on production agent loops.",
    "(ContextWeave / ExpertiseRAG — aiweave.org, Apache 2.0)",
]
y = strip_y - 76
for line in body:
    if line == "": y -= 14; continue
    font = "MonoB" if line.startswith("91%") else "Mono"
    col  = GOLD   if line.startswith("91%") else (GRAY if line.startswith("(") else WHITE)
    size = 28     if line.startswith("91%") else 24
    y = wrapped_text(line, M, y, font, size, col, W - 2*M, leading=32)

# closing question
rule(y - 14, color=CYAN, w=1)
y -= 36
c.setFont("MonoB", 24); c.setFillColorRGB(*CYAN)
q = "If your team runs multi-agent loops or RAG: what's your token spend per invocation — and are you tracking compression ratios at all?"
y = wrapped_text(q, M, y, "MonoB", 24, CYAN, W - 2*M, leading=32)

# save CTA
rule(130, color=DIM, w=1)
c.setFont("MonoB", 22); c.setFillColorRGB(*GOLD)
c.drawString(M, 94, "Save this. The four operations are free to codify in your own stack.")

footer(7)
c.showPage()


c.save()
print(f"wrote {OUT}")
