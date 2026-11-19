#!/usr/bin/env python3
"""Figures of the turbulence chapter drawn after the handwritten lecture notes on
turbulence modeling (filtering, and the velocity fluctuations v(l) across scales).
The Richardson cascade is made by richardson-cascade.py.

Usage: python3 figures-src/turbulence/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "turbulence"
RED = "#b3202a"


def polyline(xs, ys):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in zip(xs, ys))


def filtering():
    s = Svg(680, 270, "Filtering a turbulent velocity field",
            "Left: a bell-shaped filter kernel K of width l. Right: a velocity profile with "
            "structure on many scales (black), its filtered part, a smooth large-scale wave "
            "(blue), and the small-scale fluctuations left over (red), which oscillate "
            "around zero.", "filt")

    # kernel
    x0, y0, h, sig = 125, 215, 150, 26
    s.line(25, y0, 235, y0, w=1.5)
    s.line(x0, y0 + 10, x0, 35, w=1.5)
    xs = np.linspace(30, 220, 200)
    s.path(polyline(xs, y0 - h * np.exp(-0.5 * ((xs - x0) / sig) ** 2)), w=2)
    half = sig * math.sqrt(2 * math.log(2))
    yh = y0 - h / 2
    s.line(x0 - half + 2, yh, x0 + half - 2, yh, w=1.4, head=True, tail=True)
    s.text(x0 + 9, yh + 24, "ℓ")
    s.text(x0 + 22, y0 - h + 6, "K")
    s.text(232, y0 + 26, "x − x′", anchor="end")

    # signal, filtered signal, fluctuations
    rng = np.random.default_rng(7)
    n = 1200
    t = np.linspace(0, 1, n)
    big = 1.1 + 0.75 * np.sin(2 * math.pi * (1.35 * t + 0.1))
    small = np.zeros(n)
    for k in range(18, 70):
        small += k ** (-1 / 3) * np.sin(2 * math.pi * k * t + rng.uniform(0, 2 * math.pi))
    small *= 0.13 / small.std()
    v = big + small
    sig_n = 0.018 * n
    m = int(4 * sig_n)
    ker = np.exp(-0.5 * (np.arange(-m, m + 1) / sig_n) ** 2)
    ker /= ker.sum()
    vbar = np.convolve(np.pad(v, m, mode="reflect"), ker, mode="valid")
    dv = v - vbar

    X0, X1, Y0, sc = 290, 625, 215, 72
    s.line(X0 - 10, Y0, X1 + 25, Y0, w=1.5)
    s.line(X0, Y0 + 30, X0, 28, w=1.5)
    xs = X0 + 8 + (X1 - X0 - 8) * t
    s.path(polyline(xs, Y0 - sc * v), w=1.2)
    s.path(polyline(xs, Y0 - sc * vbar), color=BLUE, w=2.4)
    s.path(polyline(xs, Y0 - sc * dv), color=RED, w=1.2)
    yv = Y0 - sc * v[-1]
    s.text(X1 + 10, yv - 4, "v", bold=True)
    xb, yb = X1 - 95, Y0 - sc * 2.05 - 6
    s.text(xb, yb, "v", bold=True, fill=BLUE)
    s.line(xb + 1, yb - 17, xb + 11, yb - 17, color=BLUE, w=1.4)
    s.text(X1 + 10, Y0 + 30, "δ", fill=RED)
    s.text(X1 + 20, Y0 + 30, "v", bold=True, fill=RED)
    s.save(OUT / "filtering.svg")


def velocity_scaling():
    s = Svg(540, 330, "Velocity fluctuations across scales",
            "Log-log sketch of v(l) against l. Below the dissipation scale l_d, v grows "
            "linearly with l; in the inertial range between l_d and l_0 it grows as l to "
            "the one third; above l_0 it is constant.", "vl")
    X0, Y0, px = 70, 275, 80  # pixels per decade on both axes
    ld, l0 = 1.0, 1000.0
    s.line(X0 - 10, Y0, 505, Y0, w=1.5)
    s.line(X0, Y0 + 10, X0, 25, w=1.5)
    lx = np.linspace(-1.35, 3.95, 300)
    ll = 10 ** lx
    v = ll / ld / (1 + (ll / ld) ** 2) ** (1 / 3) / (1 + (ll / l0) ** 2) ** (1 / 6)
    xs = X0 + 15 + px * (lx - lx[0])
    ys = Y0 - 15 - px * (np.log10(v) - np.log10(v[0]))
    s.path(polyline(xs, ys), w=2.2)

    def x_of(l):
        return X0 + 15 + px * (math.log10(l) - lx[0])

    def y_of(l):
        vv = l / ld / (1 + (l / ld) ** 2) ** (1 / 3) / (1 + (l / l0) ** 2) ** (1 / 6)
        return Y0 - 15 - px * (math.log10(vv) - math.log10(v[0]))

    for l, lab in ((ld, "ℓ_d"), (l0, "ℓ_0")):
        s.line(x_of(l), y_of(l) + 6, x_of(l), Y0, w=1.3, dash="5 5")
        s.text(x_of(l), Y0 + 26, lab, anchor="middle")
    s.text(x_of(0.1) + 8, y_of(0.1) + 4, "∝ ℓ", italic=True)
    s.text(x_of(30) + 4, y_of(30) - 16, "∝ ℓ\u2009^{1/3}", anchor="end")
    s.text(478, Y0 + 26, "log", italic=False, anchor="end")
    s.text(483, Y0 + 26, "ℓ")
    s.text(X0 + 8, 30, "log", italic=False)
    s.text(X0 + 40, 30, "v(ℓ)")
    s.save(OUT / "velocity-scaling.svg")


if __name__ == "__main__":
    filtering()
    velocity_scaling()
