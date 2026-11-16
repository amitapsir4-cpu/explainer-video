"""Scenes 1-11: intro, Azad's rise, first orders, AI disruption."""
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


# ---------------- S1: cold open — the doubt ----------------
def sc_intro(c, t, dur):
    vgrad(c, 0, 0, W, H, (9, 14, 26), (24, 34, 58))
    stars(c, t, n=90, alpha=0.9)
    # window light
    c.save()
    wx, wy, ww, wh = 1180, 200, 420, 520
    c.translate(wx + ww / 2, wy + wh / 2)
    c.rotate(math.sin(t * 0.12) * 1.2)
    c.translate(-(wx + ww / 2), -(wy + wh / 2))
    radial_glow(c, wx + ww / 2, wy + wh / 2, 480, (120, 150, 220), 60)
    rrect(c, wx, wy, ww, wh, 18, fill((28, 40, 66)))
    rrect(c, wx + 12, wy + 12, ww - 24, wh - 24, 12, fill((52, 72, 116)))
    c.drawLine(skia.Point(wx + ww / 2, wy + 12), skia.Point(wx + ww / 2, wy + wh - 12), stroke((28, 40, 66), 14))
    c.drawLine(skia.Point(wx + 12, wy + wh / 2), skia.Point(wx + ww - 12, wy + wh / 2), stroke((28, 40, 66), 14))
    moon_x = wx + ww * 0.72
    moon_y = wy + wh * 0.30
    c.drawCircle(moon_x, moon_y, 26, fill((220, 228, 250)))
    c.drawCircle(moon_x - 10, moon_y - 6, 22, fill((52, 72, 116)))
    c.restore()

    # silhouette figure by the window
    fig_a = seg(t, 2.0, 3.5)
    if fig_a > 0:
        c.save()
        c.translate(980, 940)
        c.scale(1.05, 1.05)
        body = fill((8, 12, 22), int(255 * fig_a))
        c.drawCircle(0, -300, 34, body)
        rrect(c, -38, -268, 76, 160, 30, body)
        c.drawLine(skia.Point(-30, -140), skia.Point(-34, 0), stroke((8, 12, 22), 26 * fig_a))
        c.drawLine(skia.Point(30, -140), skia.Point(34, 0), stroke((8, 12, 22), 26 * fig_a))
        sway = math.sin(t * 0.8) * 3
        c.drawLine(skia.Point(-28, -240), skia.Point(-70 + sway, -160), stroke((8, 12, 22), 20 * fig_a))
        c.drawLine(skia.Point(28, -240), skia.Point(70 + sway, -160), stroke((8, 12, 22), 20 * fig_a))
        c.restore()

    # question marks drifting
    qa = seg(t, 4.5, 6.0)
    if qa > 0:
        for i, (qx, qy, qs, qp) in enumerate([(420, 320, 150, 0.0), (640, 560, 90, 1.3),
                                              (300, 640, 64, 2.1), (1500, 300, 110, 0.7),
                                              (1620, 620, 70, 2.8), (1340, 720, 56, 3.6)]):
            aa = qa * (0.25 + 0.2 * math.sin(t * 1.1 + qp))
            yy = qy + math.sin(t * 0.9 + qp) * 14
            draw_text(c, "?", qx, yy, qs, color=(150, 170, 220), weight="latin_black",
                      align="center", opacity=aa)
    # big central question mark
    big_a = seg(t, 6.5, 8.0)
    if big_a > 0:
        s = 200 * (0.6 + 0.4 * ease_out_back(big_a))
        glow = 0.5 + 0.5 * math.sin(t * 1.4)
        radial_glow(c, W / 2, 430, 300 + 40 * glow, (110, 140, 220), int(70 * big_a))
        draw_text(c, "?", W / 2, 430 + s * 0.55, s, color=(214, 226, 255), weight="latin_black",
                  align="center", opacity=big_a)
    # narration captions
    if seg(t, 0.6, 1.2) > 0 and t < 10.5:
        aa = min(seg(t, 0.6, 1.4), 1 - seg(t, 9.2, 10.4))
        draw_text(c, "এক বছর আগে", W / 2, 850, 66, color=(226, 233, 248), align="center", opacity=aa)
    if 10.5 <= t:
        aa = min(seg(t, 11.0, 12.2), 1 - seg(t, 21.8, 23.4))
        draw_text(c, "একটা সন্দেহ — গল্পের সবচেয়ে বড় রহস্য", W / 2, 850, 58,
                  color=(226, 233, 248), align="center", opacity=aa)
    if t >= 19.5:
        aa = min(seg(t, 19.8, 21.0), 1)
        draw_text(c, "চলুন দেখি একজন নতুন ফ্রিল্যান্সারের গল্প", W / 2, 950, 46,
                  color=(150, 200, 190), align="center", opacity=aa)


