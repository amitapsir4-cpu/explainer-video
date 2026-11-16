"""Bengali/Latin text rendering: harfbuzz shaping + freetype outline decomposition -> skia.Path."""
import os
import uharfbuzz as hb
import freetype
import skia

FONT_DIR = "/workspace/fonts"
_FONTS = {
    "bn": os.path.join(FONT_DIR, "NotoSansBengali-SemiBold.ttf"),
    "bn_regular": os.path.join(FONT_DIR, "NotoSansBengali-Regular.ttf"),
    "bn_bold": os.path.join(FONT_DIR, "NotoSansBengali-Bold.ttf"),
    "latin": os.path.join(FONT_DIR, "NotoSans-Bold.ttf"),
    "latin_black": os.path.join(FONT_DIR, "NotoSans-Black.ttf"),
    "latin_regular": os.path.join(FONT_DIR, "NotoSans-Regular.ttf"),
}
_hb_cache = {}
_ft_cache = {}
_path_cache = {}
_metrics_cache = {}


def _detect_script(text):
    for ch in text:
        cp = ord(ch)
        if 0x0980 <= cp <= 0x09FF:
            return "bn"
    return "latin"


def _pick_font(text, weight):
    script = _detect_script(text)
    key = f"{script}_{weight}"
    return _FONTS.get(key, _FONTS[script])


def _get_hb(path):
    if path not in _hb_cache:
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        font = hb.Font(face)
        _hb_cache[path] = (face, font)
    return _hb_cache[path]


def _get_ft(path):
    if path not in _ft_cache:
        _ft_cache[path] = freetype.Face(path)
    return _ft_cache[path]


def shape_text(text, font_path, px_size):
    """Returns list of (glyph_id, x, y) with y down (px units) and total advance width."""
    face, font = _get_hb(font_path)
    upem = face.upem
    scale = px_size / upem
    font.scale = (upem, upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    pen_x = 0.0
    glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gx = pen_x + pos.x_offset * scale
        gy = -pos.y_offset * scale
        glyphs.append((info.codepoint, gx, gy))
        pen_x += pos.x_advance * scale
    return glyphs, pen_x


class _PathBuilder:
    def __init__(self, ox, oy):
        self.path = skia.Path()
        self.ox = ox
        self.oy = oy

    def move_to(self, pt, ctx):
        self.path.moveTo(self.ox + pt.x / 64.0, self.oy - pt.y / 64.0)

    def line_to(self, pt, ctx):
        self.path.lineTo(self.ox + pt.x / 64.0, self.oy - pt.y / 64.0)

    def conic_to(self, c, pt, ctx):
        self.path.quadTo(self.ox + c.x / 64.0, self.oy - c.y / 64.0,
                         self.ox + pt.x / 64.0, self.oy - pt.y / 64.0)

    def cubic_to(self, c1, c2, pt, ctx):
        self.path.cubicTo(
            self.ox + c1.x / 64.0, self.oy - c1.y / 64.0,
            self.ox + c2.x / 64.0, self.oy - c2.y / 64.0,
            self.ox + pt.x / 64.0, self.oy - pt.y / 64.0,
        )


def _glyph_outline(font_path, glyph_id):
    """Return list of (points, tags, contours) raw outline or None."""
    ft = _get_ft(font_path)
    ft.set_pixel_sizes(0, 100)
    ft.load_glyph(glyph_id, freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_NO_BITMAP)
    g = ft.glyph
    if g.format != freetype.FT_GLYPH_FORMAT_OUTLINE:
        return None
    outline = g.outline
    return outline


def build_text_path(text, size, weight="medium"):
    """Build a skia.Path for the shaped text at given px size, baseline at y=0, pen start x=0.
    Returns (path, advance_width, ascent_px, descent_px)."""
    if not text:
        return skia.Path(), 0, 0, 0
    font_path = _pick_font(text, weight)
    glyphs, width = shape_text(text, font_path, size)
    path = skia.Path()
    ft = _get_ft(font_path)
    ft.set_pixel_sizes(0, 100)
    scale = size / 100.0
    for gid, gx, gy in glyphs:
        ft.load_glyph(gid, freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_NO_BITMAP)
        outline = ft.glyph.outline
        if outline.n_points == 0:
            continue
        builder = _PathBuilder(gx, gy)
        outline.decompose(
            builder,
            builder.move_to,
            builder.line_to,
            builder.conic_to,
            builder.cubic_to,
        )
        if scale != 1.0:
            m = skia.Matrix.Scale(scale, scale)
            path.addPath(builder.path, m)
        else:
            path.addPath(builder.path)
    fm = ft.size._metrics if hasattr(ft.size, "_metrics") else None
    ascent = size * 1.12
    descent = size * 0.38
    return path, width, ascent, descent


def C(r, g, b, a=255):
    return (int(a) << 24) | (int(r) << 16) | (int(g) << 8) | int(b)


def _as_color_int(color):
    if isinstance(color, (tuple, list)):
        return C(*color)
    return color


def draw_text(canvas, text, x, y, size, color=(30, 30, 40, 255), weight="medium",
              align="left", opacity=1.0, stroke=None, stroke_width=0.0):
    """Draw shaped text. align: left/center/right. y = baseline."""
    if not text:
        return
    if isinstance(color, (tuple, list)) and len(color) == 3:
        color = (color[0], color[1], color[2], 255)
    key = (text, round(size), weight)
    if key not in _path_cache:
        _path_cache[key] = build_text_path(text, size, weight)
    path, width, ascent, descent = _path_cache[key]
    if align == "center":
        x -= width / 2
    elif align == "right":
        x -= width
    save = canvas.save()
    canvas.translate(x, y)
    if opacity < 1.0:
        if isinstance(color, (tuple, list)):
            color = (color[0], color[1], color[2], int(color[3] * max(0.0, min(1.0, opacity))))
        else:
            a = (color >> 24) & 0xFF
            color = (color & 0x00FFFFFF) | (int(a * max(0.0, min(1.0, opacity))) << 24)
    paint = skia.Paint(AntiAlias=True, Color=_as_color_int(color), Style=skia.Paint.kFill_Style)
    canvas.drawPath(path, paint)
    if stroke is not None:
        sp = skia.Paint(AntiAlias=True, Color=_as_color_int(stroke), Style=skia.Paint.kStroke_Style,
                        StrokeWidth=stroke_width)
        canvas.drawPath(path, sp)
    canvas.restoreToCount(save)


def text_width(text, size, weight="medium"):
    key = (text, round(size), weight)
    if key not in _path_cache:
        _path_cache[key] = build_text_path(text, size, weight)
    return _path_cache[key][1]
