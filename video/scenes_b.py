"""Scenes 12-21: the twist, new jobs, Azad's pivot, advice, ending."""
import math
import skia
from gfx import (W, H, INK, CREAM, CREAM2, NAVY, NAVY2, TEAL, TEAL_D, ORANGE, CORAL, GREEN,
                 GOLD, WHITE, GREY, GREY_D, AZAD, MOM, IMRAN,
                 col, fill, stroke, rrect, vgrad, radial_glow, shadow_card, soft_shadow,
                 draw_person, draw_chair, draw_desk, draw_laptop_open,
                 icon_dollar, icon_star, icon_laptop, icon_phone, icon_ai_chip, icon_robot,
                 icon_search, icon_bubble, icon_store, icon_website, icon_trash, icon_calendar,
                 icon_coin, icon_briefcase, icon_chart_line, icon_globe,
                 skyline, tree, cloud, sun_moon, stars, bg_grid, blob, bd_map_path, gig_card)
from text_engine import draw_text, text_width
from util import (clamp, lerp, ease_in_out, ease_out, ease_out_cubic, ease_out_back,
                  ease_out_elastic, pulse, seg, smooth_noise)


def A(t, a, b):
    return seg(t, a, b)


# ---------------- S12: the twist — fewer buyers, bigger jobs ----------------
def sc_twist(c, t, dur):
    vgrad(c, 0, 0, W, H, (20, 28, 52), (38, 50, 84))
    stars(c, t, n=40, alpha=0.5)
    # callback: the question mark turns around (325.7-328.7)
    qa = seg(t, 0.4, 1.6)
    if qa > 0:
        aa = qa * (1 - seg(t, 4.4, 5.8))
        if aa > 0:
            c.save()
            c.translate(300, 300)
            c.rotate((1 - ease_in_out(qa)) * math.pi * 0.5)
            draw_text(c, "?", 0, 60, 150, color=(150, 170, 220), weight="latin_black",
                      align="center", opacity=aa)
            c.restore()
            aa2 = min(seg(t, 1.0, 2.2), 1 - seg(t, 4.2, 5.6))
            draw_text(c, "মনে আছে? সেই সন্দেহটা উল্টো দিকে যাচ্ছিল", 300, 430, 38,
                      color=(226, 233, 248), align="center", opacity=aa2)
    # report card: buyers down but spend up (328.7-341.7)
    ra = seg(t, 3.4, 4.8)
    if ra > 0:
        c.save()
        c.translate(1070, 560)
        shadow_card(c, -520, -330, 1040, 640, 28, bg=(24, 34, 58))
        draw_text(c, "ফাইভারের AI রিপোর্ট", -380, -260, 36, color=(150, 220, 205), align="left")
        # spend per buyer: $30 -> +20%
        ba = ease_out_cubic(seg(t, 5.6, 7.2))
        if ba > 0:
            c.save()
            c.translate(-240, -110)
            rrect(c, -190, -80, 380, 160, 20, fill((30, 42, 68)))
            draw_text(c, "গড় খরচ", 0, -46, 28, color=(150, 162, 186), align="center")
            draw_text(c, "$30", -90, 30, 48, color=GREY, weight="latin_black", align="center")
            arrow_a = seg(t, 7.2, 8.2)
            if arrow_a > 0:
                path = skia.Path()
                path.moveTo(-20, 14)
                path.lineTo(30, 14)
                c.drawPath(path, stroke(GREEN, 7, int(255 * arrow_a)))
                p = skia.Path()
                p.moveTo(30, 14)
                p.lineTo(14, 2)
                p.lineTo(14, 26)
                p.close()
                c.drawPath(p, fill(GREEN, int(255 * arrow_a)))
            draw_text(c, "+২০%", 110, 30, 48, color=GREEN, weight="bold", align="center",
                      opacity=seg(t, 8.2, 9.2))
            c.restore()
        # big projects grow (339.7-341.7 -> t 14-16)
        pa = seg(t, 13.4, 14.6)
        if pa > 0:
            c.save()
            c.translate(180, 120)
            rrect(c, -260, -110, 520, 220, 20, fill((30, 42, 68)))
            draw_text(c, "$১০০০+ প্রজেক্ট", 0, -50, 40, color=(240, 205, 130), align="center")
            pts = [(0.0, 0.25), (0.4, 0.45), (0.7, 0.7), (1.0, 0.95)]
            icon_chart_line(c, -190, -10, 380, 120, pts, color=GOLD, lw=9,
                            t=seg(t, 14.6, 15.6))
            draw_text(c, "১২ মাসে বড় লেনদেন বাড়ছে", 0, 150, 26, color=(150, 162, 186), align="center")
            c.restore()
        c.restore()
    # caption
    aa = min(seg(t, 10.0, 11.4), 1 - seg(t, 14.6, 15.8))
    if aa > 0:
        draw_text(c, "ক্রেতা কমেছে — কিন্তু যারা আছেন, তারা বড় কাজ দিচ্ছেন", 960, 1010, 42,
                  color=(226, 233, 248), align="center", opacity=aa)