# ---------------- S2: meet Azad ----------------
def sc_meet_azad(c, t, dur):
    vgrad(c, 0, 0, W, H, (247, 242, 232), (231, 221, 202))
    blob(c, W * 0.5, H * 0.42, 430, (255, 214, 150), 36, t)
    blob(c, W * 0.2, H * 0.7, 300, (140, 200, 190), 30, t * 1.3)
    blob(c, W * 0.82, H * 0.3, 260, (240, 170, 130), 26, t * 0.8)
    ground_y = 900
    c.drawRect(skia.Rect.MakeXYWH(0, ground_y, W, H - ground_y), fill((216, 204, 182)))

    # crowd of grey silhouettes
    crowd_a = seg(t, 0.2, 1.6)
    focus = ease_in_out(seg(t, 4.0, 6.5))  # 1 = focus on Azad
    rnd = 11.0
    for i in range(13):
        rnd = (rnd * 9301 + 49297) % 233280
        r1 = rnd / 233280
        rnd = (rnd * 9301 + 49297) % 233280
        r2 = rnd / 233280
        cx = 120 + r1 * 1680
        s = 0.55 + r2 * 0.35
        if abs(cx - 960) < 150:
            continue
        grey = 150 + int(r2 * 40)
        fade = crowd_a * (1 - 0.75 * focus)
        pal = dict(skin=(grey, grey, grey + 8), hair=(grey - 40,) * 3, shirt=(grey - 10,) * 3,
                   shirt2=(grey - 30,) * 3, pants=(grey - 20,) * 3)
        if fade > 0.01:
            draw_person(c, cx, ground_y + r2 * 20, s, "idle", t=t + i, pal=pal,
                        mood="neutral", alpha=fade)
    # azad steps forward
    az_a = seg(t, 4.5, 6.0)
    az_x = lerp(700, 960, ease_out_back(seg(t, 4.5, 7.0)))
    if az_a > 0:
        draw_person(c, az_x, ground_y, 1.25, "present" if t > 30 else "idle", t=t,
                    pal=AZAD, mood="happy" if t > 30 else "smile_open",
                    alpha=az_a, walk_phase=t * 6)

    # label
    la = seg(t, 7.0, 8.2) * (1 - seg(t, 20.5, 21.8))
    if la > 0:
        shadow_card(c, az_x - 110, 380, 220, 84, 42, bg=WHITE, alpha=la)
        draw_text(c, "আজাদ", az_x, 438, 52, color=INK, align="center", opacity=la)
    # 'not one person' line
    if 12.5 <= t < 24.2:
        aa = min(seg(t, 12.8, 14.0), 1 - seg(t, 21.5, 23.0))
        draw_text(c, "নির্দিষ্ট কোনো মানুষ নন — হাজারো ফ্রিল্যান্সারের মিলিত ছবি", W / 2, 1000, 44,
                  color=(90, 84, 70), align="center", opacity=aa)

    # Bangladesh map with stat
    ma = seg(t, 4.8, 6.6)
    if ma > 0:
        map_a = ma * (1 - seg(t, 16.8, 18.8))
        if map_a > 0:
            mx, my, mw, mh = 1330, 210, 420, 520
            path = bd_map_path(mx, my, mw, mh)
            c.save()
            c.saveLayerAlpha(skia.Rect.MakeXYWH(mx - 40, my - 40, mw + 80, mh + 80), int(255 * map_a))
            c.drawPath(path, fill((18, 148, 144), 235))
            c.drawPath(path, stroke((10, 90, 84), 6))
            # pulsing worker dots
            rnd = 5.0
            for i in range(26):
                rnd = (rnd * 9301 + 49297) % 233280
                r1, r2 = rnd / 233280, ((rnd * 7919) % 233280) / 233280
                px, py = mx + 30 + r1 * (mw - 60), my + 30 + r2 * (mh - 60)
                ph = pulse(t, 2.2 + r2, r1 * 3)
                c.drawCircle(px, py, 4 + 3 * ph, fill(WHITE, int(200 * ph + 40)))
            c.restore()
            draw_text(c, "বাংলাদেশ", mx + mw / 2, my - 44, 44, color=INK, align="center", opacity=map_a)
            # #2 badge
            ba = seg(t, 10.3, 11.8)
            if ba > 0:
                bx, by = mx + mw / 2, my + mh / 2
                c.save()
                c.translate(bx, by)
                c.scale(ease_out_back(ba), ease_out_back(ba))
                rrect(c, -92, -64, 184, 128, 24, fill(WHITE))
                draw_text(c, "#2", 0, 30, 84, color=CORAL, weight="latin_black", align="center")
                draw_text(c, "অনলাইন শ্রম", 0, 106, 30, color=(90, 84, 70), align="center")
                c.restore()


# ---------------- S3: Rajshahi, course, first gig ----------------
def sc_rajshahi(c, t, dur):
    # day establishing shot
    day_end = 15.0
    day_a = 1 - seg(t, day_end - 1.2, day_end + 0.6)
    if day_a > 0:
        c.save()
        c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * day_a))
        vgrad(c, 0, 0, W, H, (168, 216, 234), (240, 230, 205))
        sun_moon(c, 1560, 200, 64, night=False, t=t)
        for cx, cy, cs, cp in [(300, 180, 1.2, 0.0), (800, 130, 0.9, 2.0), (1200, 220, 1.0, 4.0)]:
            cloud(c, cx + math.sin(t * 0.15 + cp) * 30, cy, cs, alpha=220)
        skyline(c, 880, t, 1.0, color=(94, 120, 150), alpha=1.0, seed=5.0)
        skyline(c, 920, t, 0.7, color=(70, 94, 126), alpha=1.0, seed=9.0)
        c.drawRect(skia.Rect.MakeXYWH(0, 920, W, H - 920), fill((196, 186, 156)))
        tree(c, 240, 930, 1.3, sway=math.sin(t * 0.7) * 0.02)
        tree(c, 1680, 935, 1.1, sway=math.sin(t * 0.7 + 2) * 0.02)
        # walking azad (small, wide shot)
        wa = seg(t, 1.0, 2.0)
        if wa > 0:
            draw_person(c, lerp(500, 1050, ease_in_out(min(1.0, t / 13.0))), 925, 0.85, "walk",
                        t=t, pal=AZAD, mood="neutral", walk_phase=t * 7.0, alpha=wa)
        la = seg(t, 1.6, 2.8)
        if la > 0:
            draw_text(c, "রাজশাহী", W / 2, 240, 96, color=(52, 72, 96), align="center", opacity=la)
        c.restore()

    # night room
    na = seg(t, day_end - 0.6, day_end + 0.4)
    if na > 0:
        c.save()
        c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * na))
        vgrad(c, 0, 0, W, H, (16, 22, 40), (26, 34, 58))
        # window with moon
        rrect(c, 1360, 140, 360, 420, 16, fill((22, 30, 52)))
        rrect(c, 1374, 154, 332, 392, 10, fill((36, 52, 88)))
        c.drawCircle(1600, 260, 30, fill((220, 228, 250)))
        c.drawCircle(1590, 254, 26, fill((36, 52, 88)))
        stars(c, t, n=30, alpha=0.8, seed=3.0)
        c.drawLine(skia.Point(1540, 154), skia.Point(1540, 546), stroke((22, 30, 52), 12))
        # wall art & shelf
        rrect(c, 200, 180, 180, 130, 10, fill((32, 44, 70)))
        c.drawCircle(260, 235, 26, fill(ORANGE, 220))
        c.drawCircle(320, 245, 18, fill(TEAL, 220))
        rrect(c, 440, 200, 220, 16, 6, fill((44, 56, 84)))
        rrect(c, 470, 160, 40, 40, 6, fill((60, 74, 104)))
        rrect(c, 540, 168, 30, 32, 5, fill((80, 96, 128)))
        # lamp glow
        radial_glow(c, 1180, 620, 420, (255, 190, 110), 46)
        # desk
        draw_desk(c, 760, 850, 1.35, w=760, color=(58, 48, 44), top=(96, 78, 64))
        draw_chair(c, 760, 1010, 1.2, color=(40, 46, 62))
        draw_person(c, 760, 1010, 1.18, "type", t=t, pal=AZAD, mood="happy", laptop=True)
        # course progress (43-48s -> t 0-4.5)
        pa = seg(t, 1.2, 2.4) * (1 - seg(t, 5.6, 6.6))
        if pa > 0:
            bx, by, bw, bh = 300, 560, 420, 130
            shadow_card(c, bx, by, bw, bh, 18, alpha=pa)
            draw_text(c, "গ্রাফিক ডিজাইন কোর্স", bx + 24, by + 46, 32, color=INK, opacity=pa)
            pr = ease_out_cubic(seg(t, 1.6, 4.6))
            rrect(c, bx + 24, by + 74, bw - 48, 20, 10, fill((226, 230, 236)))
            rrect(c, bx + 24, by + 74, (bw - 48) * pr, 20, 10, fill(TEAL))
            draw_text(c, f"{int(pr * 100)}%", bx + bw - 60, by + 92, 26, color=TEAL_D,
                      weight="latin", align="center", opacity=pa)
        # youtube montage (48-53 -> t 4.5-9.5)
        ya = seg(t, 5.4, 6.6) * (1 - seg(t, 9.8, 10.8))
        if ya > 0:
            for i, (vx, vy, vs, vr) in enumerate([(1080, 430, 1.0, 0.4), (1330, 560, 0.8, 1.9),
                                                  (1150, 660, 0.65, 3.1)]):
                aa = ya * (0.5 + 0.5 * math.sin(t * 0.9 + vr))
                c.save()
                c.translate(vx, vy)
                c.rotate(math.sin(t * 0.5 + vr) * 3)
                c.scale(vs * ease_out_back(seg(t, 5.6 + i * 0.5, 6.6 + i * 0.5)))
                shadow_card(c, -110, -70, 220, 140, 12, alpha=aa)
                rrect(c, -98, -58, 196, 116, 8, fill((30, 40, 60)))
                c.drawCircle(0, 0, 30, fill(CORAL, int(255 * aa)))
                path = skia.Path()
                path.moveTo(-9, -16)
                path.lineTo(16, 0)
                path.lineTo(-9, 16)
                path.close()
                c.drawPath(path, fill(WHITE, int(255 * aa)))
                c.restore()
            aa2 = min(seg(t, 6.4, 7.4), 1 - seg(t, 9.6, 10.6))
            draw_text(c, "প্রথম মাসে $১০০০?", 1080, 820, 44, color=(240, 200, 120),
                      align="center", opacity=aa2)
        # fiverr account + gig card (53.4-59.7 -> t 9.8-16)
        fa = seg(t, 10.4, 11.8)
        if fa > 0:
            aa = fa * (1 - seg(t, 15.0, 16.1))
            if aa > 0:
                ga = ease_out_back(seg(t, 11.6, 13.2))
                c.save()
                c.translate(1180, 620)
                c.scale(ga, ga)
                c.rotate(math.sin(t * 0.7) * 1.5)
                gig_card(c, -180, -140, 1.0, price="$5", stars=0, alpha=aa)
                c.restore()
                # "gig live" ping
                ping = seg(t, 13.6, 14.6)
                if ping > 0 and ping < 1:
                    rr = 40 + ping * 120
                    c.drawCircle(1180, 560, rr, stroke(GREEN, 6, int(255 * (1 - ping))))
                aa2 = min(seg(t, 12.6, 13.6), 1 - seg(t, 15.2, 16.0))
                draw_text(c, "প্রথম গিগ লাইভ!", 1180, 830, 46, color=GREEN, align="center", opacity=aa2)
        c.restore()


