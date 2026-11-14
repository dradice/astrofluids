#!/usr/bin/env python3
"""Figures of Ch. 13 (stellar winds), after the handwritten lecture notes (winds.pdf) and the
2023 slides. The slides showed figures from Lamers & Cassinelli; the solution topology is
computed here from the Parker solution instead, and the P Cygni profile is a sketch.

Usage: python3 figures-src/winds-and-accretion/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "winds-and-accretion"


def parker_branches(K, x0, x1, n=400, cluster=None):
    """Solutions of ln w - w^2/2 + 2 ln x + 2/x = K, with w = v/c_iso and x = r/r_c, for
    x0 <= x <= x1. Returns the subsonic and the supersonic branch as lists of (x, w).
    cluster = "hi" or "lo" puts more points near that end (where the curve is vertical)."""
    def g(x):
        return K - 2 * math.log(x) - 2 / x

    def phi(w):
        return math.log(w) - w * w / 2

    sub, sup = [], []
    for i in range(n + 1):
        t = i / n
        if cluster == "hi":
            t = 1 - (1 - t) ** 3
        elif cluster == "lo":
            t = t ** 3
        x = x0 + (x1 - x0) * t
        gx = g(x)
        if gx >= -0.5 - 1e-12:
            continue
        sub.append((x, brentq(lambda w: phi(w) - gx, 1e-300, 1)))
        sup.append((x, brentq(lambda w: phi(w) - gx, 1, 60)))
    return sub, sup


def turning_points(K):
    """Radii where the curve of constant K has w = 1 (only for K > 3/2)."""
    def h(x):
        return 2 * math.log(x) + 2 / x - K - 0.5
    return brentq(h, 1e-3, 1), brentq(h, 1, 1e3)


def solutions():
    s = Svg(630, 370, "Solutions of the isothermal wind equation",
            "Curves of v/c_iso against r/r_c, from 0 to 4, for different values of the "
            "integration constant. Two critical solutions cross at r = r_c, v = c_iso, marked "
            "by a dot. The wind, a thick black line, starts subsonic near the star, accelerates "
            "and becomes supersonic at r_c, and keeps accelerating slowly. The accretion "
            "solution, a thick red dashed line, is subsonic at large radii and supersonic inside "
            "r_c. Thin grey curves show the other solutions: some are subsonic everywhere, with "
            "a maximum of v at r_c; some are supersonic everywhere, with a minimum of v at r_c; "
            "others are double valued, either at small radii, where the velocity reaches c_iso "
            "with an infinite slope before r_c, or at large radii, where they never reach r_c.",
            "parker")
    x0, y0, sx, sy = 70, 330, 120, 100

    def px(x, w):
        return (x0 + sx * x, y0 - sy * w)

    xmax, wmax = 4.0, 3.0
    s.raw(f'<clipPath id="parker-clip"><rect x="{x0}" y="{y0 - sy * wmax}" '
          f'width="{sx * xmax}" height="{sy * wmax}"/></clipPath>')

    def curve(pts, color, w, dash=None):
        d = "M " + " L ".join(f"{px(x, v)[0]:.1f} {px(x, v)[1]:.1f}" for x, v in pts)
        s.path(d, color, w, dash=dash, extra='clip-path="url(#parker-clip)"')

    for K in (0.6, 1.1):  # subsonic and supersonic everywhere
        sub, sup = parker_branches(K, 0.08, xmax)
        curve(sub, "#777", 1.3)
        curve(sup, "#777", 1.3)
    for K in (1.9, 2.4):  # double valued, on either side of r_c
        a, b = turning_points(K)
        sub, sup = parker_branches(K, 0.05, a, 600, cluster="hi")
        curve(sub + [(a, 1.0)] + sup[::-1], "#777", 1.3)
        sub, sup = parker_branches(K, b, xmax + 0.5, 600, cluster="lo")
        curve(sub[::-1] + [(b, 1.0)] + sup, "#777", 1.3)
    sub_in, sup_in = parker_branches(1.5, 0.08, 1 - 1e-6)
    sub_out, sup_out = parker_branches(1.5, 1 + 1e-6, xmax)
    curve(sub_in + [(1, 1)] + sup_out, "#000", 3.0)
    curve(sup_in + [(1, 1)] + sub_out, RED, 3.0, dash="9 6")
    s.circle(*px(1, 1), 5, fill="#000", stroke="#000")

    s.line(x0, y0, x0, 22, head=True)
    s.line(x0, y0, x0 + sx * xmax + 30, y0, head=True)
    s.text(x0 - 6, 14, "v/c_{iso}", anchor="end")
    s.text(x0 + sx * xmax + 70, y0 + 26, "r/r_c", anchor="end")
    for x in (1, 2, 3, 4):
        s.line(px(x, 0)[0], y0, px(x, 0)[0], y0 + 6)
        s.text(px(x, 0)[0], y0 + 26, str(x), anchor="middle", italic=False, size=18)
    for w in (1, 2, 3):
        s.line(x0 - 6, px(0, w)[1], x0, px(0, w)[1])
        s.text(x0 - 10, px(0, w)[1] + 6, str(w), anchor="end", italic=False, size=18)
    s.line(*px(0, 1), *px(xmax, 1), color="#999", w=1, dash="3 4")
    s.line(*px(1, 0), *px(1, wmax), color="#999", w=1, dash="3 4")
    s.text(*px(3.15, 2.37), "wind", italic=False, size=19)
    s.text(*px(3.15, 0.45), "accretion", fill=RED, italic=False, size=19)
    s.save(OUT / "parker-solutions.svg")


def pcygni():
    s = Svg(560, 300, "Sketch of a P Cygni line profile",
            "Flux, in units of the continuum flux, against the Doppler velocity in units of the "
            "terminal velocity of the wind, from -1.5 to 1.5. The continuum is a dashed "
            "horizontal line at 1. On the blue side, between -1 and 0, the flux drops below the "
            "continuum in a deep absorption trough, which ends sharply at -1. On the red side "
            "there is an emission peak, about 1.5 times the continuum, just above zero velocity, "
            "which decreases to the continuum at +1.", "pcygni")
    x0, y0, sx, sy = 280, 250, 150, 110

    def px(x, f):
        return (x0 + sx * x, y0 - sy * f)

    def flux(x):
        emis = 0.55 * math.exp(-((x - 0.12) / 0.38) ** 2) * (1 - min(abs(x), 1) ** 4)
        absn = 0.0
        if -1 < x < 0:
            u = -x
            absn = 0.85 * (1 - math.exp(-(u / 0.12) ** 2)) * (1 - math.exp(-(1 - u) / 0.04))
            absn *= 1 - 0.35 * (1 - u)
        return max(1 + emis - absn, 0.05)

    xs = [-1.5 + 3 * i / 1200 for i in range(1201)]
    s.line(px(-1.5, 0)[0], y0, px(1.5, 0)[0] + 25, y0, head=True)
    s.line(x0, y0, x0, 20, head=True)
    s.line(*px(-1.5, 1), *px(1.5, 1), color="#999", w=1.2, dash="6 5")
    s.poly([px(x, flux(x)) for x in xs], "#000", 2.4)
    for x, lab in ((-1, "−1"), (1, "1")):
        s.line(px(x, 0)[0], y0, px(x, 0)[0], y0 + 6)
        s.text(px(x, 0)[0], y0 + 26, lab, anchor="middle", italic=False, size=18)
    s.text(x0 - 8, y0 + 26, "0", anchor="end", italic=False, size=18)
    s.text(px(1.5, 0)[0] + 20, y0 + 40, "v/v_∞", anchor="end")
    s.text(x0 - 8, 32, "F/F_c", anchor="end")
    s.line(x0 - 6, px(0, 1)[1], x0, px(0, 1)[1])
    s.text(px(-1.5, 1)[0], px(0, 1)[1] - 8, "continuum", italic=False, size=17)
    s.text(px(-1.04, 0.4)[0], px(0, 0.4)[1], "absorption", anchor="end", fill=BLUE,
           italic=False, size=17)
    s.text(px(0.35, 1.58)[0], px(0, 1.58)[1], "emission", fill=RED, italic=False, size=17)
    s.save(OUT / "p-cygni.svg")


def nozzle():
    s = Svg(560, 260, "A de Laval nozzle",
            "A pipe whose cross-sectional area A(s) decreases to a minimum, the throat, and "
            "then increases again. The gas flows from left to right. It is subsonic, Ma < 1, "
            "before the throat, it reaches Ma = 1 at the throat, and it is supersonic, Ma > 1, "
            "after it.", "nozzle")
    xc, yc = 280, 120

    def half(x):
        u = (x - xc) / 220
        return 22 + 68 * u * u

    xs = [60 + 440 * i / 200 for i in range(201)]
    s.poly([(x, yc - half(x)) for x in xs], "#000", 3)
    s.poly([(x, yc + half(x)) for x in xs], "#000", 3)
    s.line(xc, yc - half(xc), xc, yc + half(xc), color="#999", w=1.2, dash="4 4")
    for x in (110, 400):
        s.line(x - 28, yc, x + 28, yc, color=BLUE, head=True)
    s.line(xc - 20, yc, xc + 20, yc, color=BLUE, head=True)
    s.text(110, 238, "Ma < 1", anchor="middle", italic=False, size=18)
    s.text(xc, 238, "Ma = 1", anchor="middle", italic=False, size=18)
    s.text(430, 238, "Ma > 1", anchor="middle", italic=False, size=18)
    s.text(xc, yc - half(xc) - 12, "throat", anchor="middle", italic=False, size=17)
    s.line(400, yc + half(400) + 2, 400, yc - half(400) - 2, w=1.2, head=True, tail=True)
    s.text(410, yc + half(400) - 6, "A(s)", size=19)
    s.save(OUT / "nozzle.svg")


def cylinder():
    s = Svg(520, 300, "Potential flow around a cylinder",
            "Streamlines of an incompressible, irrotational flow around a cylinder, shown as a "
            "grey disk. Far from the cylinder the streamlines are straight horizontal lines. "
            "Near the cylinder they bend around it symmetrically, so that the pattern is the "
            "same in front of and behind the cylinder. The flow splits at a stagnation point "
            "on the left of the cylinder and joins again at a stagnation point on the right.",
            "cylinder")
    xc, yc, R = 260, 150, 55  # R in px; lengths below are in units of R

    def y_of(x, c):
        """y > 0 on the streamline y (1 - R^2/(x^2 + y^2)) = c (lengths in units of R)."""
        f = lambda y: y * (1 - 1 / (x * x + y * y)) - c  # noqa: E731
        lo = math.sqrt(max(1 - x * x, 0)) + 1e-9
        return brentq(f, lo, 10)

    xs = [-4.4 + 8.8 * i / 400 for i in range(401)]
    for c in (0.1, 0.3, 0.6, 1.0, 1.5, 2.1):
        for sgn in (1, -1):
            pts = [(xc + R * x, yc - sgn * R * y_of(x, c)) for x in xs]
            s.poly(pts, BLUE, 1.6)
    s.line(xc - R * 4.4, yc, xc - R, yc, color=BLUE, w=1.6)
    s.line(xc + R, yc, xc + R * 4.4, yc, color=BLUE, w=1.6)
    s.circle(xc, yc, R, fill=GRAY, stroke="#000", w=1.6)
    s.line(20, 22, 70, 22, color="#000", head=True)
    s.text(78, 28, "U", size=20)
    s.save(OUT / "potential-flow-cylinder.svg")


def kelvin():
    s = Svg(620, 270, "Area swept by a curve that moves with the fluid",
            "A closed curve C(t), drawn as a solid black line with an arrow showing its "
            "counterclockwise orientation, encloses the surface A(t). A short element dl of the "
            "curve is drawn as an arrow along it. In a time dt the fluid carries the curve to a "
            "new position, C(t + dt), drawn as a dashed line, displaced to the upper right and "
            "slightly stretched. Each point of dl moves by v dt, drawn as an arrow from the start "
            "of dl. The element sweeps a small shaded parallelogram with sides dl and v dt, "
            "whose area is dA = v dt × dl.", "kelvin")
    cx, cy, R = 215, 140, 110  # centre and size of C(t) in px; lengths below in units of R
    dt = 0.32  # exaggerated, so that the displacement is visible

    def curve(th):
        r = 1 + 0.10 * math.cos(2 * th) + 0.07 * math.sin(3 * th)
        return (r * math.cos(th), 0.8 * r * math.sin(th))

    def vel(p):
        return (0.75 + 0.30 * p[0], 0.35 + 0.25 * p[1])

    def moved(p):
        u = vel(p)
        return (p[0] + u[0] * dt, p[1] + u[1] * dt)

    def px(p):
        return (cx + R * p[0], cy - R * p[1])

    ths = [2 * math.pi * i / 300 for i in range(301)]
    s.path("M " + " L ".join("%.1f %.1f" % px(moved(curve(t))) for t in ths) + " Z",
           "#555", 1.6, dash="7 5")
    s.poly([px(curve(t)) for t in ths], "#000", 2.4, closed=True)
    # orientation of C(t)
    a, b = px(curve(2.05)), px(curve(2.2))
    s.line(*a, *b, w=2.4, head=True)
    # the element dl and the parallelogram it sweeps
    t1, t2 = -0.62, -0.12
    p1, p2 = curve(t1), curve(t2)
    q1, q2 = moved(p1), moved(p2)
    s.poly([px(p1), px(p2), px(q2), px(q1)], BLUE, 1.2, fill="#c9d6f2", closed=True)
    s.line(*px(p1), *px(p2), color="#000", w=2.6, head=True)
    s.line(*px(p1), *px(q1), color=RED, w=2.2, head=True)
    s.circle(*px(p1), 3, fill="#000")
    # labels
    x, y = px(((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2))
    s.raw(f'<text x="{x - 12:.0f}" y="{y + 6:.0f}" text-anchor="end" font-size="20">'
          f'd<tspan font-weight="bold">l</tspan></text>')
    x, y = px(((p1[0] + q1[0]) / 2, (p1[1] + q1[1]) / 2))
    s.raw(f'<text x="{x + 2:.0f}" y="{y + 26:.0f}" font-size="20" fill="{RED}">'
          f'<tspan font-weight="bold">v</tspan> d<tspan font-style="italic">t</tspan></text>')
    x, y = px(((p1[0] + p2[0] + q1[0] + q2[0]) / 4, (p1[1] + p2[1] + q1[1] + q2[1]) / 4))
    s.line(x + 4, y + 2, 452, 213, w=1.2)
    s.raw(f'<text x="458" y="221" font-size="20" fill="{BLUE}">'
          f'd<tspan font-weight="bold">A</tspan> = <tspan font-weight="bold">v</tspan> '
          f'd<tspan font-style="italic">t</tspan> × d<tspan font-weight="bold">l</tspan></text>')
    s.text(cx - 40, cy + 8, "A(t)", size=22)
    x, y = px(curve(2.6))
    s.text(x - 8, y - 4, "C(t)", anchor="end")
    x, y = px(moved(curve(0.75)))
    s.raw(f'<text x="{x + 10:.0f}" y="{y - 8:.0f}" font-size="20" fill="#555">'
          f'<tspan font-style="italic">C</tspan>(<tspan font-style="italic">t</tspan> + '
          f'd<tspan font-style="italic">t</tspan>)</text>')
    s.save(OUT / "kelvin-swept-area.svg")


if __name__ == "__main__":
    kelvin()
    solutions()
    pcygni()
    nozzle()
    cylinder()
