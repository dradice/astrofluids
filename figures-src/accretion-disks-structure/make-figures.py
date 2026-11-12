#!/usr/bin/env python3
"""Sketch for the solution of Exercise 18.1 (vertical gravity in a disk), redrawn from the 2025 drawing.

Usage: python3 figures-src/accretion-disks-structure/make-figures.py   (from the notes/ directory)
The plot figure of Exercise 18.3 is made by solutions/code/accretion-disks-structure/accretion-disk.py.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "accretion-disks-structure"


def vertical_gravity():
    s = Svg(400, 220, "Vertical component of the gravitational acceleration in a disk",
            "A right triangle with a horizontal leg of length R along the disk midplane, a vertical "
            "leg of height z, and the hypotenuse of length r pointing to the central object at the "
            "left. A fluid element, drawn as a small square at the top of the vertical leg, feels the "
            "gravitational acceleration g directed along the hypotenuse towards the central object; "
            "its vertical component g_z points down.", "vertgrav")
    A, B, C = (50, 180), (320, 180), (320, 95)
    s.line(*A, *B)
    s.line(*B, *C)
    s.line(*A, *C)
    s.rect(C[0] - 17, C[1] - 17, 34, 34, stroke="#000", sw=2.4)
    # g: from the element towards the central object, along the hypotenuse
    ux, uy = (A[0] - C[0]), (A[1] - C[1])
    n = (ux * ux + uy * uy) ** 0.5
    s.line(C[0], C[1], C[0] + 130 * ux / n, C[1] + 130 * uy / n, w=2.6, head=True)
    s.line(C[0], C[1], C[0], C[1] + 52, w=2.6, head=True)
    s.text(245, 98, "g", anchor="middle", bold=True, italic=False)
    s.text(296, 145, "g_z", anchor="middle")
    s.text(335, 145, "z")
    s.text(170, 134, "r", anchor="middle")
    s.text(185, 207, "R", anchor="middle")
    s.save(OUT / "vertical-gravity.svg")


if __name__ == "__main__":
    vertical_gravity()
