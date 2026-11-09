#!/usr/bin/env python3
"""Figure of Exercise 11.1 (piston-driven shock), redrawn from the 2025 TeXmacs drawing.

Usage: python3 figures-src/shock-waves/make-figures.py   (from the notes/ directory)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "shock-waves"


def piston():
    s = Svg(480, 170, "A piston driving a shock into a cold gas",
            "A tube with a piston on the left, shown as a grey block with a handle. The piston "
            "moves to the right at speed v_p. A vertical blue line to the right of the piston is "
            "the shock, moving right at speed s. Between piston and shock the gas has density "
            "rho_2, velocity v_p and pressure p_2. Ahead of the shock the gas is at rest with "
            "density rho_1 and zero pressure.", "piston")
    s.line(20, 25, 460, 25)
    s.line(20, 145, 460, 145)
    s.rect(105, 25, 14, 120, fill=GRAY, stroke=GRAY, sw=0)
    s.rect(20, 76, 85, 18, fill=GRAY, stroke=GRAY, sw=0)
    s.line(250, 25, 250, 145, color=BLUE, w=2.2)
    s.line(254, 88, 292, 88, color=BLUE, head=True)
    s.text(272, 112, "s", fill=BLUE, anchor="middle")
    for y, a, b in ((55, "ρ_2", "ρ_1"), (90, "v_p", "v_1 = 0"), (125, "p_2", "p_1 = 0")):
        s.text(185, y, a, anchor="middle")
        s.text(380, y, b, anchor="middle")
    s.save(OUT / "piston-setup.svg")


if __name__ == "__main__":
    piston()
    print("wrote", OUT)
