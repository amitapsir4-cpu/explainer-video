"""Vector graphics library: palettes, primitives, characters, icons, environments."""
import math
import skia
from text_engine import draw_text, text_width, C
from util import (clamp, lerp, ease_in_out, ease_out, ease_out_cubic, ease_out_back,
                  ease_out_elastic, pulse, seg, smooth_noise)

W, H = 1920, 1080

# ---------- palette ----------
INK = (16, 26, 43)          # deep navy ink
CREAM = (247, 242, 232)
CREAM2 = (238, 230, 215)
NAVY = (13, 22, 38)
NAVY2 = (22, 34, 56)
TEAL = (16, 150, 138)
TEAL_D = (10, 105, 97)
ORANGE = (245, 158, 11)
CORAL = (239, 68, 68)
GREEN = (34, 197, 94)
GOLD = (234, 179, 8)
WHITE = (255, 255, 255)
GREY = (148, 155, 168)
GREY_D = (90, 98, 112)

AZAD = dict(skin=(232, 185, 138), hair=(31, 27, 30), shirt=(18, 148, 144), shirt2=(12, 110, 106), pants=(38, 50, 74))
MOM = dict(skin=(226, 178, 132), hair=(40, 32, 30), shirt=(178, 46, 74), shirt2=(140, 32, 56), pants=(178, 46, 74), sari=True)
IMRAN = dict(skin=(214, 165, 120), hair=(70, 62, 58), shirt=(222, 146, 32), shirt2=(180, 112, 20), pants=(52, 60, 80), beard=True)


def col(c, a=255):
    return C(c[0], c[1], c[2], a)


def P(**kw):
    return skia.Paint(AntiAlias=True, **kw)


def fill(c, a=255, **kw):
    return skia.Paint(AntiAlias=True, Color=col(c, a), **kw)


def stroke(c, w, a=255, cap=skia.Paint.kRound_Cap):
    return skia.Paint(AntiAlias=True, Color=col(c, a), Style=skia.Paint.kStroke_Style,
                      StrokeWidth=w, StrokeCap=cap, StrokeJoin=skia.Paint.kRound_Join)


def rrect(c, x, y, w, h, r, paint):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint)


def vgrad(c, x, y, w, h, c1, c2, a1=255, a2=255):
    shader = skia.GradientShader.MakeLinear(
        [skia.Point(x, y), skia.Point(x, y + h)],
        [col(c1, a1), col(c2, a2)], None)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(Shader=shader, AntiAlias=False))


def radial_glow(c, x, y, r, color, alpha=70):
    shader = skia.GradientShader.MakeRadial(
        skia.Point(x, y), r, [col(color, alpha), col(color, 0)], None)
    c.drawRect(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), skia.Paint(Shader=shader, AntiAlias=True))


def shadow_card(c, x, y, w, h, r, bg=WHITE, sd=(20, 30, 50, 60), sd_dy=14, sd_r=30, alpha=1.0):
    a = int(sd[3] * alpha)
    sh = skia.Paint(AntiAlias=True, Color=col(sd[:3], a),
                    MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sd_r))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y + sd_dy, w, h), r, r), sh)
    c.save()
    if alpha < 1.0:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(x - 20, y - 20, w + 40, h + 40), int(255 * alpha))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), fill(bg))
    if alpha < 1.0:
        c.restore()
    c.restore()


def soft_shadow(c, x, y, rx, ry, color=(20, 30, 50), alpha=60, blur=24):
    p = skia.Paint(AntiAlias=True, Color=col(color, alpha),
                   MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    c.drawOval(skia.Rect.MakeXYWH(x - rx, y - ry, 2 * rx, 2 * ry), p)


def vignette(c, strength=0.16):
    shader = skia.GradientShader.MakeRadial(
        skia.Point(W / 2, H / 2), W * 0.75,
        [col((0, 0, 0), 0), col((0, 0, 0), int(255 * strength))], None)
    c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Shader=shader))


def grain_free_grade(c, warm=0.0, cool=0.0, alpha=0.10):
    if warm > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), fill((255, 180, 90), int(255 * warm * alpha)))
    if cool > 0:
        c.drawRect(skia.Rect.MakeWH(W, H), fill((80, 120, 255), int(255 * cool * alpha)))


