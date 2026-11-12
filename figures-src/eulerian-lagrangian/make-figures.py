#!/usr/bin/env python3
"""Eulerian vs Lagrangian description (Ch. 5).

Usage: python3 figures-src/eulerian-lagrangian/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "eulerian-lagrangian"


def stream(x0, x1, y0, amp=18, n=80):
    """A gently curved streamline from x0 to x1 around height y0."""
    return [(x0 + (x1 - x0) * i / n, y0 - amp * math.sin(math.pi * i / n)) for i in range(n + 1)]


def point_on(pts, f):
    i = min(int(f * (len(pts) - 1)), len(pts) - 2)
    (xa, ya), (xb, yb) = pts[i], pts[i + 1]
    return xa, ya, math.atan2(yb - ya, xb - xa)


s = Svg(700, 290, "Eulerian and Lagrangian descriptions of a flow",
        "Two panels with the same curved streamlines, flowing from left to right. Left panel, "
        "Eulerian: an observer sits at a fixed point, marked by a cross in a circle, on the middle "
        "streamline. Three different fluid elements, labelled 1, 2 and 3, are on their way through "
        "that point: element 1 has just passed it and element 3 is still upstream. The observer "
        "measures the partial derivative with respect to time. Right panel, Lagrangian: a single "
        "fluid element is shown at three successive times, t_1, t_2 and t_3, as it moves along its "
        "trajectory. An observer riding with it measures the advective derivative d/dt.",
        "eulerlagrange")

GREYS = ["#4d4d4d", "#8c8c8c", "#c8c8c8"]
for x0, title, sub in ((20, "Eulerian", "∂/∂t at a fixed point"),
                       (370, "Lagrangian", "d/dt following a fluid element")):
    x1 = x0 + 310
    lines = [stream(x0, x1, y) for y in (110, 170, 230)]
    for pts in lines:
        s.poly(pts, color="#7a7a7a", w=1.4, head=True)
    s.text(x0 + 155, 28, title, anchor="middle", italic=False, bold=True)
    s.text(x0 + 155, 280, sub, anchor="middle", italic=False, size=18)
    mid = lines[1]
    if title == "Eulerian":
        px, py, _ = point_on(mid, 0.5)
        for k, f in enumerate((0.66, 0.36, 0.08)):
            x, y, _ = point_on(mid, f)
            s.circle(x, y, 11, fill=GREYS[k], stroke="#000", w=1.4)
            s.text(x, y - 18, str(k + 1), anchor="middle", italic=False, size=17)
        s.circle(px, py, 9, fill="#fff", stroke=RED, w=2.2)
        s.line(px - 6, py - 6, px + 6, py + 6, color=RED, w=2.2)
        s.line(px - 6, py + 6, px + 6, py - 6, color=RED, w=2.2)
        s.text(px + 4, py + 32, "x", anchor="middle", bold=True, italic=False)
    else:
        for k, (f, lab) in enumerate(((0.12, "t_1"), (0.47, "t_2"), (0.82, "t_3"))):
            x, y, _ = point_on(mid, f)
            s.circle(x, y, 11, fill=GREYS[2 - k], stroke="#000", w=1.4)
            s.text(x, y + 34, lab, anchor="middle")
        x, y, _ = point_on(mid, 0.82)
        s.text(x + 18, y - 16, "𝒱", italic=False)

s.save(OUT / "eulerian-lagrangian.svg")
