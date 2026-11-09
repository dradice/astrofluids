#!/usr/bin/env python3
"""Figure of the Rayleigh-Taylor worksheet (rotated fluid cylinder), redrawn from the 2025 drawing.

Usage: python3 figures-src/instabilities-rt-kh/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "instabilities-rt-kh"

HEAVY = "#b3b3b3"
LIGHT = "#ececec"


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def sector(cx, cy, r1, r2, d0, d1):
    """Annular sector from angle d0 to d1 (degrees, counterclockwise on the screen)."""
    x0, y0 = pt(cx, cy, r2, d0)
    x1, y1 = pt(cx, cy, r2, d1)
    x2, y2 = pt(cx, cy, r1, d1)
    x3, y3 = pt(cx, cy, r1, d0)
    large = 1 if (d1 - d0) % 360 > 180 else 0
    return (f"M {x0:.1f} {y0:.1f} A {r2} {r2} 0 {large} 0 {x1:.1f} {y1:.1f} "
            f"L {x2:.1f} {y2:.1f} A {r1} {r1} 0 {large} 1 {x3:.1f} {y3:.1f} Z")


def ring():
    W, H = 520, 400
    cx, cy, r, R = 260, 200, 95, 125
    th = 30
    s = Svg(W, H, "Fluid cylinder rotated across a heavy-over-light interface",
            "A heavy fluid of density rho_2 lies on top of a lighter fluid of density rho_1 along a "
            "horizontal interface. A circular region of radius r is split by the interface into a "
            "heavy upper half and a light lower half. Around it, a thin ring of fluid has been "
            "rotated counterclockwise by an angle theta: heavy fluid has moved down on the left "
            "and light fluid has moved up on the right.", "rtring")
    s.rect(20, 20, 480, 180, fill=HEAVY, stroke="none", sw=0)
    s.rect(20, 200, 480, 180, fill=LIGHT, stroke="none", sw=0)
    # ring: heavy part from theta to 180+theta, light part otherwise
    s.path(sector(cx, cy, r, R, th, 180 + th), fill=HEAVY)
    s.path(sector(cx, cy, r, R, 180 + th, 360 + th), fill=LIGHT)
    # inner disc: heavy upper half, light lower half
    s.path(f"M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy} Z", fill=HEAVY)
    s.path(f"M {cx - r} {cy} A {r} {r} 0 0 0 {cx + r} {cy} Z", fill=LIGHT)
    # interface outside the ring and the horizontal radius
    s.line(20, cy, cx - R, cy)
    s.line(cx + R, cy, 500, cy)
    s.line(cx - r, cy, cx + r, cy)
    # rotated radius and angle
    x, y = pt(cx, cy, R, th)
    s.line(cx, cy, x, y, w=2.2)
    a0 = pt(cx, cy, 55, 0)
    a1 = pt(cx, cy, 55, th)
    s.path(f"M {a0[0]:.1f} {a0[1]:.1f} A 55 55 0 0 0 {a1[0]:.1f} {a1[1]:.1f}")
    s.text(cx + 70, cy - 18, "θ", italic=True)
    s.text(cx - 40, cy - 12, "r", anchor="middle")
    s.text(40, cy - 14, "ρ_2")
    s.text(40, cy + 30, "ρ_1")
    s.save(OUT / "rotated-cylinder.svg")


if __name__ == "__main__":
    ring()