# ---------------- S13: jobs that survived ----------------
def sc_survived(c, t, dur):
    vgrad(c, 0, 0, W, H, (245, 242, 235), (227, 220, 205))
    blob(c, W * 0.3, 280, 300, (150, 205, 195), 28, t)
    blob(c, W * 0.75, 780, 280, (250, 205, 140), 26, t * 1.1)
    # left: simple jobs fade, complex jobs stay (341.7-352.7)
    ca = seg(t, 0.6, 2.0)
    if ca > 0:
        # simple jobs (fade out)
        simple = ["$5 লোগো", "ছোট লেখা", "বেসিক ব্যানার"]
        for i, label in enumerate(simple):
            fadeo = 1 - ease_in_out(seg(t, 4.0 + i * 0.5, 6.0 + i * 0.5))
            aa = ca * fadeo
            if aa <= 0:
                continue
            c.save()
            c.translate(420, 340 + i * 150)
            rrect(c, -160, -55, 320, 110, 20, fill(WHITE, int(255 * aa)))
            draw_text(c, label, 0, 12, 36, color=GREY_D, align="center", opacity=aa)
            c.restore()
        # complex jobs (stay, grow)
        complex_ = [("ব্র্যান্ড সিস্টেম", 6.4), ("ডেটা-চালিত ডিজাইন", 7.0), ("স্ট্র্যাটেজি + এক্সিকিউশন", 7.6)]
        for i, (label, t0) in enumerate(complex_):
            aa = seg(t, t0, t0 + 0.9)
            if aa <= 0:
                continue
            c.save()
            c.translate(420, 340 + i * 150)
            sc_ = ease_out_back(aa)
            c.scale(sc_, sc_)
            rrect(c, -180, -60, 360, 120, 20, fill(TEAL))
            draw_text(c, label, 0, 12, 34, color=WHITE, align="center")
            c.restore()
        draw_text(c, "টিকে যাওয়া কাজ = বেশি জটিল", 420, 820, 40, color=INK, align="center",
                  opacity=min(seg(t, 8.6, 9.8), 1 - seg(t, 15.0, 16.4)))
    # right: budget higher + new jobs born (352.7-360.7)
    ba = seg(t, 11.0, 12.4)
    if ba > 0:
        c.save()
        c.translate(1300, 420)
        shadow_card(c, -300, -170, 600, 340, 24)
        draw_text(c, "বাজেটও বেশি", 0, -110, 38, color=INK, align="center")
        for i, (v, lab) in enumerate([("$100", "আগে"), ("$300+", "এখন")]):
            bx = -140 + i * 280
            bh = (120 if i == 0 else 190) * ease_out_cubic(seg(t, 12.4 + i * 0.5, 13.6 + i * 0.5))
            rrect(c, bx - 70, 120 - bh, 140, bh, 12, fill((206, 212, 222) if i == 0 else GREEN))
            draw_text(c, lab, bx, 160, 26, color=(120, 112, 100), align="center")
        c.restore()
    na = seg(t, 14.8, 16.2)
    if na > 0:
        # sprouting new jobs
        c.save()
        c.translate(1300, 830)
        for i in range(3):
            aa = seg(t, 15.2 + i * 0.5, 16.2 + i * 0.5)
            if aa <= 0:
                continue
            c.save()
            c.translate((i - 1) * 220, 0)
            c.scale(ease_out_back(aa), ease_out_back(aa))
            c.drawLine(skia.Point(0, 40), skia.Point(0, -20), stroke(GREEN, 10))
            c.drawCircle(0, -44, 26, fill(GREEN))
            c.drawCircle(0, -44, 14, fill((140, 230, 160)))
            c.restore()
        draw_text(c, "নতুন কাজ জন্ম নিচ্ছে", 0, 110, 36, color=(40, 120, 70), align="center",
                  opacity=seg(t, 16.2, 17.0))
        c.restore()