# ---------- characters ----------
def _limb(c, x, y, a1, a2, l1, l2, w1, w2, color, hand_color=None, hand_r=None):
    """Two-segment limb. Angles in radians, 0 = down, positive = towards +x."""
    x1 = x + math.sin(a1) * l1
    y1 = y + math.cos(a1) * l1
    c.drawLine(skia.Point(x, y), skia.Point(x1, y1), stroke(color, w1))
    x2 = x1 + math.sin(a1 + a2) * l2
    y2 = y1 + math.cos(a1 + a2) * l2
    c.drawLine(skia.Point(x1, y1), skia.Point(x2, y2), stroke(color, w2))
    if hand_color is not None:
        c.drawCircle(x2, y2, hand_r, fill(hand_color))
    return x2, y2, a1 + a2


def draw_person(c, x, y, s, pose="idle", t=0.0, pal=AZAD, mood="neutral", flip=False,
                alpha=1.0, walk_phase=0.0, laptop=False, phone=None, look=None):
    """Flat vector person. (x,y) = ground point between feet. s = scale (1 ~= 300px tall).
    pose: idle|sit|walk|stand|phone|sad|present|type|celebrate|lean
    mood: neutral|happy|sad|worried|smile_open|talk
    """
    c.save()
    c.translate(x, y)
    c.scale(s if not flip else -s, s)
    if alpha < 1.0:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(-260, -420, 520, 440), int(255 * alpha))

    skin, hair, shirt, shirt2, pants = pal["skin"], pal["hair"], pal["shirt"], pal["shirt2"], pal["pants"]
    blink = 1.0 if (t % 3.7) > 0.12 else 0.12
    bob = math.sin(t * 2.1) * 3.0
    breathe = math.sin(t * 2.1) * 1.5

    # ---- pose parameters ----
    lean = 0.0
    head_tilt = 0.0
    armL = (0.25, 0.35)   # (shoulder, elbow) angles
    armR = (-0.25, -0.35)
    legL = (0.06, -0.02)
    legR = (-0.06, 0.02)
    sit = False
    crouch = 0.0
    if pose == "walk":
        ph = walk_phase
        legL = (math.sin(ph) * 0.55, -0.35 + 0.25 * math.sin(ph + 1.2))
        legR = (math.sin(ph + math.pi) * 0.55, -0.35 + 0.25 * math.sin(ph + math.pi + 1.2))
        armL = (0.35 + math.sin(ph + math.pi) * 0.45, 0.3)
        armR = (-0.35 + math.sin(ph) * 0.45, -0.3)
        bob = abs(math.sin(ph)) * -5
    elif pose == "sit":
        sit = True
        crouch = 1.0
        armL = (0.9, 0.9)
        armR = (-0.9, -0.9)
    elif pose == "type":
        sit = True
        crouch = 1.0
        ty = math.sin(t * 7) * 0.06
        armL = (1.05 + ty, 1.15)
        armR = (-1.05 - ty, -1.15)
    elif pose == "phone":
        armR = (-2.35, -0.55)
        armL = (0.3, 0.4)
        head_tilt = 0.06
    elif pose == "sad":
        lean = 0.16
        head_tilt = 0.22
        armL = (0.12, 0.15)
        armR = (-0.12, -0.15)
        bob += 6
    elif pose == "present":
        armR = (-1.25, -0.45)
        armL = (0.35, 0.3)
    elif pose == "celebrate":
        armL = (2.6, 0.15)
        armR = (-2.6, -0.15)
        mood = "happy"
    elif pose == "lean":
        lean = 0.05
        armL = (0.2, 0.2)
        armR = (-0.2, -0.2)

    hip_y = -150 + bob + crouch * 62
    shoulder_y = hip_y - 92
    head_y = shoulder_y - 52
    if sit:
        hip_y = -128 + bob * 0.4
        shoulder_y = hip_y - 90
        head_y = shoulder_y - 50

    body_p = fill(shirt)
    # legs
    if not sit:
        _limb(c, -16, hip_y + 6, legL[0], legL[1], 62, 58, 26, 22, pants)
        _limb(c, 16, hip_y + 6, legR[0], legR[1], 62, 58, 26, 22, pants)
        # shoes
    else:
        # sitting: thighs forward, shins down
        for sx in (-16, 16):
            kx = sx + math.sin(1.35) * 58
            ky = hip_y + 6 + math.cos(1.35) * 58
            c.drawLine(skia.Point(sx, hip_y + 6), skia.Point(kx, ky), stroke(pants, 26))
            c.drawLine(skia.Point(kx, ky), skia.Point(kx, ky + 62), stroke(pants, 22))

    # torso (rounded)
    c.save()
    c.translate(0, shoulder_y)
    c.rotate(math.degrees(lean))
    c.translate(0, -shoulder_y)
    rrect(c, -34, shoulder_y - 8, 68, hip_y - shoulder_y + 26, 26, body_p)
    # collar detail
    c.drawCircle(0, shoulder_y + 14, 9, fill(shirt2))
    # back arm
    arm_back = armL if not flip else armR
    _limb(c, -30, shoulder_y + 16, arm_back[0], arm_back[1], 46, 42, 20, 17, shirt2,
          hand_color=skin, hand_r=11)
    # head
    c.save()
    c.translate(0, head_y)
    c.rotate(math.degrees(head_tilt + (lean * 0.5)))
    neck = skia.Rect.MakeXYWH(-11, 30, 22, 26)
    c.drawRect(neck, fill(skin))
    c.drawCircle(0, 0, 36, fill(skin))
    # hair
    if pal.get("sari"):
        # headscarf
        hair_p = fill(hair)
        path = skia.Path()
        path.addArc(skia.Rect.MakeXYWH(-40, -40, 80, 80), 200, 140)
        c.drawPath(path, fill(pal["shirt"]))
        c.drawCircle(0, -12, 37, fill(pal["shirt"]))
        c.drawCircle(0, 0, 30, fill(skin))
        c.drawCircle(0, -14, 30, fill(pal["shirt"]))
    else:
        path = skia.Path()
        path.addArc(skia.Rect.MakeXYWH(-38, -40, 76, 76), 195, 150)
        c.drawPath(path, fill(hair))
        c.drawCircle(-16, -14, 14, fill(hair))
        c.drawCircle(16, -14, 14, fill(hair))
        c.drawCircle(0, -22, 20, fill(hair))
    if pal.get("beard"):
        rrect(c, -22, 6, 44, 30, 14, fill(hair))
        c.drawCircle(0, 26, 16, fill(hair))
    # face
    ex, ey = 13, 2
    if look == "left":
        ex, ey = -13, 2
    elif look == "up":
        ex, ey = 0, -6
    elif look == "down":
        ex, ey = 0, 8
    eye_h = 5.5 * blink
    c.drawOval(skia.Rect.MakeXYWH(ex - 5.5 - 9, ey - eye_h, 11, eye_h * 2), fill((28, 24, 26)))
    c.drawOval(skia.Rect.MakeXYWH(ex - 5.5 + 9, ey - eye_h, 11, eye_h * 2), fill((28, 24, 26)))
    # brows
    brow_dy = {"sad": 6, "worried": 4, "happy": -3}.get(mood, -1)
    bw = 12
    if mood in ("sad", "worried"):
        c.drawLine(skia.Point(ex - 15, ey - 12 + brow_dy), skia.Point(ex - 4, ey - 15 + brow_dy * 0.4), stroke(hair, 4))
        c.drawLine(skia.Point(ex + 4, ey - 15 + brow_dy * 0.4), skia.Point(ex + 15, ey - 12 + brow_dy), stroke(hair, 4))
    else:
        c.drawLine(skia.Point(ex - 14, ey - 13 + brow_dy), skia.Point(ex - 4, ey - 14 + brow_dy), stroke(hair, 4))
        c.drawLine(skia.Point(ex + 4, ey - 14 + brow_dy), skia.Point(ex + 14, ey - 13 + brow_dy), stroke(hair, 4))
    # nose
    c.drawLine(skia.Point(ex, ey + 4), skia.Point(ex + 2, ey + 10), stroke(tuple(max(0, v - 60) for v in skin), 3))
    # mouth
    my = ey + 20
    if mood == "happy":
        path = skia.Path()
        path.moveTo(ex - 12, my - 2)
        path.quadTo(ex, my + 10, ex + 12, my - 2)
        path.close()
        c.drawPath(path, fill((120, 46, 52)))
    elif mood == "smile_open":
        path = skia.Path()
        path.moveTo(ex - 11, my - 2)
        path.quadTo(ex, my + 12, ex + 11, my - 2)
        path.close()
        c.drawPath(path, fill((120, 46, 52)))
        c.drawPath(path, fill(WHITE, 200) if False else fill((120, 46, 52)))
    elif mood == "sad":
        path = skia.Path()
        path.moveTo(ex - 10, my + 3)
        path.quadTo(ex, my - 5, ex + 10, my + 3)
        c.drawPath(path, stroke((120, 60, 60), 4))
    elif mood == "worried":
        c.drawLine(skia.Point(ex - 9, my + 2), skia.Point(ex + 9, my + 1), stroke((120, 60, 60), 4))
    elif mood == "talk":
        ph = (t * 6) % 1.0
        hh = 4 + 6 * math.sin(ph * math.pi)
        path = skia.Path()
        path.moveTo(ex - 9, my - 1)
        path.quadTo(ex, my + hh, ex + 9, my - 1)
        path.close()
        c.drawPath(path, fill((120, 46, 52)))
    else:
        c.drawLine(skia.Point(ex - 10, my + 2), skia.Point(ex + 10, my + 2), stroke((120, 60, 60), 4))
    c.restore()  # head

    # front arm
    arm_front = armR if not flip else armL
    hx, hy, hand_a = _limb(c, 30, shoulder_y + 16, arm_front[0], arm_front[1], 46, 42, 20, 17, shirt,
                           hand_color=skin, hand_r=11)
    c.restore()  # torso lean

    # props
    if phone is not None:
        px, py = hx + 6, hy + 4
        c.save()
        c.translate(px, py)
        c.rotate(math.degrees(-0.9))
        rrect(c, -11, -22, 22, 42, 6, fill((24, 28, 36)))
        rrect(c, -8, -18, 16, 32, 3, fill((90, 200, 250)))
        c.restore()

    if laptop and sit:
        # laptop in front of seated person
        c.save()
        c.translate(0, -58)
        rrect(c, -70, 8, 140, 10, 4, fill((52, 60, 76)))
        c.save()
        c.translate(-70, 8)
        c.rotate(-14)
        rrect(c, 0, -88, 140, 90, 6, fill((40, 48, 62)))
        rrect(c, 6, -82, 128, 78, 4, fill((120, 200, 255, 235)))
        c.restore()
        c.restore()

    if alpha < 1.0:
        c.restore()
    c.restore()


