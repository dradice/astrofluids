#!/usr/bin/env python3
"""Figures of Appendix A (vector calculus).

Usage: python3 figures-src/vector-calculus/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "vector-calculus"


def vec_label(s, x, y, name, anchor="start", fill="#000"):
    """Write 'd' upright followed by a bold upright vector name, e.g. dl or dA."""
    s.raw(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="20" fill="{fill}">'
          f'd<tspan font-weight="bold">{name}</tspan></text>')


def stokes():
    s = Svg(440, 300, "Stokes' theorem",
            "A curved surface S, shaded grey, shaped like a dome, whose edge is the closed curve "
            "C, drawn as an ellipse. Arrows along C show the direction of the line element dl, "
            "counterclockwise when seen from above. At the top of the dome a small patch of the "
            "surface carries the area element dA, an arrow pointing up and away from the "
            "surface. The direction of C and that of dA are related by the right-hand rule: "
            "with the thumb along dA, the fingers curl along C.",
            "vec-stokes")
    cx, cy, rx, ry = 215, 225, 165, 48
    top = 70
    # dome: the surface S, from the left end of the ellipse over the top to the right end
    dome = (f"M {cx - rx} {cy} C {cx - rx} {top - 10}, {cx + rx} {top - 10}, {cx + rx} {cy} "
            f"A {rx} {ry} 0 0 1 {cx - rx} {cy} Z")
    s.path(dome, fill=GRAY, w=0)
    s.path(f"M {cx - rx} {cy} C {cx - rx} {top - 10}, {cx + rx} {top - 10}, {cx + rx} {cy}",
           w=1.4)
    # boundary C: back half dashed (hidden by the dome), front half solid
    s.path(f"M {cx - rx} {cy} A {rx} {ry} 0 0 1 {cx + rx} {cy}", color=BLUE, w=2.4, dash="6 5")
    s.path(f"M {cx + rx} {cy} A {rx} {ry} 0 0 1 {cx - rx} {cy}", color=BLUE, w=2.4)
    # orientation of C: towards the right on the front (counterclockwise seen from above)
    yf = cy + ry
    s.line(cx - 20, yf, cx + 22, yf, color=BLUE, w=2.4, head=True)
    vec_label(s, cx, yf + 26, "l", anchor="middle", fill=BLUE)
    s.text(cx + rx + 8, cy + 22, "C", fill=BLUE)
    # patch with area element dA at the top of the dome
    yp = top + 70
    s.ellipse(cx, yp, 26, 7, stroke="#000", w=1.4, fill="#fff")
    s.line(cx, yp, cx, yp - 62, color=RED, w=2.4, head=True)
    vec_label(s, cx + 10, yp - 44, "A", fill=RED)
    s.text(cx - 95, cy - 50, "S", size=22)
    s.save(OUT / "stokes.svg")


def gauss():
    s = Svg(440, 320, "Divergence theorem",
            "A closed, irregular surface S, drawn as a thick outline, enclosing a volume V shaded "
            "grey. Arrows at several points of S show the area elements dA, perpendicular to the "
            "surface and pointing outwards.",
            "vec-gauss")
    cx, cy, R = 215, 160, 92

    def point(t):
        r = R * (1 + 0.10 * math.cos(3 * t) + 0.06 * math.sin(2 * t))
        return cx + 1.25 * r * math.cos(t), cy + 0.95 * r * math.sin(t)

    n = 240
    pts = [point(2 * math.pi * i / n) for i in range(n)]
    s.poly(pts, fill=GRAY, w=2.2, closed=True)
    for k, t in enumerate((0.25, 1.35, 2.3, 3.4, 4.4, 5.4)):
        x, y = point(t)
        x1, y1 = point(t + 1e-3)
        tx, ty = x1 - x, y1 - y
        L = math.hypot(tx, ty)
        nx, ny = ty / L, -tx / L          # outward normal (the curve runs with increasing t)
        s.line(x, y, x + 48 * nx, y + 48 * ny, color=RED, w=2.4, head=True)
        s.circle(x, y, 3, fill="#000", w=0)
        if k == 0:
            vec_label(s, x + 48 * nx + 6, y + 48 * ny + 6, "A", fill=RED)
    s.text(cx - 10, cy + 8, "V", size=22)
    x, y = point(4.0)
    s.text(x - 8, y - 8, "S", anchor="end", size=22)
    s.save(OUT / "gauss.svg")


def div_curl():
    s = Svg(440, 470, "Divergence of a curl",
            "A closed surface cut along a closed curve C into two pieces, drawn pulled apart. "
            "The upper piece S_1 is a dome whose rim is C; its area element dA points up, out of "
            "the enclosed volume, and the arrow on its rim shows that C is traversed "
            "counterclockwise when seen from above. The lower piece S_2 is a bowl with the same "
            "rim C; its area element dA points down, again out of the volume, and the arrow on its "
            "rim shows that C is traversed clockwise when seen from above, opposite to the upper "
            "piece. The two circulations along C therefore cancel.",
            "vec-div-curl")
    cx, rx, ry = 220, 160, 40

    # upper piece S_1: dome over the rim at y = yt
    yt, top = 165, 55
    s.path(f"M {cx - rx} {yt} C {cx - rx} {top - 10}, {cx + rx} {top - 10}, {cx + rx} {yt} "
           f"A {rx} {ry} 0 0 1 {cx - rx} {yt} Z", fill=GRAY, w=0)
    s.path(f"M {cx - rx} {yt} C {cx - rx} {top - 10}, {cx + rx} {top - 10}, {cx + rx} {yt}", w=1.4)
    s.path(f"M {cx - rx} {yt} A {rx} {ry} 0 0 1 {cx + rx} {yt}", color=BLUE, w=2.4, dash="6 5")
    s.path(f"M {cx + rx} {yt} A {rx} {ry} 0 0 1 {cx - rx} {yt}", color=BLUE, w=2.4)
    s.line(cx - 22, yt + ry, cx + 22, yt + ry, color=BLUE, w=2.4, head=True)
    vec_label(s, cx, yt + ry + 26, "l", anchor="middle", fill=BLUE)
    s.line(cx, top + 28, cx, top - 30, color=RED, w=2.4, head=True)
    vec_label(s, cx + 10, top - 12, "A", fill=RED)
    s.text(cx - 110, yt - 40, "S_1", size=22)
    s.text(cx + rx + 8, yt + 22, "C", fill=BLUE)

    # lower piece S_2: bowl under the rim at y = yb
    yb, bottom = 300, 425
    s.path(f"M {cx - rx} {yb} C {cx - rx} {bottom + 10}, {cx + rx} {bottom + 10}, {cx + rx} {yb} "
           f"A {rx} {ry} 0 0 0 {cx - rx} {yb} Z", fill=GRAY, w=0)
    s.path(f"M {cx - rx} {yb} C {cx - rx} {bottom + 10}, {cx + rx} {bottom + 10}, {cx + rx} {yb}",
           w=1.4)
    s.ellipse(cx, yb, rx, ry, fill="#ececec", stroke=TEAL, w=2.4)
    s.line(cx + 22, yb + ry, cx - 22, yb + ry, color=TEAL, w=2.4, head=True)
    vec_label(s, cx, yb + ry + 26, "l", anchor="middle", fill=TEAL)
    # point on the bowl outline (cubic at t = 0.7) and its outward normal, down and right
    s.line(cx + 91, 385, cx + 113, 427, color=RED, w=2.4, head=True)
    vec_label(s, cx + 122, 420, "A", fill=RED)
    s.text(cx - 70, yb + 85, "S_2", size=22)
    s.text(cx + rx + 8, yb + 22, "C", fill=TEAL)
    s.save(OUT / "div-curl.svg")


if __name__ == "__main__":
    stokes()
    gauss()
    div_curl()
    print("wrote", OUT)
