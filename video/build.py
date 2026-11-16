"""Main build: frame loop -> ffmpeg rawvideo pipe, plus preview mode."""
import os
import subprocess
import sys

import numpy as np
import skia

from gfx import W, H
from timeline import Timeline
from scenes_a import (sc_intro, sc_meet_azad, sc_rajshahi, sc_first_order,
                      sc_orders_grow, sc_big_buyer, sc_imran, sc_chatgpt,
                      sc_research, sc_fiverr_report, sc_that_night)
from scenes_b import (sc_twist, sc_survived, sc_new_jobs, sc_delete_gig,
                      sc_learning, sc_portfolio, sc_no_magic, sc_advice,
                      sc_own_door, sc_ending)

TOTAL = 529.88
FPS = 24

SCENES = [
    (0.0, 24.2, sc_intro),
    (24.2, 43.6, sc_meet_azad),
    (43.6, 59.7, sc_rajshahi),
    (59.7, 74.4, sc_first_order),
    (74.6, 103.3, sc_orders_grow),
    (103.3, 150.7, sc_big_buyer),
    (150.7, 183.7, sc_imran),
    (183.7, 200.7, sc_chatgpt),
    (200.7, 253.7, sc_research),
    (253.7, 293.7, sc_fiverr_report),
    (293.7, 325.7, sc_that_night),
    (325.7, 341.7, sc_twist),
    (341.7, 360.7, sc_survived),
    (360.7, 393.7, sc_new_jobs),
    (393.7, 403.7, sc_delete_gig),
    (403.7, 425.7, sc_learning),
    (425.7, 445.7, sc_portfolio),
    (445.7, 465.0, sc_no_magic),
    (465.0, 495.0, sc_advice),
    (495.0, 517.0, sc_own_door),
    (517.0, TOTAL, sc_ending),
]

FFMPEG = "/workspace/bin/ffmpeg"
AUDIO = "/workspace/voiceover.mp3"
OUT = "/workspace/explainer_final.mp4"


def make_timeline():
    return Timeline(SCENES, TOTAL)


def preview(step=48, outdir="/workspace/preview"):
    os.makedirs(outdir, exist_ok=True)
    tl = make_timeline()
    surface = skia.Surface(W, H)
    n_frames = int(TOTAL * FPS)
    targets = set(range(0, n_frames, step))
    targets.add(n_frames - 1)
    for i in sorted(targets):
        T = i / FPS
        with surface as c:
            tl.render(c, T)
        img = surface.makeImageSnapshot()
        data = img.tobytes()
        arr = np.frombuffer(data, dtype=np.uint8).reshape(H, W, 4)
        arr = arr[:, :, [2, 1, 0, 3]]  # BGRA -> RGBA
        from PIL import Image
        Image.fromarray(arr[:, :, :3]).save(f"{outdir}/f{i:05d}_t{T:07.2f}.png")
        print(f"preview {i}/{n_frames} T={T:.2f}", flush=True)
    print("preview done")


def render():
    n_frames = int(TOTAL * FPS)
    cmd = [
        FFMPEG, "-y",
        "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "-",
        "-i", AUDIO,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-shortest",
        OUT,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tl = make_timeline()
    surface = skia.Surface(W, H)
    for i in range(n_frames):
        T = i / FPS
        with surface as c:
            tl.render(c, T)
        img = surface.makeImageSnapshot()
        proc.stdin.write(img.tobytes())
        if i % 480 == 0:
            print(f"frame {i}/{n_frames} T={T:.2f}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("render done rc=", proc.returncode)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "render"
    if mode == "preview":
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 48
        preview(step)
    else:
        render()