def draw_chair(c, x, y, s, color=(70, 78, 96)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -52, -118, 104, 20, 9, fill(color))          # seat
    rrect(c, -50, -112, 12, 112, 6, fill(color))          # back leg
    rrect(c, 38, -112, 12, 112, 6, fill(color))           # front leg
    rrect(c, -58, -196, 16, 90, 8, fill(color))           # backrest
    c.restore()


def draw_desk(c, x, y, s, w=560, color=(94, 78, 64), top=(120, 100, 82)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -w / 2, -26, w, 22, 8, fill(top))
    rrect(c, -w / 2 + 30, -4, 18, 90, 6, fill(color))
    rrect(c, w / 2 - 48, -4, 18, 90, 6, fill(color))
    c.restore()


def draw_laptop_open(c, x, y, s, screen=(126, 205, 255), content=None):
    """Open laptop facing viewer-left. (x,y)=bottom center of base."""
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -95, -12, 190, 14, 5, fill((52, 60, 76)))
    c.save()
    c.translate(-95, -10)
    c.rotate(-16)
    rrect(c, 0, -120, 190, 122, 7, fill((40, 48, 62)))
    rrect(c, 8, -112, 174, 106, 4, fill(screen))
    if content == "gig":
        rrect(c, 20, -100, 150, 34, 5, fill(WHITE))
        rrect(c, 20, -58, 110, 12, 4, fill((200, 206, 216)))
        rrect(c, 20, -40, 80, 12, 4, fill((200, 206, 216)))
    elif content == "chat":
        rrect(c, 18, -102, 120, 26, 6, fill(WHITE))
        rrect(c, 44, -68, 120, 26, 6, fill((18, 148, 144)))
        rrect(c, 18, -34, 100, 26, 6, fill(WHITE))
    c.restore()
    c.restore()