# ---------------- S14: new jobs +56% / the market changes ----------------
def sc_new_jobs(c, t, dur):
    vgrad(c, 0, 0, W, H, (18, 26, 48), (34, 46, 78))
    bg_grid(c, (120, 150, 210), 9, 120)
    # category cards rising (360.7-388.7)
    cats = [
        ("AI ভিডিও এডিটিং", 1.0, 620, 300, TEAL),
        ("AI ডেটা লেবেলিং", 1.8, 960, 260, ORANGE),
        ("AI চ্যাটবট বানানো", 2.6, 1300, 300, CORAL),
        ("Generative Engine\nOptimization", 3.4, 620, 720, (90, 100, 220)),
        ("ব্র্যান্ড + AI স্ট্র্যাটেজি", 4.2, 1300, 720, GREEN),
    ]
    for label, t0, cx, cy, cc in cats:
        aa = seg(t, t0, t0 + 1.0)
        if aa <= 0:
            continue
        c.save()
        c.translate(cx, cy)
        c.scale(ease_out_back(aa), ease_out_back(aa))
        c.rotate(math.sin(t * 0.6 + t0) * 1.5)
        shadow_card(c, -220, -110, 440, 220, 22, bg=(26, 36, 62))
        rrect(c, -220, -110, 12, 220, 6, fill(cc))
        lines = label.split("\n")
        for j, ln in enumerate(lines):
            draw_text(c, ln, -190, -40 + j * 52, 40 if len(ln) < 22 else 32,
                      color=(226, 233, 248), align="left")
        c.restore()
    # +56% chart (386-390s)
    ca = seg(t, 25.4, 26.8)
    if ca > 0:
        c.save()
        c.translate(960, 300)
        c.scale(ease_out_back(ca), ease_out_back(ca))
        rrect(c, -260, -90, 520, 180, 26, fill(WHITE))
        draw_text(c, "চাহিদা বেড়েছে", -120, 20, 40, color=INK, align="center")
        draw_text(c, "+৫৬%", 130, 30, 72, color=GREEN, weight="bold", align="center")
        c.restore()
    # Imran quote (388.7-393.7)
    qa = seg(t, 28.4, 29.8)
    if qa > 0:
        c.save()
        c.translate(960, 880)
        c.scale(ease_out_back(qa), ease_out_back(qa))
        rrect(c, -520, -90, 1040, 180, 30, fill((26, 36, 60)))
        draw_text(c, "“বাজার মরে না — বাজার বদলায়”", 0, 24, 56, color=(240, 205, 130),
                  align="center", opacity=qa)
        draw_text(c, "— ইমরান ভাই", 0, 90, 30, color=(150, 162, 186), align="center",
                  opacity=seg(t, 30.6, 31.4))
        c.restore()


