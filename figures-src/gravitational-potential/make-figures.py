#!/usr/bin/env python3
"""Figure of Exercise 7.1 (homologous collapse), redrawn from the 2025 TeXmacs drawing.

Usage: python3 figures-src/gravitational-potential/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "gravitational-potential"


def homologous():
    s = Svg(760, 330, "Effective potential and evolution of a collapsing homogeneous sphere",
            "Left: the effective potential U_eff(a), proportional to minus one over a, below the "
            "horizontal a axis, with a horizontal line at the energy E below zero and an arrow "
            "showing the point moving towards smaller a. Right: the scale factor a decreases to "
            "zero in a finite time, while the density rho grows without bound.", "homologous")
    # left panel
    s.line(100, 20, 100, 310)
    s.line(80, 50, 345, 50)
    s.text(335, 38, "a")
    pts = [(110 + 70 * a, 50 + 70 / a) for a in [0.3 + 0.01 * i for i in range(0, 291)]]
    s.poly(pts, BLUE, 2.2)
    s.line(100, 134, 168, 134, color="#555")
    s.circle(168, 134, 3.2, fill="#000")
    s.line(168, 134, 148, 152, head=True, w=1.4)
    s.text(88, 140, "E", anchor="end")
    s.text(86, 285, "U_{eff}(a)", anchor="end", fill=BLUE)
    # right panel: a(t) and rho(t) for collapse from rest (cycloid)
    x0, T, ybase, h = 470, 170, 270, 140
    s.line(470, 20, 470, 300)
    s.line(450, ybase, 730, ybase)
    s.text(722, 296, "t")
    a_pts, r_pts = [], []
    for i in range(0, 201):
        eta = math.pi * i / 200
        a = (1 + math.cos(eta)) / 2
        t = (eta + math.sin(eta)) / math.pi
        a_pts.append((x0 + T * t, ybase - h * a))
        if a > 0.01:
            y = ybase - h / a**3
            if y > 20:
                r_pts.append((x0 + T * t, y))
    s.poly(a_pts, BLUE, 2.2)
    s.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in r_pts), GREEN, 2.2, dash="9 5")
    s.text(560, 215, "a", fill=BLUE)
    s.text(604, 90, "ρ", fill=GREEN)
    s.save(OUT / "homologous-collapse.svg")


if __name__ == "__main__":
    homologous()
    print("wrote", OUT)