# ---------- icons ----------
def icon_dollar(c, x, y, s, color=WHITE, ring=None):
    if ring:
        c.drawCircle(x, y, s * 1.25, fill(ring))
    draw_text(c, "$", x, y + s * 0.85, s * 1.7, color=color, weight="latin_black", align="center")


def icon_star(c, x, y, s, color=GOLD, filled=True):
    path = skia.Path()
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = s if i % 2 == 0 else s * 0.45
        px, py = x + math.cos(ang) * r, y + math.sin(ang) * r
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()
    c.drawPath(path, fill(color) if filled else stroke(color, s * 0.18))


def icon_laptop(c, x, y, s, color=(40, 48, 62), screen=(126, 205, 255)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.save()
    c.translate(-44, 0)
    c.rotate(-16)
    rrect(c, 0, -62, 88, 64, 4, fill(color))
    rrect(c, 5, -57, 78, 54, 2, fill(screen))
    c.restore()
    rrect(c, -52, -4, 104, 8, 3, fill((70, 80, 96)))
    c.restore()


def icon_phone(c, x, y, s, color=(24, 28, 36), screen=(90, 200, 250)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -14, -26, 28, 52, 7, fill(color))
    rrect(c, -10, -20, 20, 38, 3, fill(screen))
    c.restore()


def icon_ai_chip(c, x, y, s, t=0.0, body=(18, 148, 144), glow=True):
    if glow:
        radial_glow(c, x, y, s * 2.6, body, int(60 + 30 * pulse(t, 2.4)))
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -22, -22, 44, 44, 9, fill(body))
    rrect(c, -13, -13, 26, 26, 5, fill(WHITE, 235))
    for i in (-10, 0, 10):
        c.drawLine(skia.Point(i, -30), skia.Point(i, -22), stroke(body, 4))
        c.drawLine(skia.Point(i, 22), skia.Point(i, 30), stroke(body, 4))
        c.drawLine(skia.Point(-30, i), skia.Point(-22, i), stroke(body, 4))
        c.drawLine(skia.Point(22, i), skia.Point(30, i), stroke(body, 4))
    c.restore()