# ---------------- S15: deleting the $5 gig ----------------
def sc_delete_gig(c, t, dur):
    # morning room
    vgrad(c, 0, 0, W, H, (250, 240, 220), (235, 224, 200))
    radial_glow(c, 1450, 240, 500, (255, 210, 130), 60)
    rrect(c, 1300, 120, 380, 460, 16, fill((210, 190, 160)))
    rrect(c, 1316, 136, 348, 428, 10, fill((250, 240, 215)))
    c.drawLine(skia.Point(1490, 136), skia.Point(1490, 564), stroke((210, 190, 160), 12))
    # plant
    c.save()
    c.translate(1240, 700)
    rrect(c, -40, -20, 80, 70, 10, fill((190, 120, 90)))
    for ang in (-0.5, 0, 0.5):
        c.save()
        c.rotate(math.degrees(ang) + math.sin(t * 0.8) * 2)
        c.drawLine(skia.Point(0, -20), skia.Point(0, -90), stroke((70, 130, 90), 8))
        c.drawCircle(0, -100, 24, fill((90, 160, 110)))
        c.restore()
    c.restore()
    draw_desk(c, 800, 860, 1.35, w=780, color=(94, 78, 64), top=(126, 104, 84))
    draw_chair(c, 800, 1020, 1.25, color=(70, 78, 96))
    draw_person(c, 800, 1020, 1.2, "type", t=t, pal=AZAD, mood="happy", laptop=True)
    # gig card with delete (393.7-403.7)
    da = seg(t, 1.6, 2.8)
    if da > 0:
        c.save()
        c.translate(1420, 560)
        c.rotate(math.sin(t * 0.9) * 2)
        # card
        gone = ease_in_out(seg(t, 3.6, 5.2))
        c.save()
        c.scale(1 - 0.3 * gone, 1 - 0.3 * gone)
        c.saveLayerAlpha(skia.Rect.MakeXYWH(-200, -160, 400, 320), int(255 * (1 - gone)))
        gig_card(c, -170, -125, 1.0, price="$5", stars=5, deleting=gone)
        c.restore()
        # trash icon
        ta = seg(t, 3.2, 4.0)
        if ta > 0:
            c.save()
            c.translate(0, -200 - (1 - ease_out_back(ta)) * 40)
            c.scale(1.2, 1.2)
            icon_trash(c, 0, 0, 1.0)
            c.restore()
        c.restore()
    aa = min(seg(t, 5.6, 6.8), 1 - seg(t, 8.4, 9.6))
    if aa > 0:
        draw_text(c, "প্রথম কাজ — $৫ লোগোর গিগ মুছে ফেলা", 960, 1000, 44, color=(90, 84, 70),
                  align="center", opacity=aa)
    draw_text(c, "সকাল", 1650, 660, 40, color=(180, 150, 110), align="center",
              opacity=seg(t, 0.4, 1.2) * (1 - seg(t, 8.0, 9.0)))


