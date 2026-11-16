"""Scene timeline manager with crossfades and global grade."""
import skia
from gfx import W, H, col, fill, vignette

XF = 0.7  # crossfade seconds


class Timeline:
    def __init__(self, scenes, total):
        # scenes: list of (start, end, draw_fn(c, t, dur))
        self.scenes = sorted(scenes, key=lambda s: s[0])
        self.total = total

    def render(self, c, T):
        active = []
        for (start, end, fn) in self.scenes:
            if T >= start - 0.001 and T < end + XF:
                active.append((start, end, fn))
        if not active:
            active = [self.scenes[-1]]
        for (start, end, fn) in active:
            t = min(T - start, end - start)
            t = max(t, 0.0)
            dur = end - start
            a_in = 1.0 if start <= 0.001 else min(1.0, max(0.0, (T - start) / XF))
            if a_in >= 0.999:
                before = c.getSaveCount()
                fn(c, t, dur)
                if c.getSaveCount() != before:
                    c.restoreToCount(before)
            else:
                c.saveLayerAlpha(skia.Rect.MakeWH(W, H), int(255 * a_in))
                before = c.getSaveCount()
                fn(c, t, dur)
                c.restoreToCount(before)
                c.restore()
        # global fade in/out
        if T < 0.8:
            a = 1.0 - T / 0.8
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(6, 10, 18, int(255 * a))))
        if T > self.total - 1.2:
            a = min(1.0, (T - (self.total - 1.2)) / 1.2)
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(6, 10, 18, int(255 * a))))
        vignette(c, 0.14)