# ---------------- S4: first order & mom ----------------
def sc_first_order(c, t, dur):
    vgrad(c, 0, 0, W, H, (14, 20, 38), (30, 40, 66))
    radial_glow(c, 700, 640, 500, (255, 190, 110), 40)
    rrect(c, 1420, 120, 340, 400, 16, fill((20, 28, 48)))
    rrect(c, 1434, 134, 312, 372, 10, fill((34, 48, 82)))
    c.drawCircle(1650, 240, 26, fill((220, 228, 250)))
    c.drawCircle(1640, 234, 22, fill((34, 48, 82)))
    draw_desk(c, 700, 850, 1.35, w=760, color=(58, 48, 44), top=(96, 78, 64))
    draw_chair(c, 700, 1010, 1.2, color=(40, 46, 62))
    mood = "worried" if t < 1 else ("happy" if 3 < t < 8 else "smile_open")
    pose = "type" if t < 2.4 else ("phone" if 3.0 <= t < 12.5 else "type")
    draw_person(c, 700, 1010, 1.18, pose, t=t, pal=AZAD, mood=mood, laptop=(t < 2.4 or t >= 12.5),
                phone=(3.0 <= t < 12.5))

    # order notification
    na = seg(t, 0.2, 1.4) * (1 - seg(t, 3.4, 4.4))
    if na > 0:
        c.save()
        c.translate(1240, 380)
        c.scale(ease_out_back(seg(t, 0.2, 1.2)), ease_out_back(seg(t, 0.2, 1.2)))
        shadow_card(c, -170, -70, 340, 130, 20, alpha=na)
        rrect(c, -150, -50, 60, 60, 30, fill(GREEN))
        path = skia.Path()
        path.moveTo(-130, -20)
        path.lineTo(-118, -8)
        path.lineTo(-98, -32)
        c.drawPath(path, stroke(WHITE, 8))
        draw_text(c, "নতুন অর্ডার!", -70, -6, 34, color=INK, opacity=na)
        draw_text(c, "$5 • লোগো ডিজাইন", -70, 34, 26, color=(110, 118, 130), opacity=na)
        c.restore()
        ping = seg(t, 0.6, 1.6)
        if ping < 1:
            c.drawCircle(1240, 380, 60 + ping * 160, stroke(GREEN, 6, int(255 * (1 - ping))))

    # counting money in hands
    ca = seg(t, 4.6, 6.0) * (1 - seg(t, 12.0, 13.2))
    if ca > 0:
        c.save()
        c.translate(1240, 560)
        c.rotate(math.sin(t * 1.2) * 2)
        for i in range(4):
            off = i * 7 * (0.5 + 0.5 * math.sin(t * 2.5 + i))
            c.save()
            c.translate(off * 0.6, -off * 0.3)
            c.rotate(-6 + i * 3)
            rrect(c, -90, -40, 180, 80, 10, fill((70, 160, 106)))
            rrect(c, -78, -28, 156, 56, 6, fill((92, 184, 128)))
            c.drawCircle(0, 0, 22, fill((70, 160, 106)))
            draw_text(c, "$", 0, 12, 34, color=(40, 100, 70), weight="latin_black", align="center")
            c.restore()
        c.restore()
        aa = min(seg(t, 5.0, 6.0), 1 - seg(t, 11.6, 12.8))
        draw_text(c, "হাতে গুনে দেখা — কয়েকবার", 1240, 760, 38, color=(240, 210, 140),
                  align="center", opacity=aa)

    # phone call split
    ph_a = seg(t, 6.6, 7.8)
    if ph_a > 0:
        aa = ph_a * (1 - seg(t, 13.0, 14.2))
        if aa > 0:
            # mom side card
            mx, my = 1330, 640
            c.save()
            c.translate(mx, my)
            c.scale(ease_out_back(ph_a), ease_out_back(ph_a))
            shadow_card(c, -150, -190, 300, 340, 24, alpha=aa)
            c.save()
            c.translate(0, -30)
            c.scale(0.9, 0.9)
            draw_person(c, 0, 120, 0.85, "phone", t=t + 1.0, pal=MOM, mood="talk", phone=True, alpha=aa)
            c.restore()
            c.restore()
            # speech line
            aa2 = min(seg(t, 9.6, 10.8), 1 - seg(t, 12.6, 13.6))
            icon_bubble(c, 1500, 560, 260, 74, bg=WHITE, tail="left", alpha=aa2)
            draw_text(c, "রাতে কিছু খেয়েছিস?", 1520, 512, 30, color=INK, opacity=aa2)
            # heart
            ha = seg(t, 11.0, 11.8)
            if ha > 0:
                c.save()
                c.translate(1610, 430)
                c.scale(ease_out_back(ha), ease_out_back(ha))
                path = skia.Path()
                path.moveTo(0, 10)
                path.cubicTo(-26, -14, -14, -34, 0, -20)
                path.cubicTo(14, -34, 26, -14, 0, 10)
                path.close()
                c.drawPath(path, fill(CORAL))
                c.restore()


