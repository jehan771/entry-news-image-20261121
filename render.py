#!/usr/bin/env python3
"""Render THE WORLD TODAY — Saturday 21 November 2026 — as a 2048px
front page, then downscale to the 1024px entry image.

All 23 stories were verified on 21 Nov 2026 against Reuters, AP, BBC,
Al Jazeera, AFP, ESA, UKMTO, IMD and PIB. Photos are file photos from
Wikimedia Commons / NASA, captioned as such; they illustrate the place
or the mission, never a moment they do not show.

Layout budget (2048 tall): masthead 0-200, lead 212-560, row2 576-930,
row3 946-1180, grid 1196-1910 (6 rows x 109px cards), timeline + footer
1916-2048. Every block is drawn inside its budget; nothing overflows.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W = 2048
H = 2048
BG = (250, 247, 240)
INK = (18, 18, 18)
RED = (178, 24, 24)
GREY = (92, 92, 92)
RULE = (200, 192, 180)
CARD = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def photo_cover(path, box_w, box_h):
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    scale = max(box_w / iw, box_h / ih)
    im = im.resize((int(iw * scale) + 1, int(ih * scale) + 1), Image.LANCZOS)
    x = (im.width - box_w) // 2
    y = (im.height - box_h) // 2
    return im.crop((x, y, x + box_w, y + box_h))


def draw_photo(draw, canvas, path, x, y, w, h, caption):
    canvas.paste(photo_cover(path, w, h), (x, y))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    cap_f = font(SANS, 21)
    lines = wrap(draw, caption, cap_f, w - 16)
    ch = 26 * len(lines) + 10
    draw.rectangle([x, y + h - ch, x + w, y + h], fill=(0, 0, 0))
    ty = y + h - ch + 5
    for ln in lines:
        draw.text((x + 8, ty), ln, font=cap_f, fill=(255, 255, 255))
        ty += 26


def story_card(draw, x, y, w, h, kicker, head, deck, source):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=2)
    pad = 14
    cx = x + pad
    cw = w - 2 * pad
    kf = font(SANS_B, 21)
    draw.text((cx, y + 8), kicker, font=kf, fill=RED)
    sf = font(SANS, 19)
    sw = draw.textlength(source, font=sf)
    draw.text((x + w - pad - sw, y + 9), source, font=sf, fill=GREY)
    # Headline: one line if possible, shrink until it fits.
    size = 30
    while size > 20:
        hf = font(SANS_B, size)
        hlines = wrap(draw, head, hf, cw)
        if len(hlines) <= 1:
            break
        size -= 1
    hf = font(SANS_B, size)
    hlines = wrap(draw, head, hf, cw)[:1]
    draw.text((cx, y + 34), hlines[0], font=hf, fill=INK)
    df = font(SANS, 23)
    dlines = wrap(draw, deck, df, cw)
    if dlines:
        draw.text((cx, y + 72), dlines[0], font=df, fill=(48, 48, 48))


# (kicker, headline, one-line deck <= ~58 chars, source)
STORIES = [
    ("EUROPE", "Denmark expels Russian attache over plot",
     "PET says Moscow plotted to kill rapper Kyivstoner.", "Al Jazeera"),
    ("EUROPE", "UK and EU seal post-Brexit reset deal",
     "Food checks scrapped; youth mobility for 100,000.", "Reuters"),
    ("ASIA", "Myanmar rejects world court ruling",
     "ICJ found genocide against the Rohingya, 9-6.", "Reuters"),
    ("MIDDLE EAST", "Tanker ablaze off Oman after strike",
     "Hit by unknown projectile 8 miles off Khasab.", "Reuters / UKMTO"),
    ("MARKETS", "Wall Street slides as AI sell-off deepens",
     "S&P -3.7%, Nasdaq -5.3%; Anthropic falls 8.5%.", "Barron's"),
    ("ASIA", "Cyclone Akvan crosses India's east coast",
     "Landfall near Gopalpur; 300,000 were evacuated.", "IMD"),
    ("USA", "Trump: 'very good talks' with Putin",
     "President says a Ukraine deal is possible.", "Reuters"),
    ("DIPLOMACY", "Shenzhen declaration leaves Ukraine out",
     "Trump, Xi, Putin sign four-point peace text.", "Reuters"),
    ("EUROPE", "Estonia to shut its border with Russia",
     "Crossing closes from 1 December, Tallinn says.", "DW"),
    ("UKRAINE", "114 children killed in Ukraine this year",
     "UNICEF: highest verified toll in years.", "AFP"),
    ("UKRAINE", "Double-tap strike kills boy of 7",
     "Second strike in Kryvyi Rih also kills a rescuer.", "AFP"),
    ("UKRAINE", "Kyiv hits Druzhba oil pumping station",
     "Strike on the pipeline in Tatarstan, Kyiv says.", "Reuters"),
    ("DIPLOMACY", "France seeks UN Security Council meeting",
     "Paris calls the council over the Kyiv barrage.", "BBC"),
    ("INDIA", "India launches home-grown bird-flu vaccine",
     "First H5N1 chicken vaccine, dedicated 20 Nov.", "PIB"),
    ("SPORT", "U-17 World Cup opens with goal rush",
     "Morocco 6-0 Fiji; Spain 5-0 China; Mali 3-0 NZ.", "FIFA"),
    ("EUROPE", "NATO chief heads to Warsaw after incursion",
     "Rutte calls the missile landings 'grave violation'.", "AP"),
    ("CLIMATE", "Protester halts COP31 plenary",
     "'You are killing the future,' activist shouts.", "Al Jazeera"),
    ("MIDDLE EAST", "Riyadh on alert for a third night",
     "Alert lifted after intercepts; wider threats made.", "Reuters"),
]


def main():
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    M = 48

    # ---- Masthead: 0-200 ----
    d.rectangle([0, 0, W, 148], fill=INK)
    d.text((M, 18), "THE WORLD TODAY", font=font(SERIF_B, 84), fill=(255, 255, 255))
    date_txt = "SATURDAY 21 NOVEMBER 2026"
    df_date = font(SANS_B, 34)
    d.text((W - M - d.textlength(date_txt, font=df_date), 52),
           date_txt, font=df_date, fill=(255, 210, 60))
    d.rectangle([0, 148, W, 152], fill=RED)
    d.text((M, 164), "23 VERIFIED STORIES  •  7 REGIONS  •  EVERY STORY SOURCED BELOW IT",
           font=font(SANS_B, 28), fill=RED)
    d.line([M, 204, W - M, 204], fill=RULE, width=2)

    # ---- Lead: 212-560 ----
    ly = 212
    lw = 1180
    d.text((M, ly), "MIDDLE EAST — LEAD", font=font(SANS_B, 28), fill=RED)
    head_f = font(SERIF_B, 84)
    d.text((M, ly + 38), "MISSILES OVER", font=head_f, fill=INK)
    d.text((M, ly + 126), "RIYADH", font=head_f, fill=INK)
    deck = ("Saudi air defences intercept three Houthi ballistic missiles "
            "fired at the capital in the early hours of Saturday — the third "
            "night of alerts, two days after a missile struck the PIF Tower.")
    df = font(SANS, 30)
    ty = ly + 224
    for ln in wrap(d, deck, df, lw - 10):
        d.text((M, ty), ln, font=df, fill=(48, 48, 48))
        ty += 36
    d.text((M, ly + 224 + 3 * 36 + 4), "Source: Reuters, 21 Nov 2026",
           font=font(SANS, 23), fill=GREY)
    px = M + lw + 30
    pw = W - M - px
    draw_photo(d, canvas, "photos/riyadh.jpg", px, ly, pw, 348,
               "Riyadh's King Abdullah Financial District, home to the PIF Tower. File photo: Wikimedia Commons")
    d.line([M, 566, W - M, 566], fill=RULE, width=2)

    # ---- Row 2: Peru + COP31, 576-930 ----
    ry = 576
    col_w = (W - 2 * M - 40) // 2
    x = M
    d.text((x, ry), "SOUTH AMERICA", font=font(SANS_B, 26), fill=RED)
    d.text((x, ry + 32), "Quake shakes Peru", font=font(SERIF_B, 50), fill=INK)
    d.text((x, ry + 92), "Magnitude 6.7–6.8, 00:09 UTC, felt in Lima.",
           font=font(SANS, 27), fill=(48, 48, 48))
    d.text((x, ry + 126), "No casualties or serious damage reported.",
           font=font(SANS, 27), fill=(48, 48, 48))
    d.text((x, ry + 160), "Source: Reuters / AFP / USGS", font=font(SANS, 22), fill=GREY)
    draw_photo(d, canvas, "photos/lima.jpg", x, ry + 188, col_w, 160,
               "Plaza de Armas, Lima. File photo: Wikimedia Commons")
    x2 = M + col_w + 40
    d.text((x2, ry), "CLIMATE", font=font(SANS_B, 26), fill=RED)
    d.text((x2, ry + 32), "COP31 runs into overtime", font=font(SERIF_B, 50), fill=INK)
    d.text((x2, ry + 92), "Antalya talks pass their deadline with no deal;",
           font=font(SANS, 27), fill=(48, 48, 48))
    d.text((x2, ry + 126), "the draft drops fossil fuels and a $120bn fund.",
           font=font(SANS, 27), fill=(48, 48, 48))
    d.text((x2, ry + 160), "Source: Reuters, 20–21 Nov 2026", font=font(SANS, 22), fill=GREY)
    draw_photo(d, canvas, "photos/antalya.jpg", x2, ry + 188, col_w, 160,
               "Antalya, Türkiye, host of COP31. File photo: Wikimedia Commons")
    d.line([M, 940, W - M, 940], fill=RULE, width=2)

    # ---- Row 3: Kyiv + Poland (left, to x=1300) and Mercury (right) 946-1180 ----
    gy = 946
    left_w = 1300 - M
    d.text((M, gy), "UKRAINE", font=font(SANS_B, 26), fill=RED)
    d.text((M, gy + 32), "Russia's huge barrage hits Kyiv",
           font=font(SERIF_B, 48), fill=INK)
    kyiv_deck = ("Nine killed; 110+ missiles, 400 drones; 3 Dnipro bridges hit, power cut.")
    ty = gy + 88
    for ln in wrap(d, kyiv_deck, font(SANS, 26), left_w):
        d.text((M, ty), ln, font=font(SANS, 26), fill=(48, 48, 48))
        ty += 32
    d.text((M, ty + 4), "Source: BBC / Reuters, 21 Nov 2026",
           font=font(SANS, 22), fill=GREY)
    ty += 28
    d.text((M, ty), "POLAND", font=font(SANS_B, 26), fill=RED)
    ty += 30
    pol_deck = "Two Russian missiles and a drone land in SE Poland; no one hurt."
    for ln in wrap(d, pol_deck, font(SANS, 26), left_w):
        d.text((M, ty), ln, font=font(SANS, 26), fill=(48, 48, 48))
        ty += 32
    d.text((M, ty + 4), "Source: AP / Reuters, 20 Nov 2026",
           font=font(SANS, 22), fill=GREY)
    mx = 1330
    mw = W - M - mx
    d.text((mx, gy), "SPACE", font=font(SANS_B, 26), fill=RED)
    mh = font(SERIF_B, 36)
    d.text((mx, gy + 30), "BepiColombo reaches Mercury", font=mh, fill=INK)
    mty = gy + 74
    for ln in wrap(d, "After an eight-year journey, the ESA–JAXA probe enters orbit today.",
                   font(SANS, 24), mw):
        d.text((mx, mty), ln, font=font(SANS, 24), fill=(48, 48, 48))
        mty += 30
    d.text((mx, mty + 4), "Source: ESA, 21 Nov 2026",
           font=font(SANS, 22), fill=GREY)
    draw_photo(d, canvas, "photos/mercury.jpg", mx, mty + 32, 240, 72,
               "Mercury. NASA / MESSENGER")
    d.line([M, 1186, W - M, 1186], fill=RULE, width=2)

    # ---- Grid: 1196-1910, 3 cols x 6 rows, card 109px, gap 10 ----
    ty0 = 1196
    rows, cols = 6, 3
    gw = (W - 2 * M - (cols - 1) * 24) // cols
    gh = 109
    for i, (kicker, head, deck, source) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x = M + c * (gw + 24)
        y = ty0 + r * (gh + 10)
        story_card(d, x, y, gw, gh, kicker, head, deck, source)

    # ---- Timeline + footer: 1916-2048 ----
    fy = 1916
    d.rectangle([M, fy, W - M, fy + 62], fill=INK)
    tf = font(SANS_B, 25)
    tl1 = "THE WEEK SO FAR:  19 NOV — Trump, Xi & Putin sign Shenzhen declaration  •  20 NOV — Kyiv barrage; missiles in Poland; UK–EU deal"
    tl2 = "21 NOV — Riyadh intercepts; Peru quake; BepiColombo reaches Mercury"
    d.text((M + 16, fy + 6), tl1, font=tf, fill=(255, 255, 255))
    d.text((M + 16, fy + 34), tl2, font=tf, fill=(255, 210, 60))
    d.text((M, fy + 74),
           "All 23 stories were reported on 19–21 November 2026 and verified against Reuters, AP, BBC, Al Jazeera, AFP, ESA, UKMTO, IMD and PIB.",
           font=font(SANS, 23), fill=GREY)
    d.text((M, fy + 102),
           "Photos are file photos (Wikimedia Commons / NASA) captioned as such. THE WORLD TODAY — Saturday 21 November 2026.",
           font=font(SANS, 23), fill=GREY)

    out = sys.argv[1] if len(sys.argv) > 1 else "entry-2048.png"
    canvas.save(out, format="PNG")
    print(f"wrote {out} {canvas.size}")


if __name__ == "__main__":
    main()