def icon_robot(c, x, y, s, t=0.0, body=(90, 100, 120)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawLine(skia.Point(0, -34), skia.Point(0, -46), stroke(body, 5))
    c.drawCircle(0, -50, 5, fill(CORAL))
    rrect(c, -26, -34, 52, 44, 12, fill(body))
    rrect(c, -17, -24, 34, 16, 5, fill((20, 26, 36)))
    c.drawCircle(-8, -16, 4, fill((120, 220, 255)))
    c.drawCircle(8, -16, 4, fill((120, 220, 255)))
    rrect(c, -14, 4, 28, 8, 3, fill(body))
    c.restore()


def icon_search(c, x, y, s, color=(70, 80, 96)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawCircle(0, -4, 16, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                       Color=col(color), StrokeWidth=7))
    c.drawLine(skia.Point(11, 7), skia.Point(24, 20), stroke(color, 8))
    c.restore()


def icon_bubble(c, x, y, w, h, bg=WHITE, tail="left", r=18, dots=None, alpha=1.0):
    c.save()
    if alpha < 1.0:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(x - 30, y - h - 30, w + 60, h + 60), int(255 * alpha))
    path = skia.Path()
    rect = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y - h, w, h), r, r)
    path.addRRect(rect)
    if tail == "left":
        path.moveTo(x + 20, y - 2)
        path.lineTo(x + 2, y + 16)
        path.lineTo(x + 34, y - 2)
    else:
        path.moveTo(x + w - 34, y - 2)
        path.lineTo(x + w - 2, y + 16)
        path.lineTo(x + w - 20, y - 2)
    path.close()
    c.drawPath(path, fill(bg, int(255 * alpha)))
    if dots:
        n = dots
        for i in range(n):
            dx = x + w / 2 + (i - (n - 1) / 2) * 16
            c.drawCircle(dx, y - h / 2, 5, fill((150, 158, 170), int(255 * alpha)))
    c.restore()


