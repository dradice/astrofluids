#!/usr/bin/env python3
"""Homologous expansion of a sphere: three snapshots (Ch. 1).

Each marked fluid element keeps its initial velocity v = H q (q = initial radius), so the
arrows have the same length in every snapshot while the positions scale as 1 + H t.

Usage: python3 figures-src/fluids-as-continua/homologous-expansion.py   (from notes/)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "fluids-as-continua"

R0 = 46                        # initial radius in px
FACTORS = [1.0, 1.6, 2.2]      # 1 + H t for the three snapshots
CENTERS = [85, 285, 545]
YC = 150
FILLS = ["#a6a6a6", "#d4d4d4", "#ececec"]   # density drops as (1 + H t)^-3
ARROW = 0.7                    # arrow length per px of initial radius (v = H q)
LABELS = ["t = 0", "t_1", "t_2"]

s = Svg(700, 300, "Homologous expansion of a sphere of gas",
        "Three snapshots of an expanding sphere of gas, at time zero and at two later times. "
        "The sphere grows and its shading becomes lighter as the density decreases. Six marked "
        "fluid elements at half the radius and six at the surface move outward along straight "
        "radial lines. Each element carries a velocity arrow whose length does not change "
        "from one snapshot to the next, because the elements coast; the arrows of the outer "
        "elements are twice as long as those of the inner ones. The pattern of elements is the "
        "same in every snapshot, only scaled up.", "homologous")

for f, cx, fill, lab in zip(FACTORS, CENTERS, FILLS, LABELS):
    s.circle(cx, YC, R0 * f, fill=fill, stroke="#000", w=1.6)
    for k in range(6):
        a = math.pi / 6 + k * math.pi / 3
        ux, uy = math.cos(a), -math.sin(a)
        for q in (0.5 * R0, R0):
            x, y = cx + q * f * ux, YC + q * f * uy
            L = ARROW * q
            s.line(x, y, x + L * ux, y + L * uy, color=BLUE, w=2, head=True)
            s.circle(x, y, 4, fill="#000", stroke="#000", w=1)
    s.circle(cx, YC, 2.5, fill="#000", stroke="#000", w=1)
    s.text(cx, 290, lab, anchor="middle")

s.save(OUT / "homologous-expansion.svg")