# ---------------- S5: orders 1-2-3, stars, price tweaks ----------------
def sc_orders_grow(c, t, dur):
    vgrad(c, 0, 0, W, H, (245, 241, 232), (229, 220, 203))
    blob(c, W * 0.25, 300, 320, (150, 205, 195), 30, t)
    blob(c, W * 0.8, 760, 300, (250, 205, 140), 28, t * 1.2)
    c.drawRect(skia.Rect.MakeXYWH(0, 940, W, H - 940), fill((214, 203, 182)))
    draw_person(c, 240, 1010, 1.05, "idle", t=t, pal=AZAD, mood="happy")

    # three order cards pop in
    cards = [(560, 300, 1.0, 0.6), (960, 260, 1.15, 8.4), (1360, 300, 1.0, 9.2)]
    for i, (cx, cy, cs, t0) in enumerate(cards):
        aa = seg(t, t0, t0 + 0.9)
        if aa <= 0:
            continue
        c.save()
        c.translate(cx, cy)
        sc_ = cs * ease_out_back(aa)
        c.scale(sc_, sc_)
        c.rotate(math.sin(t * 0.8 + i * 2) * 1.5)
        shadow_card(c, -150, -150, 300, 300, 22)
        rrect(c, -130, -130, 260, 150, 14, fill((232, 238, 244)))
        c.drawCircle(-40, -55, 26, fill([TEAL, ORANGE, CORAL][i]))
        draw_text(c, f"0{i+1}", -40, -42, 34, color=WHITE, weight="latin_black", align="center")
        rrect(c, 0, -80, 100, 14, 6, fill((206, 212, 222)))
        rrect(c, 0, -56, 70, 14, 6, fill((206, 212, 222)))
        draw_text(c, "অর্ডার", 0, 100, 34, color=INK, align="center")
        c.restore()
    # stars fill (78-84s)
    sa = seg(t, 12.6, 13.4)
    if sa > 0:
        for i in range(3):
            cx, cy, cs, t0 = cards[i]
            n = int(clamp(sa * 3 - i)) if t > 12.6 else 0
            for j in range(min(5, n)):
                icon_star(c, cx - 56 + j * 28, cy + 130, 12, GOLD)
    # price tweak (84-92s)
    pa = seg(t, 16.0, 17.2)
    if pa > 0:
        price = "$5" if t < 18.5 else ("$4" if t < 20.5 else "$4")
        c.save()
        c.translate(560, 620)
        c.scale(ease_out_back(pa), ease_out_back(pa))
        rrect(c, -110, -60, 220, 120, 24, fill(WHITE))
        draw_text(c, price, 0, 30, 84, color=TEAL_D, weight="latin_black", align="center")
        draw_text(c, "প্রতিদিন সকালে একটু বদলায়", 0, 96, 28, color=(120, 112, 100), align="center")
        if t >= 18.2 and t < 20.6:
            c.drawCircle(0, 0, 90, stroke(GREEN, 5, int(200 * abs(math.sin(t * 3)))))
        c.restore()
    # review cycle diagram (92-103s)
    da = seg(t, 21.0, 22.4)
    if da > 0:
        c.save()
        c.translate(1240, 700)
        c.scale(da, da)
        rrect(c, -240, -170, 480, 340, 28, fill(WHITE))
        items = [("অর্ডার", -140, -60, TEAL), ("রিভিউ", 140, -60, ORANGE), ("আস্থা", 0, 100, GREEN)]
        for label, ix, iy, ic in items:
            c.drawCircle(ix, iy, 52, fill(ic, 30))
            c.drawCircle(ix, iy, 40, fill(ic))
            draw_text(c, label, ix, iy + 12, 28, color=WHITE, align="center")
        for (x1, y1, x2, y2, mid) in [(-90, -70, 90, -70, (-0, -150)), (170, 10, 60, 90, (150, 60)),
                                      (-60, 110, -170, 10, (-150, 70))]:
            path = skia.Path()
            path.moveTo(x1, y1)
            path.quadTo(mid[0], mid[1], x2, y2)
            c.drawPath(path, stroke((170, 178, 190), 6))
            ang = math.atan2(y2 - mid[1], x2 - mid[0])
            ax, ay = x2, y2
            p = skia.Path()
            p.moveTo(ax, ay)
            p.lineTo(ax - 16 * math.cos(ang - 0.4), ay - 16 * math.sin(ang - 0.4))
            p.lineTo(ax - 16 * math.cos(ang + 0.4), ay - 16 * math.sin(ang + 0.4))
            p.close()
            c.drawPath(p, fill((170, 178, 190)))
        c.restore()
    draw_text(c, "নতুন বিক্রেতার প্রথম চক্র", 1240, 960, 36, color=(110, 104, 92),
              align="center", opacity=seg(t, 22.4, 23.2) * (1 - seg(t, 27.0, 27.8)))