# ---------------- S16: three months of learning ----------------
def sc_learning(c, t, dur):
    vgrad(c, 0, 0, W, H, (247, 242, 232), (230, 221, 204))
    c.drawRect(skia.Rect.MakeXYWH(0, 950, W, H - 950), fill((214, 203, 182)))
    # 3 month calendar strip (403.7-408.7)
    ca = seg(t, 0.5, 1.8)
    if ca > 0:
        for i, m in enumerate(["মাস ১", "মাস ২", "মাস ৩"]):
            aa = seg(t, 0.7 + i * 0.45, 1.5 + i * 0.45)
            if aa <= 0:
                continue
            c.save()
            c.translate(400 + i * 240, 260)
            c.scale(ease_out_back(aa), ease_out_back(aa))
            icon_calendar(c, 0, 0, 1.1, label=f"0{i+1}", head=TEAL)
            draw_text(c, m, 0, 74, 26, color=(110, 104, 92), align="center")
            c.restore()
        aa = min(seg(t, 2.0, 3.0), 1 - seg(t, 18.0, 19.4))
        draw_text(c, "তিন মাস — নতুন কোনো গিগ না", 960, 200, 44, color=INK, align="center", opacity=aa)
    # lesson 1: brand = color + letter (408.7-415.7)
    la = seg(t, 5.4, 6.8)
    if la > 0:
        c.save()
        c.translate(480, 560)
        c.scale(ease_out_back(la), ease_out_back(la))
        shadow_card(c, -260, -180, 520, 360, 24)
        draw_text(c, "ব্র্যান্ড কীসে দাঁড়িয়ে?", 0, -120, 34, color=INK, align="center")
        # color swatches
        for i, cc in enumerate([(239, 68, 68), (245, 158, 11), (16, 150, 138), (59, 90, 200)]):
            sw = seg(t, 7.0 + i * 0.3, 7.8 + i * 0.3)
            if sw > 0:
                c.save()
                c.translate(-180 + i * 90, -20)
                c.scale(ease_out_back(sw), ease_out_back(sw))
                rrect(c, -32, -32, 64, 64, 16, fill(cc))
                c.restore()
        # letter mark
        lta = seg(t, 8.4, 9.4)
        if lta > 0:
            c.save()
            c.translate(0, 100)
            c.scale(ease_out_back(lta), ease_out_back(lta))
            c.drawCircle(0, 0, 46, fill(INK))
            draw_text(c, "A", 0, 18, 52, color=WHITE, weight="latin_black", align="center")
            c.restore()
        c.restore()
    # lesson 2: AI tools for big drafts (412.7-418.7)
    aa = seg(t, 9.6, 10.8)
    if aa > 0:
        c.save()
        c.translate(1050, 560)
        c.scale(ease_out_back(aa), ease_out_back(aa))
        shadow_card(c, -240, -180, 480, 360, 24)
        icon_ai_chip(c, 0, -80, 1.2, t=t)
        draw_text(c, "১ ঘণ্টায় বিশাল খসড়া", 0, 40, 32, color=INK, align="center")
        draw_text(c, "AI টুল দিয়ে", 0, 92, 26, color=(120, 112, 100), align="center")
        c.restore()
    # lesson 3: convince the buyer (418.7-425.7)
    ba = seg(t, 15.4, 16.8)
    if ba > 0:
        c.save()
        c.translate(1520, 560)
        c.scale(ease_out_back(ba), ease_out_back(ba))
        shadow_card(c, -220, -180, 440, 360, 24)
        draw_person(c, 0, 150, 0.62, "present", t=t, pal=AZAD, mood="talk")
        icon_bubble(c, -170, -60, 340, 80, bg=(209, 244, 240), tail="left")
        draw_text(c, "কেন আমিই করব?", -140, -30, 30, color=INK)
        c.restore()
    # bottom caption
    aa2 = min(seg(t, 17.6, 19.0), 1 - seg(t, 19.4, 20.8))
    if aa2 > 0:
        draw_text(c, "শেখা — নিজেকে বদলে ফেলা", 960, 880, 44, color=(90, 84, 70),
                  align="center", opacity=aa2)
    draw_person(c, 200, 1010, 1.0, "idle", t=t, pal=AZAD, mood="happy")


# ---------------- S17: portfolio — three shops rebranded ----------------
def sc_portfolio(c, t, dur):
    vgrad(c, 0, 0, W, H, (245, 241, 230), (228, 219, 202))
    c.drawRect(skia.Rect.MakeXYWH(0, 940, W, H - 940), fill((214, 203, 182)))
    aa = min(seg(t, 0.6, 1.8), 1 - seg(t, 16.0, 17.4))
    if aa > 0:
        draw_text(c, "পোর্টফোলিও — তিনটা ছোট অনলাইন দোকান", 960, 200, 46, color=INK,
                  align="center", opacity=aa)
    # three shops being rebranded
    shops = [(420, "লোগো", TEAL, 2.4), (960, "প্যাকেজিং", ORANGE, 3.6), (1500, "ফেসবুক পেজ", (59, 90, 200), 4.8)]
    for cx, label, cc, t0 in shops:
        aa = seg(t, t0, t0 + 1.0)
        if aa <= 0:
            continue
        c.save()
        c.translate(cx, 560)
        c.scale(ease_out_back(aa), ease_out_back(aa))
        shadow_card(c, -240, -200, 480, 400, 26)
        icon_store(c, 0, -60, 1.6, body=cc, awning=WHITE)
        # new brand sparkle
        sp = pulse(t, 1.8, t0)
        radial_glow(c, 0, -60, 140, cc, int(50 + 30 * sp))
        draw_text(c, label, 0, 110, 38, color=INK, align="center")
        # checkmark
        ck = seg(t, t0 + 1.2, t0 + 1.9)
        if ck > 0:
            c.save()
            c.translate(170, -170)
            c.scale(ease_out_back(ck), ease_out_back(ck))
            c.drawCircle(0, 0, 26, fill(GREEN))
            path = skia.Path()
            path.moveTo(-11, 0)
            path.lineTo(-3, 9)
            path.lineTo(12, -9)
            c.drawPath(path, stroke(WHITE, 6))
            c.restore()
        c.restore()
    # slowly growing (439.7-445.7)
    ga = seg(t, 12.0, 13.4)
    if ga > 0:
        c.save()
        c.translate(960, 900)
        c.scale(ease_out_back(ga), ease_out_back(ga))
        rrect(c, -300, -60, 600, 120, 60, fill(TEAL, 30))
        draw_text(c, "আস্তে আস্তে — একটা কাজ, তারপর আরেকটা", 0, 12, 40, color=TEAL_D, align="center")
        c.restore()