def icon_store(c, x, y, s, body=(222, 146, 32), awning=CORAL):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -34, -20, 68, 46, 5, fill(body))
    rrect(c, -20, 2, 40, 24, 4, fill((60, 46, 36)))
    for i in range(4):
        rrect(c, -40 + i * 20, -34, 20, 16, 3, fill(awning if i % 2 == 0 else WHITE))
    rrect(c, -42, -22, 84, 8, 4, fill((60, 46, 36)))
    c.restore()


def icon_website(c, x, y, s, t=0.0):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -50, -34, 100, 68, 8, fill(WHITE))
    rrect(c, -50, -34, 100, 14, 8, fill((70, 80, 96)))
    c.drawCircle(-42, -27, 3, fill(CORAL))
    c.drawCircle(-32, -27, 3, fill(GOLD))
    c.drawCircle(-22, -27, 3, fill(GREEN))
    rrect(c, -40, -12, 34, 30, 4, fill((18, 148, 144)))
    rrect(c, 0, -12, 40, 8, 3, fill((200, 206, 216)))
    rrect(c, 0, 0, 40, 8, 3, fill((200, 206, 216)))
    rrect(c, 0, 12, 26, 8, 3, fill((200, 206, 216)))
    c.restore()


def icon_trash(c, x, y, s, color=CORAL):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -16, -14, 32, 36, 5, fill(color))
    rrect(c, -20, -20, 40, 8, 4, fill(color))
    rrect(c, -7, -26, 14, 6, 3, fill(color))
    c.drawLine(skia.Point(-6, -6), skia.Point(-6, 14), stroke(WHITE, 4))
    c.drawLine(skia.Point(0, -6), skia.Point(0, 14), stroke(WHITE, 4))
    c.drawLine(skia.Point(6, -6), skia.Point(6, 14), stroke(WHITE, 4))
    c.restore()


def icon_calendar(c, x, y, s, label=None, color=WHITE, head=CORAL):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -30, -26, 60, 54, 7, fill(color))
    rrect(c, -30, -26, 60, 16, 7, fill(head))
    rrect(c, -30, -18, 60, 8, 0, fill(head))
    c.drawLine(skia.Point(-16, -32), skia.Point(-16, -22), stroke((70, 80, 96), 5))
    c.drawLine(skia.Point(16, -32), skia.Point(16, -22), stroke((70, 80, 96), 5))
    if label:
        draw_text(c, label, 0, 18, 22, color=(70, 80, 96), weight="latin", align="center")
    c.restore()


def icon_coin(c, x, y, s, color=GOLD, sym="$"):
    c.drawCircle(x, y, s, fill(color))
    c.drawCircle(x, y, s * 0.8, fill(tuple(min(255, v + 30) for v in color)))
    draw_text(c, sym, x, y + s * 0.55, s * 1.1, color=(120, 84, 8), weight="latin_black", align="center")


def icon_briefcase(c, x, y, s, color=(110, 84, 60)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    rrect(c, -24, -14, 48, 34, 6, fill(color))
    rrect(c, -10, -22, 20, 10, 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                             Color=col(color), StrokeWidth=6))
    c.drawLine(skia.Point(-24, 2), skia.Point(24, 2), stroke((80, 60, 42), 4))
    c.restore()


def icon_chart_line(c, x, y, w, h, pts, color=TEAL, lw=8, area=None, t=1.0):
    """pts: list of (0..1, 0..1) with y=1 bottom. t: reveal progress."""
    n = len(pts)
    vis = max(2, int(2 + (n - 2) * clamp(t)))
    path = skia.Path()
    for i in range(vis):
        px = x + pts[i][0] * w
        py = y + (1 - pts[i][1]) * h
        if i == 0:
            path.moveTo(px, py)
        else:
            px0 = x + pts[i - 1][0] * w
            py0 = y + (1 - pts[i - 1][1]) * h
            mx = (px0 + px) / 2
            path.cubicTo(mx, py0, mx, py, px, py)
    if area is not None:
        ap = skia.Path(path)
        ap.lineTo(x + pts[vis - 1][0] * w, y + h)
        ap.lineTo(x, y + h)
        ap.close()
        c.drawPath(ap, fill(area, 40))
    c.drawPath(path, stroke(color, lw))