# ---------------- S6: the big buyer — typing & deleting ----------------
def sc_big_buyer(c, t, dur):
    vgrad(c, 0, 0, W, H, (15, 21, 39), (28, 37, 62))
    radial_glow(c, 960, 620, 620, (255, 190, 110), 34)
    # chat window
    wx, wy, ww, wh = 480, 130, 960, 800
    shadow_card(c, wx, wy, ww, wh, 24, bg=WHITE)
    rrect(c, wx, wy, ww, 84, 24, fill((18, 148, 144)))
    rrect(c, wx, wy + 50, ww, 34, 0, fill((18, 148, 144)))
    c.drawCircle(wx + 60, wy + 42, 26, fill(WHITE, 60))
    draw_text(c, "ক্রেতা", wx + 110, wy + 55, 36, color=WHITE, align="left")
    # buyer message (103-112s)
    b1 = seg(t, 0.6, 1.8)
    if b1 > 0:
        c.save()
        c.translate(wx + 40, wy + 150)
        c.scale(ease_out_back(seg(t, 0.6, 1.6)), ease_out_back(seg(t, 0.6, 1.6)))
        icon_bubble(c, 0, 0, 620, 96, bg=(238, 240, 244), tail="left")
        draw_text(c, "১০টা লোগো দরকার — হোয়াটসঅ্যাপে কথা বলি?", 30, -30, 30, color=INK)
        draw_text(c, "অর্থমূল্য এখনই দেব", 30, 12, 26, color=(110, 118, 130))
        c.restore()
    # second bubble: half payment
    b2 = seg(t, 10.6, 11.8)
    if b2 > 0:
        c.save()
        c.translate(wx + 40, wy + 300)
        c.scale(ease_out_back(seg(t, 10.6, 11.6)), ease_out_back(seg(t, 10.6, 11.6)))
        icon_bubble(c, 0, 0, 480, 76, bg=(238, 240, 244), tail="left")
        draw_text(c, "টাকা দেব অর্ধেক এখনই", 30, -20, 28, color=INK)
        c.restore()
    # azad reply — typing number then deleting (112-132s)
    typing = seg(t, 12.4, 13.4)
    if typing > 0:
        num = "+8801XXXXXXXXX"
        n_shown = int(clamp(seg(t, 13.0, 15.0)) * len(num))
        n_del = int(clamp(seg(t, 20.4, 22.0)) * len(num))
        shown = num[:max(0, n_shown - n_del)]
        # input field
        fx, fy, fw, fh = wx + 40, wy + wh - 110, ww - 80, 70
        rrect(c, fx, fy, fw, fh, 16, fill((240, 242, 246)))
        rrect(c, fx, fy, 6, fh, 3, fill(TEAL))
        cursor_on = (t % 1.0) < 0.55
        draw_text(c, shown, fx + 30, fy + 48, 34, color=INK, weight="latin")
        if cursor_on and 13.0 < t < 22.4:
            cw = text_width(shown, 34, "latin")
            c.drawRect(skia.Rect.MakeXYWH(fx + 34 + cw, fy + 16, 3, 40), fill(TEAL))
        # send button
        rrect(c, fx + fw - 90, fy + 10, 76, 50, 25, fill(TEAL, 90))
        path = skia.Path()
        path.moveTo(fx + fw - 62, fy + 24)
        path.lineTo(fx + fw - 38, fy + 35)
        path.lineTo(fx + fw - 62, fy + 46)
        path.close()
        c.drawPath(path, fill(WHITE, 180))
        # deleting puff
        if 20.4 < t < 21.6:
            da = seg(t, 20.4, 21.4)
            c.drawCircle(fx + 34 + text_width(shown, 34, "latin") + 20, fy + 35, 30 + da * 30,
                         stroke((200, 205, 214), 5, int(255 * (1 - da))))
    # azad at desk (right side, lit by screen)
    draw_desk(c, 1620, 880, 1.05, w=460, color=(58, 48, 44), top=(96, 78, 64))
    draw_chair(c, 1620, 1020, 1.05, color=(40, 46, 62))
    mood = "worried" if t > 22 else "talk"
    draw_person(c, 1620, 1020, 1.0, "type" if t < 22.4 else "sad", t=t, pal=AZAD, mood=mood)
    # caption
    aa = min(seg(t, 23.4, 24.6), 1 - seg(t, 38.0, 39.4))
    if aa > 0:
        draw_text(c, "নিজের নম্বর লিখল… তারপর পাঠানোর আগেই মুছে ফেলল", 960, 1010, 42,
                  color=(226, 233, 248), align="center", opacity=aa)
    # long pause beat (132-150s): clock + moon drift
    pa = seg(t, 40.0, 42.0)
    if pa > 0:
        # wall clock
        c.save()
        c.translate(240, 300)
        c.drawCircle(0, 0, 70, fill((30, 40, 64)))
        c.drawCircle(0, 0, 58, fill((226, 232, 244)))
        for i in range(12):
            ang = i * math.pi / 6
            c.drawLine(skia.Point(48 * math.sin(ang), -48 * math.cos(ang)),
                       skia.Point(54 * math.sin(ang), -54 * math.cos(ang)), stroke((120, 128, 142), 4))
        base = 40.0
        minute = (t - base) * 24 + 15
        hour = (t - base) * 2 + 10
        c.drawLine(skia.Point(0, 0), skia.Point(30 * math.sin(hour * math.pi / 180), -30 * math.cos(hour * math.pi / 180)), stroke(INK, 7))
        c.drawLine(skia.Point(0, 0), skia.Point(44 * math.sin(minute * math.pi / 180), -44 * math.cos(minute * math.pi / 180)), stroke(INK, 5))
        c.drawCircle(0, 0, 5, fill(CORAL))
        c.restore()
        aa2 = min(seg(t, 42.0, 43.5), 1 - seg(t, 55.0, 56.5))
        draw_text(c, "রাত গভীর হচ্ছে…", 240, 440, 38, color=(170, 182, 210), align="center", opacity=aa2)


# ---------------- S7: Imran bhai ----------------
def sc_imran(c, t, dur):
    vgrad(c, 0, 0, W, H, (247, 241, 230), (231, 222, 204))
    blob(c, W * 0.7, 260, 300, (250, 210, 150), 30, t)
    c.drawRect(skia.Rect.MakeXYWH(0, 940, W, H - 940), fill((214, 203, 182)))
    # chat panel
    wx, wy, ww, wh = 420, 120, 1080, 760
    shadow_card(c, wx, wy, ww, wh, 24, bg=WHITE)
    rrect(c, wx, wy, ww, 84, 24, fill((34, 44, 66)))
    rrect(c, wx, wy + 50, ww, 34, 0, fill((34, 44, 66)))
    c.drawCircle(wx + 60, wy + 42, 26, fill((70, 84, 112)))
    draw_text(c, "ইমরান ভাই", wx + 110, wy + 55, 36, color=WHITE)
    msgs = [
        ("left", 0.4, "ভাই, আসলে কী করার?"),
        ("right", 3.2, "সত্যিই কি এমন হচ্ছে?"),
        ("left", 5.4, "আমারও ৫০-৭০ ডলারের"),
        ("left", 7.2, "ছোট অর্ডারগুলাই আসছে"),
    ]
    y = wy + 150
    for side, t0, txt in msgs:
        aa = seg(t, t0, t0 + 0.8)
        if aa <= 0:
            continue
        wpx = text_width(txt, 32) + 60
        if side == "left":
            bx = wx + 40
            bgc = (238, 240, 244)
        else:
            bx = wx + ww - 40 - wpx
            bgc = (209, 244, 240)
        c.save()
        c.translate(bx, y + 76)
        c.scale(ease_out_back(seg(t, t0, t0 + 0.7)), ease_out_back(seg(t, t0, t0 + 0.7)))
        icon_bubble(c, 0, 0, wpx, 76, bg=bgc, tail=side)
        draw_text(c, txt, 30, -22, 32, color=INK)
        c.restore()
        y += 110
    # step back visual (181-184s)
    sb = seg(t, 30.0, 31.5)
    if sb > 0:
        draw_person(c, 1660, 1010, 1.1, "sad", t=t, pal=AZAD, mood="worried")
        aa = min(seg(t, 31.0, 32.0), 1 - seg(t, 31.5, 32.9))
        if aa > 0:
            draw_text(c, "এক ধাপ পিছিয়ে যেতে হলো", 1660, 830, 36, color=(140, 90, 60),
                      align="center", opacity=aa)
    else:
        draw_person(c, 1660, 1010, 1.1, "idle", t=t, pal=AZAD, mood="worried")
    # Imran figure
    ia = seg(t, 2.0, 3.2)
    if ia > 0:
        draw_person(c, 200, 1010, 1.15, "present", t=t + 0.5, pal=IMRAN, mood="talk", alpha=ia)