# ---------------- S18: no magic formula ----------------

def sc_no_magic(c, t, dur):
    vgrad(c, 0, 0, W, H, (22, 30, 52), (40, 52, 84))
    stars(c, t, n=40, alpha=0.4)
    # story card dissolves (445.7-449.7)
    sa = seg(t, 0.4, 1.6)
    if sa > 0:
        dis = ease_in_out(seg(t, 3.4, 5.4))
        c.save()
        c.translate(960, 380 + math.sin(t * 0.9) * 5)
        c.saveLayerAlpha(skia.Rect.MakeXYWH(-560, -160, 1120, 320), int(255 * sa * (1 - dis)))
        c.scale(1 - 0.15 * dis, 1 - 0.15 * dis)
        rrect(c, -520, -110, 1040, 220, 30, fill((30, 42, 68)))
        draw_text(c, "আজাদের গল্প — কোনো জাদুর সূত্র নয়", 0, 12, 52, color=(226, 233, 248),
                  align="center")
        c.restore()
    # real picture (451.7-459.7)
    ra = seg(t, 6.4, 7.8)
    if ra > 0:
        aa = ra * (1 - seg(t, 16.0, 17.4))
        if aa > 0:
            c.save()
            c.translate(960, 640 + math.sin(t * 0.8 + 1.5) * 5)
            c.scale(ease_out_back(ra), ease_out_back(ra))
            rrect(c, -480, -90, 960, 180, 30, fill((26, 36, 60)))
            draw_text(c, "নতুনদের জন্য বাস্তব চিত্র", 0, 12, 48, color=(240, 205, 130), align="center")
            c.restore()
    # reality 1: some months at zero (459.7-465.7)
    za = seg(t, 10.4, 11.8)
    if za > 0:
        c.save()
        c.translate(560, 900 + math.sin(t * 0.9 + 0.6) * 4)
        c.scale(ease_out_back(za), ease_out_back(za))
        shadow_card(c, -280, -140, 560, 280, 24, bg=WHITE)
        draw_text(c, "কয়েক মাস আয় শূন্য থাকতে পারে", 0, -80, 34, color=INK, align="center")
        pts = [(0.0, 0.5), (0.3, 0.05), (0.7, 0.05), (1.0, 0.05)]
        icon_chart_line(c, -220, -30, 440, 120, pts, color=CORAL, lw=8, t=seg(t, 12.2, 13.8))
        c.restore()
    # reality 2: keep a side income
    ba = seg(t, 15.2, 16.6)
    if ba > 0:
        c.save()
        c.translate(1360, 900 + math.sin(t * 0.9 + 2.1) * 4)
        c.scale(ease_out_back(ba), ease_out_back(ba))
        shadow_card(c, -280, -140, 560, 280, 24, bg=WHITE)
        icon_briefcase(c, -140, 0, 1.6)
        draw_text(c, "শুরুর দিনে", 60, -40, 32, color=INK, align="center")
        draw_text(c, "পাশের কাজ রাখুন", 60, 20, 32, color=INK, align="center")
        c.restore()


