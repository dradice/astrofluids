#!/usr/bin/env python3
"""Figures of Ch. 12 (blast waves), after the handwritten lecture notes on supernova remnants
and the 2023 slides. The Sedov profiles are computed here (the slides showed Shu's figure).
The worksheet plot is made by fireball-data.py.

Usage: python3 figures-src/blast-waves/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "blast-waves"


def sedov_solution(G=5 / 3):
    """Sedov solution in the variables of the text: x = r/r_sh = xi/xi_0 and
    rho = rho_2 R(x), v = v_2 x V(x), p = p_2 x^2 P(x). Returns x, R, V, P and xi_0."""
    a, k = 2 / (G + 1), (G - 1) / (G + 1)

    def rhs(s, y):  # s = ln x; the three ODEs of the text are linear in the derivatives
        R, V, P = y
        Q, W = P + R * V * V, G * P + R * V * V
        M = np.array([[a * V - 1, a * R, 0],
                      [0, -0.4 + 0.4 * a * V, 0.4 * k / R],
                      [-0.4 * V * V + 0.4 * a * V ** 3,
                       -0.8 * R * V + 0.4 * a * (W + 2 * R * V * V), -0.4 + 0.4 * a * G * V]])
        b = np.array([-3 * a * R * V, V - 0.4 * a * V * V - 0.8 * k * P / R,
                      2 * Q - 2 * a * V * W])
        return np.linalg.solve(M, b)

    sol = solve_ivp(rhs, [0, -12], [1, 1, 1], rtol=1e-10, atol=1e-12, dense_output=True)
    s = np.linspace(-12, 0, 4001)
    R, V, P = sol.sol(s)
    x = np.exp(s)
    integral = np.trapezoid((P + R * V * V) * x ** 4, x)
    xi0 = (25 * (G * G - 1) / (32 * math.pi) / integral) ** 0.2
    return x, R, V, P, xi0


def free_expansion():
    s = Svg(720, 260, "Free expansion and the reverse shock",
            "Two sketches of the density rho against r/r_sh. Left: at early times the "
            "supernova ejecta, a high plateau, end at r/r_sh = 1 and move outwards into the "
            "interstellar medium, a low plateau. Right: at later times a reverse shock, moving "
            "inwards with respect to the gas, separates the ejecta from a higher plateau of "
            "shocked gas, which ends at the forward shock at r/r_sh = 1; beyond it is the cold "
            "interstellar medium.", "free-expansion")
    for x0, panel in ((40, 0), (400, 1)):
        y0, w = 200, 300
        s.line(x0, y0, x0, 25, head=True)
        s.line(x0 - 10, y0, x0 + w, y0, head=True)
        s.text(x0 - 10, 35, "ρ", anchor="end")
        s.text(x0 + w - 4, y0 + 40, "r/r_{sh}", anchor="end")
        x1 = x0 + 200
        s.line(x1, y0, x1, y0 + 6)
        s.text(x1, y0 + 26, "1", anchor="middle", italic=False)
        if panel == 0:
            s.poly([(x0, 90), (x1, 90), (x1, 170), (x0 + w - 15, 170)], "#000", 2.4)
            s.line(x1 - 18, 130, x1 + 22, 130, head=True)
            s.text(x0 + 70, 145, "ejecta", italic=False, size=18)
            s.text(x1 + 30, 160, "ISM", italic=False, size=18)
        else:
            xr = x0 + 140
            s.poly([(x0, 130), (xr, 130), (xr, 70), (x1, 70), (x1, 170), (x0 + w - 15, 170)],
                   "#000", 2.4)
            s.text(x0 + 30, 160, "ejecta", italic=False, size=18)
            s.text((xr + x1) / 2, 60, "shocked gas", anchor="middle", italic=False, size=17)
            s.line(xr + 20, 100, xr - 22, 100, color=BLUE, head=True)
            s.text(xr - 5, 32, "reverse shock", anchor="middle", fill=BLUE, italic=False, size=17)
            s.line(xr, 38, xr, 62, color=BLUE, w=1.2)
            s.text(x1 + 12, 120, "forward", fill=BLUE, italic=False, size=17)
            s.text(x1 + 12, 140, "shock", fill=BLUE, italic=False, size=17)
            s.text(x1 + 30, 192, "cold ISM", italic=False, size=17)
    s.save(OUT / "free-expansion.svg")


def sedov_profiles():
    x, R, V, P, xi0 = sedov_solution()
    s = Svg(560, 360, "The Sedov solution",
            "Profiles of the Sedov solution for Gamma = 5/3 against r/r_sh, from 0 to 1.25. "
            "The pressure p/p_2, in black, is about 0.31 at the centre, rises slowly and then "
            "steeply to 1 at the shock. The velocity v/v_2, in blue, grows almost linearly from "
            "0 at the centre to 1 at the shock. The density rho/rho_2, in red, is close to zero "
            "in most of the interior and rises steeply to 1 just behind the shock; outside the "
            "shock it drops to rho_1/rho_2 = 1/4.", "sedov")
    x0, y0, sx, sy = 70, 300, 360, 250

    def px(u, v):
        return (x0 + sx * u, y0 - sy * v)

    s.line(x0, y0, x0, 25, head=True)
    s.line(x0, y0, 540, y0, head=True)
    s.text(530, y0 + 40, "r/r_{sh}", anchor="end")
    for u, lab in ((0, "0"), (1, "1")):
        s.line(px(u, 0)[0], y0, px(u, 0)[0], y0 + 6)
        s.text(px(u, 0)[0], y0 + 26, lab, anchor="middle", italic=False)
    for v, lab in ((1, "1"), (0.306, "0.31")):
        s.line(x0 - 6, px(0, v)[1], x0, px(0, v)[1])
        s.text(x0 - 10, px(0, v)[1] + 6, lab, anchor="end", italic=False, size=18)
    s.line(px(1, 0)[0], y0, px(1, 0)[0], px(1, 1)[1], color="#999", w=1, dash="3 4")
    for f, color in ((x * x * P, "#000"), (x * V, BLUE), (R, RED)):
        s.poly([px(u, v) for u, v in zip(x[::4], f[::4])], color, 2.2)
    s.poly([px(1, 0.25), px(1.25, 0.25)], RED, 2.2)
    s.text(px(0.12, 0.31)[0], px(0, 0.31)[1] - 12, "p/p_2", size=19)
    s.text(px(0.62, 0.62)[0] - 4, px(0, 0.62)[1] - 6, "v/v_2", anchor="end", fill=BLUE, size=19)
    s.text(px(0.40, 0.03)[0], px(0, 0.03)[1] - 10, "ρ/ρ_2", fill=RED, size=19)
    s.text(px(1.04, 0.25)[0], px(0, 0.25)[1] - 10, "ρ_1/ρ_2", fill=RED, size=19)
    s.save(OUT / "sedov-profiles.svg")
    return xi0


def snowplough():
    s = Svg(560, 330, "Structure of a remnant in the snowplough phase",
            "Sketch of the pressure p/p_max, in red, and of the density rho/rho_max, in black, "
            "against r/r_sh. The pressure is constant in the hot bubble that fills the interior "
            "and drops at the shell. The density is low in the interior and rises to a narrow "
            "peak, the cold shell, just inside r/r_sh = 1, which moves outwards at speed "
            "v_shell, about U_sh. Outside the shell the density is that of the ISM.", "snowplough")
    x0, y0, w, h = 60, 260, 360, 200
    s.line(x0, y0, x0, 25, head=True)
    s.line(x0, y0, 540, y0, head=True)
    s.text(530, y0 + 40, "r/r_{sh}", anchor="end")
    x1 = x0 + w
    s.line(x1, y0, x1, y0 + 6)
    s.text(x1, y0 + 26, "1", anchor="middle", italic=False)
    s.line(x0 - 6, y0 - h, x0, y0 - h)
    s.text(x0 - 10, y0 - h + 6, "1", anchor="end", italic=False)

    def rho(u):
        if u > 1:
            return 0.06
        return 0.02 + 0.98 * math.exp(-(1 - u) / 0.018) + 0.10 * math.exp(-(1 - u) / 0.12)

    def pres(u):
        if u > 1:
            return 0.0
        return 1 / (1 + math.exp((u - 0.975) / 0.006))

    us = [i / 1000 for i in range(0, 1001)]
    s.poly([(x0 + w * u, y0 - h * pres(u)) for u in us] + [(x1, y0 - 1), (x0 + w * 1.3, y0 - 1)],
           RED, 2.2)
    s.poly([(x0 + w * u, y0 - h * rho(u)) for u in us] + [(x1, y0 - h * 0.06),
                                                         (x0 + w * 1.3, y0 - h * 0.06)], "#000", 2.2)
    s.text(x0 + 80, y0 - h - 12, "p/p_{max}", fill=RED, size=19)
    s.text(x1 + 18, y0 - h * 0.30, "ρ/ρ_{max}", size=19)
    s.text(x0 + 110, y0 - 70, "hot bubble", italic=False, size=18)
    s.text(x1 - 150, y0 + 46, "cold shell", italic=False, size=18)
    s.path(f"M {x1 - 90} {y0 + 30} C {x1 - 40} {y0 + 25} {x1 - 15} {y0 + 10} {x1 - 8} {y0 - 6}",
           "#000", 1.4, head=True)
    s.line(x1 - 2, 52, x1 + 34, 52, head=True)
    s.text(x1 + 40, 58, "v_{shell} ≈ U_{sh}", size=19)
    s.save(OUT / "snowplough.svg")


def phases():
    s = Svg(560, 300, "Shock velocity in the three phases of a supernova remnant",
            "Sketch of the shock velocity U_sh against time t, both on logarithmic axes. In the "
            "free-expansion phase, up to t_0, U_sh is constant. In the Sedov–Taylor phase, between t_0 "
            "and t_1, it decreases as t to the power -3/5. At t_1 it drops, and in the "
            "snowplough phase it decreases as t to the power -5/7.", "phases")
    x0, y0 = 70, 230
    s.line(x0, y0, x0, 20, head=True)
    s.line(x0, y0, 540, y0, head=True)
    s.text(x0 - 10, 32, "U_{sh}", anchor="end")
    s.text(530, y0 + 40, "t", anchor="end")
    t0, t1, t2 = 200, 370, 510
    ya = 55
    yb = ya + (t1 - t0) * 0.6 * 0.55
    yc = yb + 18
    yd = yc + (t2 - t1) * 5 / 7 * 0.55
    s.poly([(x0 + 15, ya), (t0, ya), (t1, yb)], "#000", 2.4)
    s.poly([(t1, yb), (t1, yc), (t2, yd)], "#000", 2.4)
    for x, lab in ((t0, "t_0"), (t1, "t_1")):
        s.line(x, y0, x, y0 + 6)
        s.text(x, y0 + 28, lab, anchor="middle")
        s.line(x, y0, x, 40, color="#999", w=1, dash="3 4")
    s.text((t0 + t1) / 2 + 10, (ya + yb) / 2 - 12, "t^{−3/5}")
    s.text((t1 + t2) / 2 + 10, (yc + yd) / 2 - 12, "t^{−5/7}")
    for xc, l1, l2 in (((x0 + t0) / 2, "free", "expansion"), ((t0 + t1) / 2, "Sedov–Taylor", ""),
                       ((t1 + t2) / 2, "snowplough", "")):
        s.text(xc, y0 - 34, l1, anchor="middle", italic=False, size=17)
        if l2:
            s.text(xc, y0 - 14, l2, anchor="middle", italic=False, size=17)
    s.save(OUT / "phases.svg")


if __name__ == "__main__":
    free_expansion()
    xi0 = sedov_profiles()
    snowplough()
    phases()
    print(f"xi_0 = {xi0:.4f} (Gamma = 5/3)")