# ---------------- S8: November — ChatGPT arrives ----------------
def sc_chatgpt(c, t, dur):
    vgrad(c, 0, 0, W, H, (18, 24, 44), (34, 44, 76))
    stars(c, t, n=50, alpha=0.6)
    bg_grid(c, (140, 170, 230), 10, 120)
    # calendar flip to November (184-187s)
    ca = seg(t, 0.4, 1.6)
    if ca > 0:
        c.save()
        c.translate(300, 330)
        c.scale(ease_out_back(ca) * 1.4, ease_out_back(ca) * 1.4)
        icon_calendar(c, 0, 0, 1.0, label="NOV", head=CORAL)
        c.restore()
        draw_text(c, "নভেম্বর", 300, 520, 44, color=(226, 233, 248), align="center",
                  opacity=seg(t, 1.0, 1.8))
    # AI orb descends into hands (187-190s)
    oa = seg(t, 3.4, 4.8)
    oy = lerp(-100, 620, ease_out_cubic(oa))
    if oa > 0:
        icon_ai_chip(c, 960, oy, 1.6, t=t)
        # beams to phones
        ba = seg(t, 4.6, 5.8)
        if ba > 0:
            for px, py in [(400, 760), (1520, 760)]:
                path = skia.Path()
                path.moveTo(960, oy)
                path.quadTo((960 + px) / 2, (oy + py) / 2 - 120, px, py)
                c.drawPath(path, stroke((120, 220, 255), 6, int(160 * ba)))
            for px, py in [(400, 760), (1520, 760)]:
                icon_phone(c, px, py, 1.4)
                c.drawCircle(px, py + 4, 26 + 10 * pulse(t, 1.6), fill((120, 220, 255), int(120 * ba)))
    # research intro (188-200s)
    ra = seg(t, 6.6, 8.0)
    if ra > 0:
        cards = [("Harvard Business School", 0), ("Imperial College London", 1), ("জার্মান গবেষণা প্রতিষ্ঠান", 2)]
        for i, (name, _) in enumerate(cards):
            aa = seg(t, 8.0 + i * 0.8, 9.2 + i * 0.8)
            if aa <= 0:
                continue
            cx = 480 + i * 480
            c.save()
            c.translate(cx, 880)
            c.scale(ease_out_back(aa), ease_out_back(aa))
            shadow_card(c, -210, -110, 420, 220, 20, bg=WHITE, alpha=aa)
            c.drawCircle(0, -40, 34, fill([CORAL, (0, 125, 195), GOLD][i]))
            draw_text(c, ["H", "IC", "DE"][i], 0, -22, 40, color=WHITE, weight="latin_black", align="center")
            draw_text(c, name, 0, 60, 26 if i < 2 else 30, color=INK, align="center")
            c.restore()
        aa2 = min(seg(t, 10.6, 11.8), 1 - seg(t, 14.6, 16.0))
        if aa2 > 0:
            draw_text(c, "১৪ মাসের ডেটা বিশ্লেষণ", 960, 1010, 44, color=(240, 205, 130),
                      align="center", opacity=aa2)


# ---------------- S9: the research findings ----------------
def sc_research(c, t, dur):
    vgrad(c, 0, 0, W, H, (245, 242, 235), (228, 222, 210))
    bg_grid(c, (160, 150, 130), 10, 120)
    # left: buyer makes logo himself in 1 second (200-214s)
    la = seg(t, 0.6, 2.0)
    if la > 0:
        aa = la * (1 - seg(t, 50.0, 52.0))
        if aa > 0:
            c.save()
            c.translate(400, 480)
            c.scale(aa, aa)
            # buyer person
            draw_person(c, -160, 330, 0.95, "idle", t=t, mood="happy")
            # before: $5 tag crossed
            rrect(c, -320, -160, 190, 80, 18, fill(WHITE))
            draw_text(c, "$5", -225, -100, 52, color=GREY_D, weight="latin_black", align="center")
            c.drawLine(skia.Point(-310, -95), skia.Point(-140, -140), stroke(CORAL, 8))
            # arrow
            path = skia.Path()
            path.moveTo(-110, -120)
            path.lineTo(60, -120)
            c.drawPath(path, stroke(TEAL, 8))
            p = skia.Path()
            p.moveTo(60, -120)
            p.lineTo(38, -134)
            p.lineTo(38, -106)
            p.close()
            c.drawPath(p, fill(TEAL))
            # AI sparkle
            icon_ai_chip(c, 190, -120, 1.1, t=t)
            draw_text(c, "১ সেকেন্ডে নিজেই", 60, 30, 34, color=TEAL_D, align="center")
            c.restore()
    # right: bar chart $1000 -> $14 (240-246s area)
    ba = seg(t, 4.0, 5.4)
    if ba > 0:
        c.save()
        c.translate(1340, 560)
        c.scale(ba, ba)
        shadow_card(c, -330, -330, 660, 620, 26, bg=WHITE)
        draw_text(c, "গ্রাফিক কাজের বাজেট", 0, -270, 36, color=INK, align="center")
        # before bar
        hb = 380 * ease_out_cubic(seg(t, 5.4, 7.0))
        rrect(c, -220, 240 - hb, 150, hb, 12, fill(TEAL))
        draw_text(c, "$1000", -145, 240 - hb - 26, 40, color=TEAL_D, weight="latin_black", align="center")
        # after bar
        ha = 12 * ease_out_cubic(seg(t, 7.4, 8.4)) + 8
        rrect(c, 70, 240 - ha - 8, 150, max(10, ha), 12, fill(CORAL))
        draw_text(c, "$14", 145, 240 - ha - 46, 40, color=CORAL, weight="latin_black", align="center")
        c.drawLine(skia.Point(-260, 240), skia.Point(260, 240), stroke((200, 206, 216), 5))
        draw_text(c, "আগে", -145, 290, 28, color=(120, 112, 100), align="center")
        draw_text(c, "এখন", 145, 290, 28, color=(120, 112, 100), align="center")
        c.restore()
    # -30% professionals (249-253s)
    da = seg(t, 8.6, 9.8)
    if da > 0:
        c.save()
        c.translate(1340, 950)
        c.scale(ease_out_back(da), ease_out_back(da))
        rrect(c, -230, -60, 460, 120, 24, fill((255, 236, 232)))
        draw_text(c, "প্রফেশনালদের রেট", -80, -8, 30, color=(150, 60, 50), align="center")
        draw_text(c, "-৩০%", 130, 6, 52, color=CORAL, weight="bold", align="center")
        c.restore()
    # bottom caption
    aa = min(seg(t, 2.2, 3.4), 1 - seg(t, 48.0, 49.6))
    if aa > 0:
        draw_text(c, "যে কাজ $৫-এ কিনত, এখন সেটা AI দিয়ে নিজেই বানায়", 960, 1010, 42,
                  color=(90, 84, 70), align="center", opacity=aa)