# ---------------- S19: practical advice ----------------
def sc_advice(c, t, dur):
    vgrad(c, 0, 0, W, H, (247, 242, 232), (229, 220, 203))
    blob(c, W * 0.2, 260, 280, (150, 205, 195), 26, t)
    blob(c, W * 0.85, 800, 300, (250, 205, 140), 26, t * 1.2)
    aa = min(seg(t, 0.4, 1.6), 1 - seg(t, 26.0, 27.4))
    if aa > 0:
        draw_text(c, "বাস্তব পরামর্শ", 960, 170, 54, color=INK, align="center", opacity=aa)
    items = [
        ("দাম ৩ গুণ করে শুরু", "×3", 2.0, 480, 420, TEAL),
        ("ফাইভারের ২০% ফি হিসাব রাখুন", "20%", 4.0, 960, 420, ORANGE),
        ("প্রতি ৪-৫ দিনে গিগ আপডেট", "৪-৫ দিন", 6.0, 1440, 420, GREEN),
        ("প্ল্যাটফর্মের বাইরে লেনদেন নয়", "!", 9.0, 720, 760, CORAL),
        ("নিজের ওয়েবসাইট • লিংকডইন", "in", 12.0, 1200, 760, (59, 90, 200)),
    ]
    for label, badge, t0, cx, cy, cc in items:
        aa = seg(t, t0, t0 + 0.9)
        if aa <= 0:
            continue
        c.save()
        c.translate(cx, cy)
        c.scale(ease_out_back(aa), ease_out_back(aa))
        c.rotate(math.sin(t * 0.7 + t0) * 1.2)
        shadow_card(c, -230, -110, 460, 220, 22)
        rrect(c, -230, -110, 12, 220, 6, fill(cc))
        # badge
        c.save()
        c.translate(150, -50)
        c.scale(0.9, 0.9)
        c.drawCircle(0, 0, 44, fill(cc, 36))
        draw_text(c, badge, 0, 16, 44, color=cc, weight="latin_black", align="center")
        c.restore()
        lines = label.split(" • ")
        for j, ln in enumerate(lines):
            draw_text(c, ln, -190, -10 + j * 52, 34, color=INK, align="left")
        c.restore()


# ---------------- S20: build your own door ----------------
def sc_own_door(c, t, dur):
    vgrad(c, 0, 0, W, H, (18, 26, 48), (36, 48, 80))
    bg_grid(c, (120, 150, 210), 9, 120)
    # platform = one door vs own presence = many doors (495.7-517)
    aa = min(seg(t, 0.6, 1.8), 1 - seg(t, 18.0, 19.4))
    if aa > 0:
        draw_text(c, "একটা দরজা নয় — নিজের ঠিকানা গড়ুন", 960, 180, 50, color=(226, 233, 248),
                  align="center", opacity=aa)
    # own website card
    wa = seg(t, 3.4, 4.8)
    if wa > 0:
        c.save()
        c.translate(560, 520 + math.sin(t * 0.9) * 4)
        c.scale(ease_out_back(wa), ease_out_back(wa))
        shadow_card(c, -260, -200, 520, 400, 26, bg=WHITE)
        icon_website(c, 0, -60, 1.4, t=t)
        draw_text(c, "নিজের ওয়েবসাইট", 0, 120, 36, color=INK, align="center")
        c.restore()
    # linkedin card
    la = seg(t, 7.4, 8.8)
    if la > 0:
        c.save()
        c.translate(1100, 520 + math.sin(t * 0.9 + 1.2) * 4)
        c.scale(ease_out_back(la), ease_out_back(la))
        shadow_card(c, -260, -200, 520, 400, 26, bg=WHITE)
        c.save()
        c.translate(0, -60)
        rrect(c, -70, -70, 140, 140, 20, fill((59, 90, 200)))
        draw_text(c, "in", 0, 30, 84, color=WHITE, weight="latin_black", align="center")
        c.restore()
        draw_text(c, "প্রফেশনাল প্রোফাইল", 0, 120, 36, color=INK, align="center")
        c.restore()
    # audience growing
    au = seg(t, 11.4, 12.8)
    if au > 0:
        c.save()
        c.translate(1560, 520 + math.sin(t * 0.9 + 2.4) * 4)
        c.scale(ease_out_back(au), ease_out_back(au))
        shadow_card(c, -220, -200, 440, 400, 26, bg=(26, 36, 60))
        draw_text(c, "নিজের ভিজিটর", 0, -130, 32, color=(226, 233, 248), align="center")
        pts = [(0.0, 0.1), (0.3, 0.3), (0.6, 0.55), (1.0, 0.9)]
        icon_chart_line(c, -170, -90, 340, 200, pts, color=GREEN, lw=9,
                        area=(34, 197, 94), t=seg(t, 12.8, 14.6))
        c.restore()
    # caption
    aa2 = min(seg(t, 17.6, 18.8), 1)
    if aa2 > 0:
        draw_text(c, "যখন কেউ খুঁজবে — আপনি তখন সহজে খুঁজে পাওয়া যান", 960, 950, 40,
                  color=(200, 210, 235), align="center", opacity=aa2)


