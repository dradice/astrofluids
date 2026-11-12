#!/usr/bin/env python3
"""Figures of Ch. 8 (hydrostatic equilibrium).

Usage: python3 figures-src/hydrostatic-equilibrium/make-figures.py   (from the notes/ directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "hydrostatic-equilibrium"


def tidal_disruption():
    s = Svg(780, 255, "Tidal forces on a star near a black hole",
            "A black hole of mass M_BH on the left and a star of mass M_* and radius R_* at a "
            "distance r on the right. On the side of the star facing the black hole, the black "
            "hole pulls with acceleration G M_BH over (r minus R_*) squared, towards the black "
            "hole, while the self-gravity of the star pulls with G M_* over R_* squared, towards "
            "the center of the star. On the opposite side, both accelerations point towards the "
            "black hole: G M_BH over (r plus R_*) squared and G M_* over R_* squared.",
            "tidal-disruption")
    xb, xs, y, R = 90, 480, 100, 95
    s.circle(xb, y, 32, fill="#000")
    s.text(xb, y + 62, "M_{BH}", anchor="middle")
    s.ellipse(xs, y, R, 72)
    s.circle(xs, y, 3.2, fill="#000")
    s.text(xs + 8, y - 8, "M_*")
    xn, xf = xs - R, xs + R
    for x in (xn, xf):
        s.circle(x, y, 3.2, fill="#000")
    # accelerations: black hole (blue, above the axis) and self-gravity (green, below)
    s.line(xn, y - 12, xn - 85, y - 12, color=BLUE, w=2.2, head=True)
    s.line(xf, y - 12, xf - 40, y - 12, color=BLUE, w=2.2, head=True)
    s.line(xn, y + 12, xn + 45, y + 12, color=GREEN, w=2.2, head=True)
    s.line(xf, y + 12, xf - 45, y + 12, color=GREEN, w=2.2, head=True)
    s.text(xn - 10, y - 32, "GM_{BH}/(r − R_*)^2", anchor="end", fill=BLUE)
    s.text(xf + 10, y - 32, "GM_{BH}/(r + R_*)^2", fill=BLUE)
    s.text(xn - 10, y + 36, "GM_*/R_*^2", anchor="end", fill=GREEN)
    s.text(xf + 10, y + 36, "GM_*/R_*^2", fill=GREEN)
    # distances
    s.bracket(xs, 195, xf, 195)
    s.text((xs + xf) / 2, 186, "R_*", anchor="middle")
    s.bracket(xb, 232, xs, 232)
    s.text((xb + xs) / 2, 223, "r", anchor="middle")
    s.save(OUT / "tidal-disruption.svg")


if __name__ == "__main__":
    tidal_disruption()
    print("wrote", OUT)