# ---------------- S10: Fiverr AI-first & the decline ----------------
def sc_fiverr_report(c, t, dur):
    vgrad(c, 0, 0, W, H, (16, 22, 42), (30, 40, 68))
    stars(c, t, n=40, alpha=0.5)
    bg_grid(c, (120, 150, 210), 9, 120)
    # identical $5 gigs everywhere (253.7-264.7)
    ga = seg(t, 0.4, 1.6)
    if ga > 0:
        fade = ga * (1 - seg(t, 9.6, 11.2))
        if fade > 0:
            rnd = 31.0
            for i in range(8):
                rnd = (rnd * 9301 + 49297) % 233280
                r1 = rnd / 233280
                rnd = (rnd * 9301 + 49297) % 233280
                r2 = rnd / 233280
                gx = 200 + (i % 4) * 420 + math.sin(t * 0.6 + i) * 6
                gy = 260 + (i // 4) * 330 + math.cos(t * 0.5 + i * 1.3) * 6
                aa = fade * ease_out_back(seg(t, 0.6 + i * 0.18, 1.8 + i * 0.18))
                if aa <= 0:
                    continue
                c.save()
                c.translate(gx, gy)
                c.scale(0.62 * aa, 0.62 * aa)
                gig_card(c, -170, -125, 1.0, price="$5", alpha=1.0)
                c.restore()
            aa2 = min(seg(t, 2.0, 3.2), 1 - seg(t, 9.0, 10.4))
            draw_text(c, "হাজারো নতুন ফ্রিল্যান্সার — একই $৫ গিগ", 960, 950, 44,
                      color=(226, 233, 248), align="center", opacity=aa2)
    # AI-FIRST announcement + layoffs (264.7-276.7)
    an = seg(t, 11.4, 12.8)
    if an > 0:
        aa1 = an * (1 - seg(t, 32.0, 33.6))
        if aa1 > 0:
            c.save()
            c.translate(560, 320)
            c.scale(ease_out_back(seg(t, 11.4, 12.8)) * 1.1, ease_out_back(seg(t, 11.4, 12.8)) * 1.1)
            shadow_card(c, -260, -110, 520, 220, 26, bg=WHITE, alpha=aa1)
            draw_text(c, "AI-FIRST", 0, 10, 76, color=(40, 200, 170), weight="latin_black", align="center")
            draw_text(c, "সেপ্টেম্বরে কোম্পানির ঘোষণা", 0, 76, 30, color=(120, 112, 100), align="center")
            c.restore()
        # workers fading out (272.7-276.7 -> t 19-23)
        ly = seg(t, 19.0, 20.2)
        if ly > 0:
            c.save()
            c.translate(1400, 320)
            rnd = 23.0
            for i in range(12):
                rnd = (rnd * 9301 + 49297) % 233280
                r1 = rnd / 233280
                gx = -220 + (i % 6) * 88
                gy = -60 + (i // 6) * 120
                gone = clamp(seg(t, 20.2 + r1 * 3.0, 21.8 + r1 * 3.0))
                c.save()
                c.translate(gx, gy + gone * 220)
                c.rotate(gone * 40 * (1 if i % 2 else -1))
                alpha = ly * (1 - gone * 0.9)
                c.drawCircle(0, -30, 22, fill((150, 160, 180), int(255 * alpha)))
                rrect(c, -26, -8, 52, 56, 18, fill((150, 160, 180), int(255 * alpha)))
                c.restore()
            aa2 = min(seg(t, 19.2, 20.4), 1 - seg(t, 30.0, 31.4))
            draw_text(c, "হাজারো কর্মী ছাঁটাই", 1400, 560, 36, color=(240, 170, 140), align="center", opacity=aa2)
            c.restore()
    # October report: buyers down (276.7-287.7 -> t 23-34)
    ra = seg(t, 23.4, 24.8)
    if ra > 0:
        c.save()
        c.translate(960, 780)
        shadow_card(c, -500, -240, 1000, 400, 26, bg=(24, 34, 58))
        draw_text(c, "অক্টোবরের রিপোর্ট", -360, -170, 34, color=(226, 233, 248), align="left")
        # buyer crowd shrinking
        n0, n1 = 24, 13
        shr = ease_in_out(seg(t, 25.6, 30.0))
        for i in range(n0):
            gx = -420 + (i % 12) * 70
            gy = -60 + (i // 12) * 110
            gone = clamp(seg(shr * n0, i, i + 1))
            alpha = (1 - gone * 0.95)
            c.drawCircle(gx, gy - 26, 16, fill((150, 160, 180), int(255 * alpha)))
            rrect(c, gx - 19, gy - 6, 38, 40, 13, fill((150, 160, 180), int(255 * alpha)))
        aa3 = min(seg(t, 26.0, 27.2), 1 - seg(t, 36.4, 37.8))
        draw_text(c, "ক্রেতা কমেছে ২ লাখ+", 240, 60, 44, color=(250, 190, 130), align="center", opacity=aa3)
        c.restore()
    # market price falling (287.7-293.7 -> t 34-40)
    ma = seg(t, 34.2, 35.4)
    if ma > 0:
        c.save()
        c.translate(1500, 760)
        c.scale(ma, ma)
        shadow_card(c, -180, -160, 360, 320, 22, bg=WHITE)
        draw_text(c, "মার্কেট প্রাইস", 0, -110, 30, color=INK, align="center")
        pts = [(0.0, 0.8), (0.5, 0.55), (1.0, 0.2)]
        icon_chart_line(c, -130, -70, 260, 160, pts, color=CORAL, lw=9,
                        t=seg(t, 35.4, 38.4))
        draw_text(c, "প্রায় $৩০০", 0, 120, 34, color=CORAL, weight="bold", align="center")
        c.restore()


# ---------------- S11: that night — the quiet exit & balcony ----------------
def sc_that_night(c, t, dur):
    vgrad(c, 0, 0, W, H, (14, 20, 38), (28, 37, 62))
    stars(c, t, n=60, alpha=0.7)
    # room with desk (holds through 316.7 -> t 23)
    room_a = 1 - seg(t, 23.0, 24.4)
    if room_a > 0:
        c.save()
        c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * room_a))
        radial_glow(c, 960, 640, 560, (255, 190, 110), 36 * room_a)
        draw_desk(c, 960, 880, 1.4, w=900, color=(58, 48, 44), top=(96, 78, 64))
        draw_chair(c, 960, 1040, 1.25, color=(40, 46, 62))
        draw_person(c, 960, 1040, 1.2, "type" if t < 23 else "sad", t=t, pal=AZAD,
                    mood="worried", laptop=True)
        # AI chat search beat (296.7-306.7 -> t 3-13)
        sa = seg(t, 3.4, 4.8)
        if sa > 0:
            aa3 = sa * (1 - seg(t, 12.6, 14.0))
            if aa3 > 0:
                c.save()
                c.translate(420, 380)
                rrect(c, -230, -46, 460, 92, 46, fill(WHITE, int(255 * aa3)))
                icon_search(c, -180, 0, 1.1, color=(150, 158, 170))
                draw_text(c, "আগে: গুগল সার্চ", -130, 12, 32, color=(150, 158, 170), opacity=aa3)
                c.restore()
                c.save()
                c.translate(420, 560)
                aa4 = seg(t, 5.4, 6.6)
                if aa4 > 0:
                    icon_bubble(c, -230, 46, 460, 92, bg=(30, 42, 66), tail="left", alpha=aa4)
                    icon_robot(c, -180, 0, 0.9, t=t)
                    draw_text(c, "এখন: সরাসরি AI-কে জিজ্ঞেস", -120, 4, 30, color=(226, 233, 248), opacity=aa4)
                c.restore()
        # 2027 traffic chart (306.7-312.7 -> t 13-19)
        ta = seg(t, 13.4, 14.8)
        if ta > 0:
            c.save()
            c.translate(1420, 460)
            shadow_card(c, -300, -230, 600, 400, 22, bg=(24, 34, 58), alpha=ta)
            draw_text(c, "ভিজিটর ২০২৭ পর্যন্ত কমতে পারে", 0, -180, 30, color=(240, 200, 150),
                      align="center", opacity=ta)
            pts = [(0.0, 0.85), (0.33, 0.7), (0.66, 0.45), (1.0, 0.2)]
            icon_chart_line(c, -240, -140, 480, 240, pts, color=CORAL, lw=9,
                            area=(239, 68, 68), t=seg(t, 14.8, 18.6))
            c.restore()
        # buyers never reach the gig (312.7-316.7 -> t 19-23)
        va = seg(t, 19.2, 20.4)
        if va > 0:
            aa5 = va * (1 - seg(t, 22.6, 23.8))
            if aa5 > 0:
                c.save()
                c.translate(420, 780)
                c.scale(0.8 * aa5, 0.8 * aa5)
                gig_card(c, -170, -125, 1.0, price="$5", alpha=aa5)
                c.restore()
                # visitor dots fading before reaching card
                for i in range(6):
                    dx = 700 + i * 40
                    fade_i = clamp(seg(t, 19.6 + i * 0.28, 20.4 + i * 0.28))
                    c.drawCircle(dx, 760 + math.sin(i * 2.1) * 30, 8,
                                 fill((150, 160, 180), int(255 * aa5 * (1 - fade_i))))
                aa6 = min(seg(t, 20.2, 21.4), 1 - seg(t, 22.4, 23.6))
                draw_text(c, "ক্রেতা গিগে পৌঁছানোর আগেই…", 420, 960, 36, color=(200, 210, 235),
                          align="center", opacity=aa6)
        # closing gig + laptop (316.7-321.7 -> t 23-28)
        cl = seg(t, 23.4, 24.6)
        if cl > 0:
            c.save()
            c.translate(1500, 400)
            c.rotate(cl * 0.25)
            c.scale(1 - 0.55 * cl, 1 - 0.55 * cl)
            gig_card(c, -170, -125, 1.0, price="$5", alpha=1 - cl * 0.9)
            c.restore()
            aa7 = min(seg(t, 24.0, 25.2), 1 - seg(t, 27.0, 28.2))
            draw_text(c, "সেই রাতে গিগের পেজ বন্ধ, ল্যাপটপে ঢাকনা", 960, 1000, 40,
                      color=(226, 233, 248), align="center", opacity=aa7)
        c.restore()
    # balcony scene (321.7-325.7 -> t 28-32)
    ba = seg(t, 28.0, 29.4)
    if ba > 0:
        c.save()
        c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * ba))
        vgrad(c, 0, 0, W, H, (10, 16, 30), (28, 40, 70))
        stars(c, t, n=100, alpha=ba)
        sun_moon(c, 1500, 220, 54, night=True, t=t, alpha=ba)
        skyline(c, 700, t, 1.0, color=(16, 26, 46), windows=(250, 210, 130), alpha=ba, seed=13.0)
        skyline(c, 760, t, 0.65, color=(10, 18, 34), windows=(240, 200, 120), alpha=ba, seed=17.0)
        c.drawRect(skia.Rect.MakeXYWH(0, 860, W, H - 860), fill((24, 32, 52), int(255 * ba)))
        for i in range(14):
            c.drawLine(skia.Point(60 + i * 140, 640), skia.Point(60 + i * 140, 880),
                       stroke((40, 52, 78), 10, int(255 * ba)))
        c.drawLine(skia.Point(0, 640), skia.Point(W, 640), stroke((52, 66, 94), 14, int(255 * ba)))
        draw_person(c, 960, 880, 1.35, "lean", t=t, pal=AZAD, mood="sad", alpha=ba, look="down")
        aa = min(seg(t, 29.6, 30.8), 1)
        if aa > 0:
            draw_text(c, "এক মাস পর — বারান্দার রেলিংয়ে হেলান", 960, 1000, 40,
                      color=(200, 210, 235), align="center", opacity=aa)
        c.restore()