def icon_globe(c, x, y, s, color=(70, 130, 200)):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.drawCircle(0, 0, 26, fill(color))
    c.save()
    c.clipPath(skia.Path().addCircle(0, 0, 26), skia.ClipOp.kIntersect)
    c.drawLine(skia.Point(-26, 0), skia.Point(26, 0), stroke(WHITE, 3))
    c.drawLine(skia.Point(0, -26), skia.Point(0, 26), stroke(WHITE, 3))
    path = skia.Path()
    path.addOval(skia.Rect.MakeXYWH(-12, -26, 24, 52))
    c.drawPath(path, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, Color=col(WHITE), StrokeWidth=3))
    path2 = skia.Path()
    path2.addOval(skia.Rect.MakeXYWH(-26, -10, 52, 20))
    c.drawPath(path2, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, Color=col(WHITE), StrokeWidth=3))
    c.restore()
    c.restore()


# ---------- environments ----------
def skyline(c, y, t=0.0, scale=1.0, color=(30, 42, 66), windows=None, alpha=1.0, seed=3.0):
    """Flat city skyline along baseline y."""
    c.save()
    if alpha < 1.0:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(0, y - 500, W, 600), int(255 * alpha))
    rnd = seed
    x = -60
    while x < W + 60:
        rnd = (rnd * 9301 + 49297) % 233280
        r = rnd / 233280
        bw = (60 + r * 120) * scale
        bh = (90 + r * 220) * scale
        rrect(c, x, y - bh, bw, bh + 10, 6, fill(color, int(255 * alpha)))
        if windows:
            wr = (rnd * 7919) % 5
            for wy in range(int(y - bh + 18), int(y - 14), 34):
                for wx in range(int(x + 10), int(x + bw - 14), 26):
                    if (wx * 7 + wy * 13 + wr) % 3 == 0:
                        c.drawRect(skia.Rect.MakeXYWH(wx, wy, 12, 16), fill(windows, int(200 * alpha)))
        x += bw + (8 + r * 26) * scale
    c.restore()


def tree(c, x, y, s=1.0, trunk=(110, 84, 60), leaf=(58, 125, 84), sway=0.0):
    c.save()
    c.translate(x, y)
    c.rotate(math.degrees(sway))
    c.drawLine(skia.Point(0, 0), skia.Point(0, -60 * s), stroke(trunk, 10 * s))
    c.drawCircle(0, -85 * s, 34 * s, fill(leaf))
    c.drawCircle(-22 * s, -66 * s, 24 * s, fill(leaf))
    c.drawCircle(22 * s, -66 * s, 24 * s, fill(leaf))
    c.restore()


def cloud(c, x, y, s=1.0, color=WHITE, alpha=200):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    p = fill(color, alpha)
    c.drawOval(skia.Rect.MakeXYWH(-50, -16, 100, 32), p)
    c.drawCircle(-20, -18, 22, p)
    c.drawCircle(14, -22, 26, p)
    c.restore()


def sun_moon(c, x, y, r, night=False, t=0.0, alpha=1.0):
    if not night:
        radial_glow(c, x, y, r * 3.2, (255, 205, 110), int(120 * alpha))
        c.drawCircle(x, y, r, fill((255, 200, 90), int(255 * alpha)))
    else:
        radial_glow(c, x, y, r * 3.2, (200, 215, 255), int(80 * alpha))
        c.drawCircle(x, y, r, fill((226, 232, 248), int(255 * alpha)))
        c.drawCircle(x - r * 0.35, y - r * 0.25, r * 0.85,
                     fill((13, 22, 38), int(255 * alpha)))


def stars(c, t=0.0, n=70, alpha=1.0, seed=7.0):
    rnd = seed
    for i in range(n):
        rnd = (rnd * 9301 + 49297) % 233280
        r1 = rnd / 233280
        rnd = (rnd * 9301 + 49297) % 233280
        r2 = rnd / 233280
        x, y = r1 * W, r2 * H * 0.7
        tw = 0.55 + 0.45 * math.sin(t * 1.5 + i * 1.7)
        c.drawCircle(x, y, 1.6 + r2 * 1.6, fill((220, 228, 250), int(255 * tw * alpha)))


