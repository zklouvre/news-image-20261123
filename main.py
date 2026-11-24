#!/usr/bin/env python3
"""Draw The Daily Globe - Monday 23 November 2026 (1024x1024, deterministic).

Renders /output/entry.png with PIL only: no network, no clock, no
randomness. Same input always produces byte-identical output.
Run: python3 main.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 14                      # outer margin
CW = W - 2 * M              # content width

PAPER = (247, 243, 232)
INK = (24, 24, 22)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (18, 110, 110)
GREY = (110, 106, 96)
LIGHT = (233, 227, 211)
SEA = (168, 196, 214)
LAND = (232, 220, 192)
LAND_LINE = (138, 122, 90)
GREEN = (27, 120, 60)

CHIP_COLORS = {"CONFIRMED": (27, 120, 60), "REPORTED": (31, 90, 160),
               "CLAIM": (176, 120, 10)}

FONT_DIR = "/usr/share/fonts/truetype/noto"


def _pick(bold, serif):
    """Preferred Noto face, DejaVu fallback if a file is missing."""
    if serif:
        name = "NotoSerif-Bold.ttf" if bold else "NotoSerif-Regular.ttf"
        alt = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" \
            if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    else:
        name = "NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf"
        alt = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" \
            if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    path = os.path.join(FONT_DIR, name)
    return path if os.path.exists(path) else alt


SERIF_B = _pick(True, True)
SERIF_R = _pick(False, True)
SANS_B = _pick(True, False)
SANS_R = _pick(False, False)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit in width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def trunc(draw, text, fnt, width):
    """Shorten text with an ellipsis so it fits on one line."""
    if draw.textlength(text, font=fnt) <= width:
        return text
    words = text.split()
    out = ""
    for w in words:
        trial = (out + " " + w).strip()
        if draw.textlength(trial + " \u2026", font=fnt) <= width:
            out = trial
        else:
            break
    return (out + " \u2026") if out else "\u2026"


def chip(draw, x, y, label, size=9):
    """Draw a small coloured tag; returns width used."""
    fnt = font(SANS_B, size)
    tw = draw.textlength(label, font=fnt)
    w = int(tw) + 8
    h = size + 6
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3,
                           fill=CHIP_COLORS[label])
    draw.text((x + 4, y + 2), label, font=fnt, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Monday 23 November 2026
# in at least one time zone. Sources were checked live on 24 Nov 2026
# (Reuters, UN, European Commission, US Treasury, NHS, ESA/JAXA, ICC,
# Al Jazeera, BBC, Investopedia, Principia day summary).
# Tags: CONFIRMED = verified by a primary source or wire;
#       REPORTED = reported by a named outlet, not yet independently verified;
#       CLAIM    = one party's claim, unverified.
# Regions (7): North America, South America, Europe, Africa, Middle East,
# Asia, Oceania.

LEADS = [
    {
        "n": 1, "field": "Climate", "region": "Europe",
        "kicker": "COP31 COLLAPSES",
        "headline": "COP31 ends without a deal as fossil-fuel split kills the Antalya pact",
        "body": ("Two weeks of talks and two days of overtime ended with no "
                 "overarching deal - the first collapse since Copenhagen in "
                 "2009. The EU and 130+ countries rejected a draft with no "
                 "fossil-fuel phase-out; Guterres was 'deeply disappointed'."),
        "chip": "CONFIRMED", "source": "UN / Reuters, 23 Nov",
        "pin": (37.5, 33.0), "art": "pact",
    },
    {
        "n": 2, "field": "War", "region": "Africa",
        "kicker": "THE WAR REACHES THE MED",
        "headline": "Ukrainian drone hits Russian warship at Benghazi; Zelensky confirms strike",
        "body": ("A Russian vessel exploded at Benghazi after a suspected "
                 "Ukrainian drone strike, which President Zelensky confirmed. "
                 "Eastern Libyan forces claimed the port as the ship burned "
                 "offshore, raising fears the war is spreading to the Med."),
        "chip": "CONFIRMED", "source": "Reuters, 23 Nov",
        "pin": (32.1, 20.07), "art": "harbour",
    },
    {
        "n": 3, "field": "Tech", "region": "North America",
        "kicker": "HUANG IS BACK",
        "headline": "Nvidia brings back Huang as CEO; shares jump 31%",
        "body": ("Eleven days after he resigned, the board unanimously "
                 "restored Huang as president, CEO and director, saying US "
                 "officials assured them his return posed no national-"
                 "security risk. The Nasdaq rose 6% on the news."),
        "chip": "CONFIRMED", "source": "Reuters, 23 Nov",
        "pin": (37.37, -121.96), "art": "chip",
    },
]

SMALL = [
    {"n": 4, "field": "Tech", "region": "North America",
     "headline": "US puts Megaspeed on trade blacklist over China chips",
     "chip": "CONFIRMED", "source": "Commerce Dept, 23 Nov", "pin": (2.5, 102.0)},
    {"n": 5, "field": "War", "region": "Europe",
     "headline": "Russian strikes kill at least 15 around Kyiv",
     "chip": "CONFIRMED", "source": "Ukraine officials, 23 Nov", "pin": (49.5, 33.5)},
    {"n": 6, "field": "Diplomacy", "region": "Europe",
     "headline": "EU proposes 22nd Russia sanctions: 60 banks off SWIFT",
     "chip": "CONFIRMED", "source": "European Commission, 23 Nov", "pin": (50.5, 4.5)},
    {"n": 7, "field": "Law", "region": "North America",
     "headline": "US sanctions 30 in Iran shadow-banking network",
     "chip": "CONFIRMED", "source": "US Treasury, 23 Nov", "pin": (38.9, -77.04)},
    {"n": 8, "field": "War", "region": "Europe",
     "headline": "Drone-hit Sparta II reaches St Petersburg under tow",
     "chip": "CONFIRMED", "source": "Reuters, 23 Nov", "pin": (61.5, 28.0)},
    {"n": 9, "field": "Disaster", "region": "Asia",
     "headline": "Sweets-factory fire in Banten kills 24; ~30 missing",
     "chip": "CONFIRMED", "source": "Reuters, 23 Nov", "pin": (-7.5, 108.0)},
    {"n": 10, "field": "Markets", "region": "Asia",
     "headline": "Asian markets slide: Nikkei -5.06%, KOSPI -3.5%",
     "chip": "CONFIRMED", "source": "Reuters, 23 Nov", "pin": (35.68, 139.69)},
    {"n": 11, "field": "Health", "region": "Europe",
     "headline": "NHS trials AI in breast-cancer screening",
     "chip": "CONFIRMED", "source": "NHS, 23 Nov", "pin": (53.5, -3.5)},
    {"n": 12, "field": "Science", "region": "Europe",
     "headline": "BepiColombo enters Mercury orbit after 8-year trip",
     "chip": "CONFIRMED", "source": "ESA/JAXA, 23 Nov", "pin": (48.5, 10.5)},
    {"n": 13, "field": "Diplomacy", "region": "Africa",
     "headline": "Kenya and DR Congo restore ambassador ties",
     "chip": "CONFIRMED", "source": "Ruto, 23 Nov", "pin": (-1.29, 36.82)},
    {"n": 14, "field": "Politics", "region": "South America",
     "headline": "Brazil lower house backs Lula fiscal bill 353-128",
     "chip": "REPORTED", "source": "Rio Times, 23 Nov", "pin": (-15.79, -47.88)},
    {"n": 15, "field": "Sport", "region": "Oceania",
     "headline": "NZ-India Test drawn; Australia up to 2nd in WTC",
     "chip": "CONFIRMED", "source": "ICC, 23 Nov", "pin": (-41.29, 174.78)},
]

NUMBERED = [
    (16, "FBI probes possible hack of crime database", "REPORTED", "FBI, 23 Nov", "Crime", "North America"),
    (17, "US intel tracked Alice Huang's alleged spy contacts", "REPORTED", "NYT, 23 Nov", "Tech", "North America"),
    (18, "Wall Street soars: Nasdaq +6.5%, S&P +4.7%, Dow +1,450", "CONFIRMED", "Investopedia, 23 Nov", "Markets", "North America"),
    (19, "US extradition order exists for 'El Chapo Isidro'", "CONFIRMED", "Reuters, 23 Nov", "Crime", "North America"),
    (20, "Euro-area inflation rises to 4.0%", "CONFIRMED", "Eurostat, 23 Nov", "Markets", "Europe"),
    (21, "UK voters name rising prices top concern amid Iran war", "REPORTED", "UK polling, 23 Nov", "Politics", "Europe"),
    (22, "Ukrainians face another winter without power", "REPORTED", "Reuters, 23 Nov", "War", "Europe"),
    (23, "Drone strikes hit homes and a UN building in Khartoum", "REPORTED", "OkayAfrica, 23 Nov", "War", "Africa"),
    (24, "Boat capsizes in Nigeria's Bayelsa; 24+ mourners dead", "REPORTED", "Bayelsa reports, 23 Nov", "Disaster", "Africa"),
    (25, "African energy exporters gained extra $21.6bn in Iran war", "REPORTED", "CREA, 23 Nov", "Markets", "Africa"),
    (26, "Israeli strikes kill 3+ in Gaza, incl. UNRWA worker", "REPORTED", "Gaza reports, 23 Nov", "War", "Middle East"),
    (27, "Israeli opposition calls settler attacks 'Jewish terrorism'", "REPORTED", "Reuters, 23 Nov", "Politics", "Middle East"),
    (28, "Israeli army pulls back from Lebanese village in pilot", "REPORTED", "Reuters, 23 Nov", "War", "Middle East"),
    (29, "UN: Gaza war erased decades of human development", "REPORTED", "UN, 23 Nov", "Aid", "Middle East"),
    (30, "Anthropic says AI helped prove Riemann hypothesis", "CLAIM", "Anthropic claim, 23 Nov", "Science", "North America"),
    (31, "Tata Steel to buy $1.67bn stake in APL Apollo", "REPORTED", "Reports, 23 Nov", "Markets", "Asia"),
    (32, "Australian shares set to slide at open; NZ falls", "REPORTED", "Reuters, 23 Nov", "Markets", "Oceania"),
    (33, "Paraguay detains ex-president's brother in Ueno Bank case", "REPORTED", "Rio Times, 23 Nov", "Crime", "South America"),
    (34, "Chile stocks +0.96% as peso steadies", "REPORTED", "Rio Times, 23 Nov", "Markets", "South America"),
    (35, "Zambia opposition leader charged with treason", "REPORTED", "OkayAfrica, 23 Nov", "Politics", "Africa"),
    (36, "15 APC supporters killed in Zamfara road crash", "REPORTED", "Punch, 23 Nov", "Disaster", "Africa"),
]

# UTC timeline: six moments across the whole day, each with a sourced time.
TIMELINE = [
    ("01:23", "Nikkei -5.06%; Asia slides"),
    ("09:05", "Asian governments step in"),
    ("12:35", "Israeli fire kills Palestinian"),
    ("15:37", "EU proposes 22nd sanctions"),
    ("21:25", "US blacklists Megaspeed"),
    ("23:41", "15 killed in Zamfara road crash"),
]

# Older stories deliberately LEFT OUT of the 36 - a careless page would
# include them. All of these happened before 23 November 2026.
DATE_CHECK = [
    ("Sparta II hit by drones in Gulf of Finland", "21 Nov"),
    ("'El Chapo Isidro' captured in Sinaloa gunbattle", "20 Nov"),
    ("Boca Juniors win Copa Sudamericana", "21 Nov"),
    ("EU and Indonesia sign trade deal", "22 Nov"),
    ("Bolsonaro 'stable' in intensive care", "21 Nov"),
    ("M6.8 quake shakes Peru's Junin region", "21 Nov"),
    ("Nvidia faces SEC accounting inquiry", "22 Nov"),
    ("Philippines and Chile sign free trade deal", "22 Nov"),
]

# Simplified continent outlines (lon, lat) for the drawn world map.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
     (-60, 47), (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-92, 15),
     (-97, 16), (-105, 20), (-110, 24), (-117, 33), (-125, 40), (-125, 49),
     (-135, 58), (-155, 58), (-168, 66)],
    # South America
    [(-78, 7), (-72, 11), (-60, 8), (-52, 5), (-42, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52),
     (-73, -50), (-73, -37), (-70, -20), (-80, -5), (-81, 2), (-78, 7)],
    # Africa
    [(-17, 15), (-16, 21), (-10, 31), (0, 36), (10, 37), (20, 32),
     (32, 31), (35, 28), (43, 12), (51, 11), (48, 2), (41, -2),
     (40, -10), (36, -18), (33, -26), (26, -34), (19, -35), (15, -27),
     (12, -18), (9, -1), (-8, 5), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (2, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
     (30, 70), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50),
     (28, 45), (23, 40), (19, 42), (12, 44), (8, 38), (3, 38),
     (-2, 37), (-10, 36)],
    # Asia (incl. Middle East, India, SE Asia, China, Siberia)
    [(30, 36), (36, 36), (44, 39), (48, 30), (52, 26), (57, 25), (61, 25),
     (66, 25), (72, 20), (77, 8), (80, 7), (85, 19), (89, 22), (92, 16),
     (98, 8), (100, 6), (104, 2), (107, 11), (109, 14), (106, 20),
     (110, 22), (114, 22), (118, 25), (121, 28), (122, 32), (120, 35),
     (122, 38), (127, 40), (130, 42), (135, 44), (138, 46), (142, 50),
     (142, 59), (158, 60), (162, 62), (170, 66), (178, 65), (170, 70),
     (160, 70), (140, 72), (120, 73), (100, 77), (80, 73), (68, 70),
     (60, 69), (55, 68), (50, 68), (45, 68), (40, 68), (35, 66),
     (32, 66), (30, 62), (28, 58), (25, 55), (22, 50), (20, 46),
     (25, 42), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (136, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (153, -24), (150, -22), (146, -19), (142, -11), (137, -12), (132, -12),
     (126, -14), (122, -17), (118, -20), (113, -22)],
]


# ------------------------------------------------------------------- art
def draw_pact(draw, x, y, w, h):
    """COP31: a conference hall, flags, and a pact paper stamped NO DEAL."""
    draw.rectangle([x, y, x + w, y + h], fill=(207, 227, 238))
    # hall wall + long table
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 110, 95))
    draw.rectangle([x + 14, y + h - 40, x + w - 14, y + h - 26],
                   fill=(70, 60, 55))
    # row of small flags along the back wall
    flag_cols = [(31, 58, 95), (176, 30, 36), (18, 110, 110), (200, 160, 40),
                 (27, 120, 60), (120, 60, 140), (200, 90, 30), (31, 90, 160)]
    for i, col in enumerate(flag_cols):
        fx = x + 12 + i * 40
        draw.rectangle([fx, y + 10, fx + 28, y + 30], fill=col)
        draw.rectangle([fx + 12, y + 30, fx + 15, y + h - 40], fill=(60, 55, 50))
    # the pact paper, centre, with a red cross through it
    px, py, pw, ph = x + w // 2 - 52, y + 8, 104, 52
    draw.rectangle([px, py, px + pw, py + ph], fill=(250, 250, 248),
                   outline=(90, 84, 70))
    for i in range(4):
        draw.line([(px + 10, py + 10 + i * 10), (px + pw - 10, py + 10 + i * 10)],
                  fill=(150, 146, 136), width=2)
    draw.line([(px + 6, py + 6), (px + pw - 6, py + ph - 6)], fill=RED, width=4)
    draw.line([(px + pw - 6, py + 6), (px + 6, py + ph - 6)], fill=RED, width=4)


def draw_harbour(draw, x, y, w, h):
    """Benghazi: harbour water, a burning ship, smoke, one drone arc."""
    draw.rectangle([x, y, x + w, y + h], fill=(207, 227, 238))
    sea_y = y + int(h * 0.55)
    draw.rectangle([x, sea_y, x + w, y + h], fill=(47, 111, 159))
    draw.rectangle([x, sea_y, x + w, sea_y + 3], fill=(120, 170, 200))
    # harbour wall, left
    draw.rectangle([x, y + h - 30, x + 70, y + h], fill=(120, 110, 95))
    # ship hull + superstructure, centre-right
    hx = x + 110
    draw.polygon([(hx, sea_y + 8), (hx + 150, sea_y + 8), (hx + 138, sea_y + 26),
                  (hx + 12, sea_y + 26)], fill=(30, 32, 38))
    draw.rectangle([hx + 52, sea_y - 12, hx + 98, sea_y + 8], fill=(200, 200, 195))
    draw.rectangle([hx + 62, sea_y - 22, hx + 72, sea_y - 12], fill=(176, 30, 36))
    # flames on deck
    for fx, fh in ((hx + 30, 16), (hx + 58, 22), (hx + 92, 14), (hx + 118, 18)):
        draw.polygon([(fx, sea_y - 2), (fx + 7, sea_y - fh), (fx + 14, sea_y - 2)],
                     fill=(240, 140, 30))
    # smoke puffs
    for sx, sy, sr in ((hx + 60, sea_y - 34, 9), (hx + 78, sea_y - 46, 12),
                       (hx + 100, sea_y - 58, 10)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(90, 88, 84))
    # drone arc (red dots) from upper left to the ship
    for t in range(0, 11):
        if t % 2 == 0:
            continue
        px = 30 + (150 - 30) * t / 10.0
        py = 34 - 22 * (t / 10.0) * (1 - t / 10.0) * 4 - (t / 10.0) * 10
        draw.ellipse([x + px - 2, y + py - 2, x + px + 2, y + py + 2],
                     fill=RED)


def draw_chip(draw, x, y, w, h):
    """Nvidia: a chip on dark navy, a green arrow shooting up, +31%."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    # faint grid
    for gx in range(x + 20, x + w, 40):
        draw.line([(gx, y), (gx, y + h)], fill=(40, 52, 84), width=1)
    # chip, left
    cx, cy, cw, ch = x + 26, y + 16, 74, 74
    for i in range(4):
        draw.line([(cx + 12 + i * 18, cy - 8), (cx + 12 + i * 18, cy)],
                  fill=(180, 190, 200), width=3)
        draw.line([(cx + 12 + i * 18, cy + ch), (cx + 12 + i * 18, cy + ch + 8)],
                  fill=(180, 190, 200), width=3)
    draw.rectangle([cx, cy, cx + cw, cy + ch], fill=(46, 160, 90),
                   outline=(220, 230, 220), width=2)
    draw.rectangle([cx + 22, cy + 22, cx + cw - 22, cy + ch - 22],
                   fill=(24, 32, 54))
    draw.text((cx + 30, cy + 28), "NV", font=font(SANS_B, 16),
              fill=(255, 255, 255))
    # rising arrow, right of the chip
    ax, ay = x + 130, y + h - 22
    draw.line([(ax, ay), (ax + 62, ay - 26), (ax + 118, ay - 58)],
              fill=(46, 200, 110), width=4)
    draw.polygon([(ax + 118, ay - 58), (ax + 100, ay - 56), (ax + 114, ay - 40)],
                 fill=(46, 200, 110))
    draw.text((x + w - 92, y + 10), "+31%", font=font(SANS_B, 26),
              fill=(46, 200, 110))