# ---------------- S21: ending ----------------
def sc_ending(c, t, dur):
    # sunrise scene
    sr = ease_in_out(seg(t, 0.0, 4.0))
    top = (lerp(30, 255, sr), lerp(40, 200, sr), lerp(70, 150, sr))
    bot = (lerp(50, 250, sr), lerp(60, 235, sr), lerp(90, 210, sr))
    vgrad(c, 0, 0, W, H, top, bot)
    sun_y = lerp(760, 300, ease_out_cubic(sr))
    sun_moon(c, 960, sun_y, 90, night=False, t=t)
    for cx, cy, cs, cp in [(400, 300, 1.1, 0.0), (1450, 260, 0.9, 2.0)]:
        cloud(c, cx + math.sin(t * 0.12 + cp) * 20, cy, cs, color=(255, 245, 235), alpha=180)
    skyline(c, 900, t, 1.0, color=(70, 96, 130), seed=21.0)
    c.drawRect(skia.Rect.MakeXYWH(0, 930, W, H - 930), fill((90, 120, 100)))
    tree(c, 300, 940, 1.4, sway=math.sin(t * 0.7) * 0.02)
    tree(c, 1620, 945, 1.2, sway=math.sin(t * 0.7 + 2) * 0.02)
    # azad confident at dawn
    draw_person(c, 1180, 945, 1.15, "celebrate" if t > 6.5 else "idle", t=t, pal=AZAD,
                mood="happy")
    # big statement (517.7-521.7)
    ta = seg(t, 1.6, 3.0)
    if ta > 0:
        aa = ta * (1 - seg(t, 8.4, 9.8))
        if aa > 0:
            c.save()
            c.translate(820, 400)
            c.scale(ease_out_back(ta), ease_out_back(ta))
            shadow_card(c, -480, -110, 960, 220, 34, bg=WHITE, alpha=aa)
            draw_text(c, "পাঁচ ডলারের যুগ শেষ", 0, 20, 76, color=INK, align="center", opacity=aa)
            c.restore()
    # closing line (521.7-529.9)
    ca = seg(t, 5.4, 6.8)
    if ca > 0:
        aa = ca
        c.save()
        c.translate(820, 660)
        c.scale(ease_out_back(ca), ease_out_back(ca))
        rrect(c, -560, -110, 1120, 220, 30, fill((16, 26, 43), int(230 * ca)))
        draw_text(c, "টিকে থাকবেন তিনিই — যিনি এমন কিছু বিক্রি করেন", 0, -30, 40,
                  color=(240, 205, 130), align="center", opacity=aa)
        draw_text(c, "যা ক্রেতা AI-কে জিজ্ঞেস করে নিজে বানাতে পারেন না", 0, 50, 40,
                  color=WHITE, align="center", opacity=aa)
        c.restore()