def bg_grid(c, color=(16, 26, 43), line_alpha=14, step=90):
    p = stroke(color, 1.5, line_alpha)
    for x in range(0, W + step, step):
        c.drawLine(skia.Point(x, 0), skia.Point(x, H), p)
    for y in range(0, H + step, step):
        c.drawLine(skia.Point(0, y), skia.Point(W, y), p)


def blob(c, x, y, r, color, alpha=30, t=0.0):
    path = skia.Path()
    n = 8
    for i in range(n * 2):
        ang = math.pi * i / n
        rr = r * (1 + 0.08 * math.sin(ang * 3 + t * 0.6 + x * 0.01))
        px = x + math.cos(ang) * rr
        py = y + math.sin(ang) * rr
        if i == 0:
            path.moveTo(px, py)
        else:
            path.lineTo(px, py)
    path.close()
    c.drawPath(path, fill(color, alpha))


# ---------- Bangladesh map (simplified) ----------
BD_MAP = [
    (0.30, 0.02), (0.55, 0.06), (0.62, 0.16), (0.80, 0.20), (0.88, 0.34),
    (0.80, 0.44), (0.86, 0.56), (0.74, 0.66), (0.78, 0.80), (0.60, 0.88),
    (0.44, 0.84), (0.34, 0.94), (0.20, 0.88), (0.26, 0.72), (0.12, 0.64),
    (0.22, 0.52), (0.10, 0.40), (0.24, 0.30), (0.16, 0.16),
]


def bd_map_path(x, y, w, h):
    path = skia.Path()
    for i, (fx, fy) in enumerate(BD_MAP):
        px, py = x + fx * w, y + fy * h
        if i == 0:
            path.moveTo(px, py)
        else:
            prev = BD_MAP[i - 1]
            mx = x + (fx + prev[0]) / 2 * w
            my = y + (fy + prev[1]) / 2 * h
            path.quadTo(mx, my, px, py)
    first = BD_MAP[0]
    last = BD_MAP[-1]
    mx = x + (first[0] + last[0]) / 2 * w
    my = y + (first[1] + last[1]) / 2 * h
    path.quadTo(mx, my, x + first[0] * w, y + first[1] * h)
    path.close()
    return path


# ---------- misc components ----------
def gig_card(c, x, y, s, title="আধুনিক মিনিমালিস্ট লোগো", price="$5", t=0.0, alpha=1.0,
             stars=0, w=340, h=250, deleting=False):
    """Marketplace gig card."""
    c.save()
    if alpha < 1.0:
        c.saveLayerAlpha(skia.Rect.MakeXYWH(x - 30, y - 30, w + 60, h + 60), int(255 * alpha))
    scale = 1.0
    if deleting:
        scale = 1.0 - 0.25 * ease_out_cubic(deleting)
    c.translate(x + w / 2, y + h / 2)
    c.scale(scale, scale)
    c.translate(-(x + w / 2), -(y + h / 2))
    shadow_card(c, x, y, w, h, 18, bg=WHITE, sd=(20, 30, 50, 50), sd_dy=10, sd_r=22)
    # thumbnail
    rrect(c, x + 14, y + 14, w - 28, 120, 12, fill((232, 238, 244)))
    # mini logo art
    cx, cy = x + w / 2, y + 74
    c.drawCircle(cx - 26, cy, 20, fill(TEAL))
    c.drawCircle(cx + 26, cy, 20, fill(ORANGE))
    rrect(c, cx - 8, cy - 34, 16, 68, 8, fill(INK))
    rrect(c, x + 30, y + 148, w - 60, 16, 5, fill((60, 70, 86)))
    rrect(c, x + 30, y + 172, (w - 60) * 0.62, 12, 5, fill((196, 202, 212)))
    if stars > 0:
        for i in range(5):
            icon_star(c, x + 44 + i * 30, y + 210, 11, GOLD, filled=i < stars)
    rrect(c, x + w - 96, y + 196, 80, 30, 15, fill(TEAL))
    draw_text(c, price, x + w - 56, y + 217, 26, color=WHITE, weight="latin_black", align="center")
    c.restore()


def progress_note(c, t):
    pass
