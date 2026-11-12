#!/usr/bin/env python3
"""Figures of Ch. 11 (shock waves). The piston of Exercise 11.1 and the colliding clouds of
Exercise 11.2 are redrawn from the 2025 TeXmacs drawings; the radiative-shock figures follow
the 2025 slides (after Mihalas & Mihalas 1984 and Shu 1992); the others follow the
handwritten lecture notes.

Usage: python3 figures-src/shock-waves/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "shock-waves"


def piston():
    s = Svg(480, 170, "A piston driving a shock into a cold gas",
            "A tube with a piston on the left, shown as a gray block with a handle. The piston "
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


def weak_solution():
    s = Svg(460, 300, "A discontinuity in the x-t plane",
            "Axes t, vertical, and x, horizontal. A thick line starts at the origin and reaches "
            "x = sT at time T: it is the discontinuity, moving with speed s. To its left the "
            "solution is U_L, to its right U_R. A horizontal line at t = T and a dashed vertical "
            "line at x = X bound the integration region.", "weak-solution")
    x0, y0, sx, ty = 60, 255, 300, 190  # origin, pixels per X, pixels per T
    s.line(x0, y0, x0, 25, head=True)
    s.line(x0, y0, 440, y0, head=True)
    s.text(x0 - 12, 30, "t", anchor="end")
    s.text(430, y0 + 28, "x", anchor="middle")
    s.text(x0 - 10, y0 + 22, "0", anchor="end")
    s.line(x0, y0 - ty, 430, y0 - ty)
    s.text(x0 - 10, y0 - ty + 7, "T", anchor="end")
    xs = x0 + 0.55 * sx
    s.line(x0, y0, xs, y0 - ty, w=3.4)
    s.text(xs, y0 - ty - 10, "sT", anchor="middle")
    s.line(x0 + sx, y0, x0 + sx, y0 - ty, dash="6 4")
    s.text(x0 + sx, y0 + 28, "X", anchor="middle")
    s.text(x0 + 40, y0 - 120, "U_L")
    s.text(x0 + 215, y0 - 80, "U_R")
    s.text(x0 + 0.30 * sx + 12, y0 - 0.30 * ty + 10, "s")
    s.save(OUT / "weak-solution.svg")


def shock_frame():
    s = Svg(440, 170, "A shock in its rest frame",
            "A tube crossed by a thick vertical line, the shock. An arrow shows the gas flowing "
            "from left to right. On the left, upstream, the gas has density rho_1, velocity u_1 "
            "and pressure p_1. On the right, downstream, it has density rho_2, velocity u_2 and "
            "pressure p_2.", "shock-frame")
    s.line(20, 45, 420, 45)
    s.line(20, 155, 420, 155)
    s.line(220, 45, 220, 155, color=BLUE, w=3.4)
    s.text(120, 30, "upstream", anchor="middle", italic=False)
    s.text(320, 30, "downstream", anchor="middle", italic=False)
    s.line(160, 75, 280, 75, head=True)
    s.text(120, 120, "ρ_1,  u_1,  p_1", anchor="middle")
    s.text(320, 120, "ρ_2,  u_2,  p_2", anchor="middle")
    s.save(OUT / "shock-frame.svg")


def hugoniot():
    G = 5 / 3
    s = Svg(640, 420, "Shock adiabat and adiabats",
            "Logarithmic plot of the pressure ratio p_2/p_1 against the volume ratio V_2/V_1 for "
            "Gamma = 5/3. The adiabats p V^Gamma = const are straight blue lines. The shock "
            "adiabat, in black, touches the adiabat through the point (1, 1) at that point. For "
            "compressions, V_2/V_1 < 1, it rises above it towards a vertical asymptote at "
            "V_2/V_1 = (Gamma - 1)/(Gamma + 1) = 1/4, and a compressed state lies on a higher "
            "adiabat, so its entropy is larger. For expansions, V_2/V_1 > 1, the shock adiabat "
            "is dashed and lies below the adiabat through (1, 1), so the entropy would be "
            "smaller.", "hugoniot")
    from math import log10
    x0, y0, sx, sy = 90, 360, 270, 105  # pixels per decade
    X0, Y0 = -0.75, -1.4  # log10 of the lower-left corner

    def px(x, y):
        return (x0 + sx * (log10(x) - X0), y0 - sy * (log10(y) - Y0))

    def hug(x):
        return ((G + 1) - (G - 1) * x) / ((G + 1) * x - (G - 1))

    s.line(x0, y0, x0, 20, head=True)
    s.line(x0, y0, 620, y0, head=True)
    s.text(x0 - 12, 32, "p_2/p_1", anchor="end")
    s.text(612, y0 + 34, "V_2/V_1", anchor="end")
    xa = (G - 1) / (G + 1)
    s.line(px(xa, 1)[0], y0, px(xa, 1)[0], 30, color="#555", w=1.2, dash="3 4")
    s.line(px(xa, 1)[0], y0, px(xa, 1)[0], y0 + 6)
    s.text(px(xa, 1)[0], y0 + 26, "(Γ−1)/(Γ+1)", anchor="middle", size=17)
    s.line(px(1, 1)[0], y0, px(1, 1)[0], y0 + 6)
    s.text(px(1, 1)[0], y0 + 26, "1", anchor="middle", italic=False)
    s.line(x0 - 6, px(1, 1)[1], x0, px(1, 1)[1])
    s.text(x0 - 10, px(1, 1)[1] + 6, "1", anchor="end", italic=False)
    # adiabats: straight lines of slope -Gamma
    xb, xc = 0.4, 3.0
    yb = hug(xb)
    s.line(*px(0.19, 0.19 ** -G), *px(3.3, 3.3 ** -G), color=BLUE, w=2)
    s.line(*px(0.27, yb * (0.27 / xb) ** -G), *px(3.0, yb * (3.0 / xb) ** -G), color=BLUE, w=2)
    s.text(px(3.0, 1)[0], px(1, 0.3)[1], "pV^Γ = const", fill=BLUE)
    # shock adiabat
    s.poly([px(x, hug(x)) for x in [0.274 + 0.002 * i for i in range(0, 364)]], "#000", 2.4)
    xs = [1 + 0.01 * i for i in range(0, 237)]
    s.path("M " + " L ".join(f"{px(x, hug(x))[0]:.1f} {px(x, hug(x))[1]:.1f}" for x in xs),
           "#000", 2, dash="7 5")
    for x, y in ((1, 1), (xb, yb), (xc, hug(xc))):
        s.circle(*px(x, y), 4, fill="#000")
    # entropy arrows
    a, b, c = px(1, 1), px(xb, yb), px(xc, hug(xc))
    s.path(f"M {a[0] + 6:.1f} {a[1] - 8:.1f} C {a[0] + 40:.1f} {a[1] - 90:.1f} "
           f"{b[0] + 90:.1f} {b[1] - 40:.1f} {b[0] + 9:.1f} {b[1] - 4:.1f}", RED, 1.8, head=True)
    s.text(a[0] + 30, b[1] - 34, "entropy increases", fill=RED, italic=False, size=18)
    s.path(f"M {a[0] - 4:.1f} {a[1] + 9:.1f} C {a[0] + 10:.1f} {a[1] + 90:.1f} "
           f"{c[0] - 80:.1f} {c[1] + 40:.1f} {c[0] - 9:.1f} {c[1] + 3:.1f}", RED, 1.8, head=True)
    s.text(c[0] + 18, c[1] + 4, "entropy decreases", fill=RED, italic=False, size=18)
    s.save(OUT / "hugoniot.svg")


def evolutionary():
    s = Svg(740, 230, "Small perturbations of a shock",
            "A shock in its rest frame, with the gas flowing from left to right. A thin dashed "
            "vertical line marks the unperturbed shock; the perturbed shock, a thick wavy line, "
            "oscillates around it, and its displacement is marked eta. On the upstream side, on "
            "the left, two gray arrows point towards the shock: the sound waves moving at "
            "u_1 - c_s,1 and u_1 + c_s,1, which are both positive. On the downstream side, on "
            "the right, a gray arrow points towards the shock: the sound wave moving at "
            "u_2 - c_s,2, which is negative. Two blue arrows point away from the shock: the "
            "entropy and vorticity perturbations, moving at u_2, and the sound wave moving at "
            "u_2 + c_s,2.", "evolutionary")
    xs, amp, lam, y0 = 320, 12, 125, 205  # crest of the perturbed shock at y0
    s.line(xs, 20, xs, 215, color="#555", w=1.2, dash="6 4")
    s.poly([(xs + amp * math.cos(2 * math.pi * (y - y0) / lam), y) for y in range(20, 216)], "#000", 3.4)
    s.line(xs, y0, xs + amp, y0, w=1.2)
    s.text(xs + amp + 6, y0 + 6, "η")
    s.text(160, 30, "upstream", anchor="middle", italic=False)
    s.text(480, 30, "downstream", anchor="middle", italic=False)
    for y, lab in ((75, "u_1 − c_{s,1}"), (135, "u_1 + c_{s,1}")):
        s.line(170, y, 290, y, color="#777", w=2, head=True)
        s.text(230, y - 12, lab, anchor="middle", fill="#555")
    s.line(470, 75, 350, 75, color="#777", w=2, head=True)
    s.text(410, 63, "u_2 − c_{s,2}", anchor="middle", fill="#555")
    for y, lab, what in ((135, "u_2", "(entropy, vorticity)"), (185, "u_2 + c_{s,2}", "(sound)")):
        s.line(350, y, 470, y, color=BLUE, w=2, head=True)
        s.text(480, y + 6, lab, fill=BLUE)
        s.text(570, y + 6, what, fill=BLUE, italic=False)
    s.save(OUT / "evolutionary.svg")

def wavy_arrow(s, x1, x2, y, color, amp=3.5, waves=5):
    """Horizontal wavy arrow (a photon) from x1 to x2."""
    n = 80
    pts = [(x1 + (x2 - x1) * i / n, y + amp * math.sin(2 * math.pi * waves * i / n))
           for i in range(n + 1)]
    for i in range(n - 12, n + 1):
        pts[i] = (pts[i][0], y)
    s.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts), color, 1.6, head=True)


def viscous_profile():
    s = Svg(640, 250, "Structure of a viscous shock",
            "Two panels. Left: the velocity u as a function of x decreases smoothly from u_1 to "
            "u_2 over a width delta; a dotted line shows the corresponding discontinuity. Right: "
            "the pressure p increases smoothly from p_1 to p_2 over the same width.",
            "viscous-profile")
    d = 22  # half-width of the transition (pixels)
    for x0, top, bot, rising, lab1, lab2, name in ((40, 60, 170, False, "u_1", "u_2", "u"),
                                                    (360, 60, 170, True, "p_1", "p_2", "p")):
        xc = x0 + 120
        s.line(xc, 205, xc, 30, head=True)
        s.line(x0, 205, x0 + 250, 205, head=True)
        s.text(xc - 10, 40, name, anchor="end")
        s.text(x0 + 244, 228, "x", anchor="middle")
        lo, hi = (bot, top) if rising else (top, bot)
        pts = [(x0 + i, lo + (hi - lo) * (1 + math.tanh((x0 + i - xc) / d * 1.5)) / 2)
               for i in range(0, 231)]
        s.poly(pts, "#000", 2.2)
        s.path(f"M {x0} {lo} L {xc} {lo} L {xc} {hi} L {x0 + 230} {hi}", "#555", 1.2, dash="2 3")
        s.text(x0 - 4, lo + 6, lab1, anchor="end")
        s.text(x0 + 234, hi + 6, lab2)
        s.bracket(xc - d, 222, xc + d, 222, w=1.2)
        s.text(xc + d + 8, 228, "δ")
    s.save(OUT / "viscous-profile.svg")


def thick_shock():
    s = Svg(680, 240, "Structure of a radiatively thick shock",
            "A tube with the gas flowing from left to right. In the middle, a double blue line "
            "is the viscous shock. Wavy arrows labelled gamma show photons moving from the "
            "viscous shock upstream, to the left, into the precursor, which is bounded by a red "
            "line on the left. Downstream of the viscous shock, a relaxation layer ends at a "
            "second red line. Upstream of the precursor the gas has rho_1, u_1 and h_1; "
            "downstream of the relaxation layer it has rho_2, u_2 and h_2.", "thick-shock")
    s.line(20, 50, 660, 50)
    s.line(20, 200, 660, 200)
    s.line(150, 50, 150, 200, color=RED, w=1.8)
    s.line(530, 50, 530, 200, color=RED, w=1.8)
    s.line(335, 50, 335, 200, color=BLUE, w=2)
    s.line(343, 50, 343, 200, color=BLUE, w=2)
    s.text(339, 36, "viscous shock", anchor="middle", fill=BLUE, italic=False)
    s.text(242, 224, "precursor", anchor="middle", fill=RED, italic=False)
    s.text(436, 224, "relaxation layer", anchor="middle", fill=RED, italic=False)
    for y in (90, 165):
        wavy_arrow(s, 325, 250, y, "#000")
        s.text(287, y - 14, "γ", anchor="middle")
    s.line(40, 128, 120, 128, head=True)
    s.text(80, 160, "ρ_1, u_1, h_1", anchor="middle")
    s.text(595, 160, "ρ_2, u_2, h_2", anchor="middle")
    s.save(OUT / "thick-shock.svg")


def thin_shock():
    s = Svg(660, 420, "Structure of an optically thin radiative shock",
            "Top: the gas flows from left to right. Region 1 is cold gas moving rapidly, with "
            "rho_1, p_1, T_1 and u_1. A double line, the viscous shock, separates it from "
            "region 2, hot gas moving slowly, with rho_2, p_2, T_2 and u_2. The gas then cools "
            "in a radiative relaxation layer, which ends in region 3, cold gas moving very "
            "slowly, with rho_3, p_3, T_3 and u_3. Below, two profiles aligned with the "
            "regions: the density jumps from rho_1 to rho_2 at the shock and then keeps "
            "increasing to rho_3 in the relaxation layer; the temperature jumps from T_1 to T_2 "
            "at the shock and then decreases to T_3, close to T_1.", "thin-shock")
    xs, xe, x0, x1 = 210, 470, 30, 640
    s.line(xs - 4, 20, xs - 4, 150, w=1.8)
    s.line(xs + 4, 20, xs + 4, 150, w=1.8)
    s.line(xe, 20, xe, 150, w=1.8)
    s.text(xs - 10, 34, "1", anchor="end", italic=False)
    s.text(xs + 10, 34, "2", italic=False)
    s.text(xe + 8, 34, "3", italic=False)
    for xc, l1, l2, vars_ in (((x0 + xs) / 2, "cold gas,", "moving fast", "ρ_1, p_1, T_1, u_1"),
                              ((xs + xe) / 2, "hot gas, cooling,", "moving slowly", "ρ_2, p_2, T_2, u_2"),
                              ((xe + x1) / 2, "cold gas, moving", "very slowly", "ρ_3, p_3, T_3, u_3")):
        s.text(xc, 62, l1, anchor="middle", italic=False, size=17)
        s.text(xc, 84, l2, anchor="middle", italic=False, size=17)
        s.text(xc, 122, vars_, anchor="middle", size=18)
    s.text((xs + xe) / 2, 146, "relaxation layer", anchor="middle", fill=RED, italic=False, size=17)
    ell = 55

    def profile(ybase, h, f, color, labels, sym):
        s.line(x0, ybase, x1, ybase, color="#999", w=1)
        pts = [(x, ybase - h * f(x)) for x in range(x0, x1 + 1)]
        s.poly(pts, color, 2.2)
        for (x, v), lab in zip(labels, ("_1", "_2", "_3")):
            s.text(x, ybase - h * v - 8, sym + lab, anchor="middle", fill=color, size=18)

    def rho(x):
        if x < xs:
            return 0.12
        return 1.0 - (1.0 - 0.45) * math.exp(-(x - xs) / ell)

    def temp(x):
        if x < xs:
            return 0.12
        return 0.16 + (1.0 - 0.16) * math.exp(-(x - xs) / ell)

    profile(275, 90, rho, "#000", ((120, 0.12), (xs + 30, 0.64), (560, 1.0)), "ρ")
    profile(400, 90, temp, RED, ((120, 0.12), (xs + 36, 0.9), (560, 0.16)), "T")
    for y in (180, 305):
        s.line(xs, y, xs, y + 98, color="#999", w=1, dash="3 3")
        s.line(xe, y, xe, y + 98, color="#999", w=1, dash="3 3")
    s.save(OUT / "thin-shock.svg")


def colliding_clouds():
    s = Svg(470, 200, "Idealized geometry of the colliding-cloud problem",
            "One-dimensional sketch along the z axis. A thick blue line on the left marks the "
            "edge of the shocked layer and a thin blue line marks the shock, which moves to the "
            "right at speed s. Between them the shocked material has density rho_2, velocity "
            "zero and temperature T_2. To the right of the shock is the unshocked cloud, with "
            "density rho_1, velocity v_1 and temperature T_1, ending at radius R_cloud.", "geometry")
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
    s.text(378, 80, "R_{cloud}")
    s.text(404, 122, "z")
    s.text(195, 178, "shocked material", anchor="middle", italic=False)
    s.text(322, 178, "cloud", anchor="middle", italic=False)
    s.save(OUT / "colliding-clouds-geometry.svg")



if __name__ == "__main__":
    piston()
    weak_solution()
    shock_frame()
    hugoniot()
    evolutionary()
    viscous_profile()
    thick_shock()
    thin_shock()
    colliding_clouds()
    print("wrote", OUT)