ART = {"pact": draw_pact, "harbour": draw_harbour, "chip": draw_chip}


def draw_map(draw, x, y, w, h, pins):
    """Stylised equirectangular world map with numbered pins."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    for lon in range(-150, 181, 30):
        gx = x + (lon + 180) / 360.0 * w
        draw.line([(gx, y), (gx, y + h)], fill=(140, 170, 190), width=1)
    for lat in (-30, 0, 30, 60):
        gy = y + (84 - lat) / 142.0 * h
        draw.line([(x, gy), (x + w, gy)], fill=(140, 170, 190), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360.0 * w, y + (84 - lat) / 142.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_LINE)
    draw.text((x + 6, y + 4), "WHERE IT HAPPENED \u2014 15 PINNED STORIES",
              font=font(SANS_B, 10), fill=NAVY)
    for n, (lat, lon) in pins:
        px, py = proj(lon, lat)
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        fnt = font(SANS_B, 9 if n < 10 else 8)
        tw = draw.textlength(str(n), font=fnt)
        draw.text((px - tw / 2, py - 6), str(n), font=fnt, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # ---- Masthead ----
    d.text((M, y), "THE DAILY GLOBE", font=font(SERIF_B, 46), fill=INK)
    d.text((W - M, y + 2), "MONDAY", font=font(SANS_B, 19), fill=RED, anchor="ra")
    d.text((W - M, y + 26), "23 NOVEMBER 2026", font=font(SANS_B, 22),
           fill=INK, anchor="ra")
    d.text((W - M, y + 52), "ONE DAY  \u00b7  ONE PAGE", font=font(SANS_B, 10),
           fill=GREY, anchor="ra")
    y = 84
    d.line([(M, y), (W - M, y)], fill=RED, width=3)
    y += 8
    # ---- Lead-story teasers (winner #1 style) ----
    d.text((M, y), "COP31 ENDS WITHOUT A DEAL  \u2022  UKRAINIAN DRONE HITS RUSSIAN WARSHIP AT BENGHAZI",
           font=font(SANS_B, 12), fill=RED)
    y += 16
    d.text((M, y), "NVIDIA BRINGS BACK HUANG AS CEO \u2014 SHARES +31%",
           font=font(SANS_B, 12), fill=RED)
    y += 22
    d.text((M, y), "36 STORIES  \u2022  7 REGIONS  \u2022  13 FIELDS  \u2022  EVERY STORY HAPPENED OR WAS FIRST REPORTED ON 23 NOVEMBER 2026",
           font=font(SANS_B, 11), fill=NAVY)
    y += 20

    # ---- UTC timeline (full day) ----
    d.text((M, y), "UTC TIMELINE \u2014 THE DAY, HOUR BY HOUR",
           font=font(SANS_B, 11), fill=RED)
    y += 16
    cell = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = M + i * cell
        d.line([(cx + cell / 2, y + 2), (cx + cell / 2, y + 8)], fill=RED, width=2)
        d.text((cx + 4, y + 10), t, font=font(SANS_B, 11), fill=RED)
        d.text((cx + 4, y + 24),
               trunc(d, txt, font(SANS_R, 10), cell - 8),
               font=font(SANS_R, 10), fill=INK)
    y += 42

    # ---- By-field bar ----
    fields = {}
    for s in LEADS + SMALL:
        fields[s["field"]] = fields.get(s["field"], 0) + 1
    for _n, _h, _c, _s, f, _r in NUMBERED:
        fields[f] = fields.get(f, 0) + 1
    order = sorted(fields.items(), key=lambda kv: (-kv[1], kv[0]))
    top = ["%s %d" % (k.upper(), v) for k, v in order if v >= 3]
    rest = sum(1 for _k, v in order if v < 3)
    bar = "BY FIELD   " + "  \u2022  ".join(top) + "  \u2022  +%d MORE AT 2 OR FEWER" % rest
    d.text((M, y), bar, font=font(SANS_B, 10), fill=INK)
    y += 18

    # ---- Three illustrated leads ----
    col_w = (CW - 16) // 3
    for i, lead in enumerate(LEADS):
        lx = M + i * (col_w + 8)
        ART[lead["art"]](d, lx, y, col_w, 88)
        ty = y + 94
        d.text((lx, ty), lead["kicker"], font=font(SANS_B, 10), fill=RED)
        ty += 14
        for ln in wrap(d, lead["headline"], font(SANS_B, 17), col_w):
            d.text((lx, ty), ln, font=font(SANS_B, 17), fill=INK)
            ty += 19
        ty += 2
        for ln in wrap(d, lead["body"], font(SANS_R, 11), col_w)[:5]:
            d.text((lx, ty), ln, font=font(SANS_R, 11), fill=(40, 40, 38))
            ty += 13
        ty += 3
        cw = chip(d, lx, ty, lead["chip"])
        d.text((lx + cw + 6, ty + 1), lead["source"], font=font(SANS_R, 9),
               fill=GREY)
    y += 88 + 6 + 14 + 38 + 2 + 65 + 3 + 15 + 8

    # ---- 12 small stories: 4 cols x 3 rows ----
    scw = (CW - 24) // 4
    for i, s in enumerate(SMALL):
        r, c = divmod(i, 4)
        sx = M + c * (scw + 8)
        sy = y + r * 58
        d.text((sx, sy), "%d." % s["n"], font=font(SANS_B, 12), fill=RED)
        lines = wrap(d, s["headline"], font(SANS_B, 12.5), scw - 20)
        ly = sy
        for ln in lines[:2]:
            d.text((sx + 18, ly), ln, font=font(SANS_B, 12.5), fill=INK)
            ly += 15
        cw = chip(d, sx + 18, ly + 1, s["chip"], size=8)
        d.text((sx + 18 + cw + 5, ly + 2), s["source"], font=font(SANS_R, 8.5),
               fill=GREY)
        if c < 3:
            d.line([(sx + scw + 4, sy), (sx + scw + 4, sy + 52)], fill=LIGHT, width=1)
    y += 3 * 58 + 8

    # ---- World map (left) + DATE CHECK (right) ----
    map_w = 620
    pins = [(s["n"], s["pin"]) for s in LEADS + SMALL]
    draw_map(d, M, y, map_w, 184, pins)
    dx = M + map_w + 8
    dw = W - M - dx
    d.rectangle([dx, y, dx + dw, y + 184], outline=RED, width=2)
    d.rectangle([dx, y, dx + dw, y + 26], fill=RED)
    d.text((dx + 8, y + 5), "DATE CHECK \u2014 LEFT OUT AS OLDER NEWS",
           font=font(SANS_B, 12), fill=(255, 255, 255))
    dy = y + 32
    for story, when in DATE_CHECK:
        d.text((dx + 8, dy), "\u2715", font=font(SANS_B, 11), fill=RED)
        d.text((dx + 22, dy),
               trunc(d, "%s \u2014 %s" % (story, when),
                     font(SANS_B, 11), dw - 30),
               font=font(SANS_B, 11), fill=INK)
        dy += 17
    y += 184 + 8

    # ---- Numbered list: 21 more stories, 3 columns x 7 ----
    d.text((M, y), "THE REST OF THE DAY \u2014 21 MORE STORIES",
           font=font(SANS_B, 14), fill=NAVY)
    d.line([(M, y + 20), (W - M, y + 20)], fill=NAVY, width=1)
    y += 26
    ncw = (CW - 16) // 3
    for i, (n, headline, _chip, source, _f, _r) in enumerate(NUMBERED):
        col, row = divmod(i, 7)
        nx = M + col * (ncw + 8)
        ny = y + row * 16
        d.text((nx, ny), "%d." % n, font=font(SANS_B, 10.5), fill=RED)
        txt = trunc(d, "%s \u2014 %s" % (headline, source),
                    font(SANS_R, 10.5), ncw - 26)
        d.text((nx + 24, ny), txt, font=font(SANS_R, 10.5), fill=INK)
    y += 7 * 16 + 8

    # ---- Footer ----
    fy = H - 20
    d.line([(M, fy - 4), (W - M, fy - 4)], fill=GREY, width=1)
    d.text((M, fy), "Sources: Reuters \u2022 UN \u2022 European Commission \u2022 US Treasury \u2022 NHS \u2022 ESA/JAXA \u2022 ICC \u2022 Al Jazeera \u2022 BBC \u2022 Investopedia  \u2014  Built by an AI agent for make.fun's news-image-20261123 bounty.",
           font=font(SANS_R, 9.5), fill=GREY)

    print("layout bottom y =", y, " (canvas H =", H, ")")
    out_dir = "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "entry.png")
        img.save(out, "PNG", optimize=True)
    except OSError:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "entry.png")
        img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
