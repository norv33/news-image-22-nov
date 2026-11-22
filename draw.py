#!/usr/bin/env python3
"""Draw entry.png for 'The World - 22 November 2026' (make.fun news-image-20261122).

Original design: a dark-teal "evening atlas" poster. One wide lead panel for
the Gulf escalation, then five horizontal story rows, each with a hand-drawn
pictogram built from PIL primitives, a short headline, one fact line and a
region tag. No images from the internet, no copied artwork.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (12, 43, 51)          # deep teal
PANEL = (19, 65, 74)       # lighter teal panel
PANEL2 = (15, 55, 63)      # alternating row panel
GOLD = (232, 184, 75)      # gold accent
CREAM = (245, 239, 224)    # headline text
MUTED = (159, 184, 188)    # secondary text
INK = (12, 43, 51)         # dark text on chips

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
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


def text_block(d, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        d.text((x, y + i * leading), line, font=fnt, fill=fill)
    return y + len(lines) * leading


def starburst(d, cx, cy, r_out, r_in, points, fill):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def draw_ship(d, cx, cy, s, hull, deck):
    """Small cargo ship, centred at (cx, cy), scale s (half-width)."""
    # hull: trapezoid
    d.polygon([(cx - s, cy), (cx + s, cy), (cx + s * 0.78, cy + s * 0.42),
               (cx - s * 0.78, cy + s * 0.42)], fill=hull)
    # containers
    d.rectangle([cx - s * 0.55, cy - s * 0.55, cx - s * 0.05, cy - s * 0.05], fill=deck)
    d.rectangle([cx + s * 0.02, cy - s * 0.62, cx + s * 0.5, cy - s * 0.05], fill=deck)
    # bridge tower
    d.rectangle([cx + s * 0.55, cy - s * 0.75, cx + s * 0.85, cy - s * 0.05], fill=CREAM)
    # waves
    for k, wy in enumerate((cy + s * 0.62, cy + s * 0.82)):
        d.arc([cx - s * 1.05, wy - 8, cx - s * 0.15, wy + 8], 0, 180, fill=(79, 163, 209), width=3)
        d.arc([cx + s * 0.05, wy - 8, cx + s * 0.95, wy + 8], 0, 180, fill=(79, 163, 209), width=3)


def draw_drone(d, cx, cy, s, fill):
    d.ellipse([cx - s * 0.22, cy - s * 0.16, cx + s * 0.22, cy + s * 0.16], fill=fill)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        d.line([cx, cy, cx + dx * s * 0.7, cy + dy * s * 0.55], fill=fill, width=3)
        d.ellipse([cx + dx * s * 0.7 - s * 0.3, cy + dy * s * 0.55 - 3,
                   cx + dx * s * 0.7 + s * 0.3, cy + dy * s * 0.55 + 3], fill=fill)


def pictogram(d, kind, cx, cy, s):
    """Draw one story pictogram centred at (cx, cy), roughly s px radius."""
    if kind == "gulf":
        draw_ship(d, cx - s * 0.1, cy + s * 0.25, s * 0.62, (228, 87, 46), GOLD)
        starburst(d, cx + s * 0.55, cy - s * 0.55, s * 0.5, s * 0.24, 8, (255, 176, 32))
        starburst(d, cx + s * 0.55, cy - s * 0.55, s * 0.26, s * 0.12, 8, (255, 240, 180))
    elif kind == "baltic":
        draw_ship(d, cx - s * 0.05, cy + s * 0.35, s * 0.68, (79, 163, 209), CREAM)
        # quadcopter drone, top right, with spinning rotors
        dx, dy = cx + s * 0.55, cy - s * 0.5
        d.rectangle([dx - 9, dy - 6, dx + 9, dy + 6], fill=GOLD)
        for ox, oy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            d.line([dx, dy, dx + ox * 20, dy + oy * 14], fill=GOLD, width=3)
            d.ellipse([dx + ox * 20 - 11, dy + oy * 14 - 3,
                       dx + ox * 20 + 11, dy + oy * 14 + 3], fill=GOLD)
        d.line([dx - 8, dy + 12, cx + s * 0.1, cy - s * 0.05],
               fill=GOLD, width=2)
    elif kind == "cop":
        # globe: open circle with clear latitude/longitude lines
        gx, gy, gr = cx - s * 0.18, cy, s * 0.62
        d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr],
                  outline=(88, 179, 104), width=4)
        d.ellipse([gx - gr * 0.45, gy - gr, gx + gr * 0.45, gy + gr],
                  outline=(88, 179, 104), width=3)
        d.line([gx - gr, gy, gx + gr, gy], fill=(88, 179, 104), width=3)
        d.arc([gx - gr, gy - gr * 0.55, gx + gr, gy + gr * 0.55],
              0, 360, fill=(88, 179, 104), width=2)
        # thermometer
        tx = cx + s * 0.68
        d.rounded_rectangle([tx - 7, cy - s * 0.7, tx + 7, cy + s * 0.45],
                            radius=7, outline=CREAM, width=3)
        d.rounded_rectangle([tx - 4, cy - s * 0.15, tx + 4, cy + s * 0.42],
                            radius=4, fill=(228, 87, 46))
        d.ellipse([tx - 13, cy + s * 0.32, tx + 13, cy + s * 0.72],
                  fill=(228, 87, 46))
    elif kind == "fbi":
        # monitor with a keyhole and a crack
        d.rounded_rectangle([cx - s * 0.75, cy - s * 0.6, cx + s * 0.75, cy + s * 0.35],
                            radius=8, outline=CREAM, width=4)
        d.line([cx, cy + s * 0.35, cx, cy + s * 0.62], fill=CREAM, width=5)
        d.line([cx - s * 0.4, cy + s * 0.62, cx + s * 0.4, cy + s * 0.62],
               fill=CREAM, width=5)
        # keyhole
        d.ellipse([cx - 9, cy - s * 0.38, cx + 9, cy - s * 0.38 + 18], fill=GOLD)
        d.polygon([(cx - 6, cy - s * 0.38 + 12), (cx + 6, cy - s * 0.38 + 12),
                   (cx, cy + s * 0.12)], fill=GOLD)
        # crack
        d.line([cx + s * 0.45, cy - s * 0.6, cx + s * 0.3, cy - s * 0.25,
                cx + s * 0.5, cy + s * 0.05], fill=(228, 87, 46), width=3)
    elif kind == "sinaloa":
        # two linked handcuff rings, staggered, with a chain link between them
        d.ellipse([cx - s * 0.9, cy - s * 0.55, cx - s * 0.12, cy + s * 0.28],
                  outline=GOLD, width=6)
        d.ellipse([cx + s * 0.05, cy - s * 0.28, cx + s * 0.83, cy + s * 0.55],
                  outline=GOLD, width=6)
        d.ellipse([cx - 9, cy - s * 0.18, cx + 9, cy + s * 0.02],
                  outline=GOLD, width=3)
        starburst(d, cx + s * 0.55, cy - s * 0.62, s * 0.38, s * 0.18, 8, (228, 87, 46))
    elif kind == "bolsonaro":
        # hospital cross + heartbeat line
        d.rounded_rectangle([cx - s * 0.7, cy - s * 0.7, cx + s * 0.7, cy + s * 0.7],
                            radius=12, fill=(62, 193, 176))
        d.rectangle([cx - 10, cy - s * 0.45, cx + 10, cy + s * 0.45], fill=CREAM)
        d.rectangle([cx - s * 0.45, cy - 10, cx + s * 0.45, cy + 10], fill=CREAM)
        d.line([cx - s * 0.95, cy + s * 0.82, cx - s * 0.3, cy + s * 0.82,
                cx - s * 0.12, cy + s * 0.55, cx + s * 0.08, cy + s * 0.95,
                cx + s * 0.28, cy + s * 0.7, cx + s * 0.95, cy + s * 0.7],
               fill=(228, 87, 46), width=4)


STORIES = [
    dict(kind="gulf", tag="MIDDLE EAST", accent=(228, 87, 46),
         head="Gulf in flames: Iran strikes Bahrain; two tankers hit in Hormuz",
         fact="Bahrain says Iran hit a civilian industrial site, sparking a fire; "
              "a maritime agency reports two tankers struck in the Strait of Hormuz."),
    dict(kind="baltic", tag="EUROPE", accent=(79, 163, 209),
         head="Drones hit Russian cargo ship in the Baltic",
         fact="A Russian-bound cargo ship caught fire in the Gulf of Finland after "
              "a drone strike; Finland tightened security."),
    dict(kind="cop", tag="CLIMATE", accent=(88, 179, 104),
         head="COP31 deadlocked over fossil fuels",
         fact="Climate talks ran into overtime with no final deal, as negotiators "
              "failed to agree on fossil fuels and finance."),
    dict(kind="fbi", tag="UNITED STATES", accent=(155, 126, 222),
         head="FBI probes hack of its crime database",
         fact="The FBI is investigating an apparent intrusion into its National "
              "Crime Information Center database."),
    dict(kind="sinaloa", tag="MEXICO", accent=(242, 140, 40),
         head="Cartel violence erupts in Sinaloa; 11 killed",
         fact="Gunmen clashed across Sinaloa after the army captured FBI most-wanted "
              "drug lord \u201cEl Chapo Isidro\u201d."),
    dict(kind="bolsonaro", tag="BRAZIL", accent=(62, 193, 176),
         head="Bolsonaro in intensive care",
         fact="Brazil\u2019s jailed ex-president Jair Bolsonaro was admitted to ICU "
              "with an acute bowel obstruction."),
]

ALSO_TODAY = ("Hong Kong begins voting for its Election Committee  \u2022  "
              "Judge approves $7.25bn Roundup cancer settlement  \u2022  "
              "France protests enter a sixth weekend over living costs")


def chip(d, x, y, text, accent, fnt):
    w = fnt.getlength(text) + 22
    h = 30
    d.rounded_rectangle([x, y, x + w, y + h], radius=15, fill=accent)
    d.text((x + 11, y + 5), text, font=fnt, fill=INK)
    return w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    f_title = font(SANS_B, 62)
    f_date = font(SANS_B, 40)
    title = "THE WORLD"
    d.text(((W - f_title.getlength(title)) / 2, 14), title, font=f_title, fill=CREAM)
    d.line([60, 92, W - 60, 92], fill=GOLD, width=3)
    date = "SUNDAY, 22 NOVEMBER 2026"
    d.text(((W - f_date.getlength(date)) / 2, 102), date, font=f_date, fill=GOLD)
    d.line([60, 156, W - 60, 156], fill=GOLD, width=2)

    f_lead_head = font(SANS_B, 31)
    f_lead_fact = font(SANS, 20)
    f_tag = font(SANS_B, 16)
    f_head = font(SANS_B, 25)
    f_fact = font(SANS, 18)

    # --- lead panel (story 1) ---
    lead = STORIES[0]
    ly, lh = 168, 172
    d.rounded_rectangle([24, ly, W - 24, ly + lh], radius=14, fill=PANEL)
    d.rectangle([24, ly + 10, 34, ly + lh - 10], fill=lead["accent"])
    pictogram(d, lead["kind"], 118, ly + lh // 2, 62)
    tx = 210
    chip(d, W - 24 - 190, ly + 16, lead["tag"], lead["accent"], f_tag)
    head_lines = wrap(lead["head"], f_lead_head, 620)
    text_block(d, tx, ly + 18, head_lines, f_lead_head, CREAM, 36)
    fact_lines = wrap(lead["fact"], f_lead_fact, 740)
    text_block(d, tx, ly + 18 + len(head_lines) * 36 + 8,
               fact_lines, f_lead_fact, MUTED, 25)

    # --- five horizontal rows (stories 2-6) ---
    ry = 352
    rh, gap = 102, 10
    for i, st in enumerate(STORIES[1:]):
        y = ry + i * (rh + gap)
        fill = PANEL if i % 2 == 0 else PANEL2
        d.rounded_rectangle([24, y, W - 24, y + rh], radius=12, fill=fill)
        d.rectangle([24, y + 8, 32, y + rh - 8], fill=st["accent"])
        pictogram(d, st["kind"], 92, y + rh // 2, 38)
        tx = 150
        chip(d, W - 24 - 185, y + 13, st["tag"], st["accent"], f_tag)
        head_lines = wrap(st["head"], f_head, 660)
        text_block(d, tx, y + 14, head_lines, f_head, CREAM, 30)
        fact_lines = wrap(st["fact"], f_fact, 790)
        text_block(d, tx, y + 14 + len(head_lines) * 30 + 4,
                   fact_lines, f_fact, MUTED, 22)

    # --- also today strip ---
    ay = 912
    d.rounded_rectangle([24, ay, W - 24, ay + 56], radius=12, fill=(10, 36, 43))
    f_also_lab = font(SANS_B, 18)
    f_also = font(SANS, 17)
    d.text((44, ay + 17), "ALSO TODAY", font=f_also_lab, fill=GOLD)
    lab_w = f_also_lab.getlength("ALSO TODAY")
    also_lines = wrap(ALSO_TODAY, f_also, W - 24 - 44 - lab_w - 28 - 44)
    text_block(d, 44 + lab_w + 28, ay + 8, also_lines, f_also, CREAM, 21)

    # --- footer ---
    f_foot = font(SANS, 15)
    foot = ("Sources: BBC News \u00b7 AFP \u00b7 Reuters \u00b7 The Guardian \u00b7 "
            "The Times of India  \u2014  Drawn from reports of 22 November 2026")
    d.text(((W - f_foot.getlength(foot)) / 2, 984), foot, font=f_foot, fill=MUTED)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
