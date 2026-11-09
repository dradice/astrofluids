#!/usr/bin/env python3
"""Figure of Exercise 12.1 (colliding clouds), redrawn from the 2025 TeXmacs drawing.

Usage: python3 figures-src/radiative-shocks/make-figures.py   (from the notes/ directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "radiative-shocks"


def geometry():
    s = Svg(440, 200, "Idealized geometry of the colliding-cloud problem",
            "One-dimensional sketch along the z axis. A thick blue line on the left marks the "
            "edge of the shocked layer and a thin blue line marks the shock, which moves to the "
            "right at speed s. Between them the shocked material has density rho_2, velocity "
            "zero and temperature T_2. To the right of the shock is the unshocked cloud, with "
            "density rho_1, velocity v_1 and temperature T_1, ending at radius R_c.", "geometry")
    s.line(22, 13, 22, 187)
    s.line(109, 13, 109, 187, color=BLUE, w=3.2)
    s.line(282, 13, 282, 187, color=BLUE, w=1.8)
    s.line(370, 13, 370, 187)
    s.line(195, 100, 412, 100)
    s.line(264, 57, 300, 57, color=BLUE, head=True)
    s.line(264, 143, 300, 143, color=BLUE, head=True)
    s.text(300, 38, "s", fill=BLUE)
    s.text(202, 52, "ρ_2", anchor="middle")
    s.text(215, 90, "v_2 = 0", anchor="middle")
    s.text(202, 135, "T_2", anchor="middle")
    s.text(332, 52, "ρ_1", anchor="middle")
    s.text(332, 90, "v_1", anchor="middle")
    s.text(332, 135, "T_1", anchor="middle")
    s.text(385, 80, "R_c")
    s.text(404, 122, "z")
    s.text(195, 178, "shocked material", anchor="middle", italic=False)
    s.text(322, 178, "cloud", anchor="middle", italic=False)
    s.save(OUT / "colliding-clouds-geometry.svg")


if __name__ == "__main__":
    geometry()
    print("wrote", OUT)
