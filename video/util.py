"""Shared animation utilities: easing, interpolation, color helpers."""
import math


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def lerp(a, b, t):
    return a + (b - a) * t


def ease_in_out(t):
    t = clamp(t)
    return t * t * (3 - 2 * t)


def ease_in(t):
    t = clamp(t)
    return t * t


def ease_out(t):
    t = clamp(t)
    return 1 - (1 - t) * (1 - t)


def ease_out_cubic(t):
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_cubic(t):
    t = clamp(t)
    return t ** 3


def ease_out_back(t, s=1.70158):
    t = clamp(t)
    t -= 1
    return 1 + t * t * ((s + 1) * t + s)


def ease_out_elastic(t):
    t = clamp(t)
    if t in (0.0, 1.0):
        return t
    p = 0.35
    return math.pow(2, -9 * t) * math.sin((t - p / 4) * (2 * math.pi / p)) + 1


def ease_out_bounce(t):
    t = clamp(t)
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375


def pulse(t, period=2.0, phase=0.0):
    return 0.5 + 0.5 * math.sin(2 * math.pi * (t / period + phase))


def seg(t, a, b):
    """Normalized progress of t within [a,b]."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def smooth_noise(t, seed=0.0):
    """Cheap smooth pseudo-noise in [-1,1]."""
    x = t * 1.7 + seed * 13.37
    return (math.sin(x) * 0.5 + math.sin(x * 2.3 + 1.7) * 0.3 + math.sin(x * 4.1 + 0.3) * 0.2)
