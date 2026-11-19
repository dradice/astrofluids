#!/usr/bin/env python3
"""Figures of the fluid-instabilities chapter: displaced fluid element, convection cycle, vortex sheet,
and the eigenvalue sketches (from the instructor's handwritten notes and the 2023 slides), plus the
Rayleigh-Taylor worksheet figure (rotated fluid cylinder), redrawn from the 2025 drawing.

Usage: python3 figures-src/fluid-instabilities/make-figures.py   (from the notes/ directory)
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "fluid-instabilities"

HEAVY = "#b3b3b3"
LIGHT = "#ececec"


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def sector(cx, cy, r1, r2, d0, d1):
    """Annular sector from angle d0 to d1 (degrees, counterclockwise on the screen)."""
    x0, y0 = pt(cx, cy, r2, d0)
    x1, y1 = pt(cx, cy, r2, d1)
    x2, y2 = pt(cx, cy, r1, d1)
    x3, y3 = pt(cx, cy, r1, d0)
    large = 1 if (d1 - d0) % 360 > 180 else 0
    return (f"M {x0:.1f} {y0:.1f} A {r2} {r2} 0 {large} 0 {x1:.1f} {y1:.1f} "
            f"L {x2:.1f} {y2:.1f} A {r1} {r1} 0 {large} 1 {x3:.1f} {y3:.1f} Z")


def ring():
    W, H = 520, 400
    cx, cy, r, R = 260, 200, 95, 125
    th = 30
    s = Svg(W, H, "Fluid cylinder rotated across a heavy-over-light interface",
            "A heavy fluid of density rho_2 lies on top of a lighter fluid of density rho_1 along a "
            "horizontal interface. A circular region of radius r is split by the interface into a "
            "heavy upper half and a light lower half. Around it, a thin ring of fluid has been "
            "rotated counterclockwise by an angle theta: heavy fluid has moved down on the left "
            "and light fluid has moved up on the right.", "rtring")
    s.rect(20, 20, 480, 180, fill=HEAVY, stroke="none", sw=0)
    s.rect(20, 200, 480, 180, fill=LIGHT, stroke="none", sw=0)
    # ring: heavy part from theta to 180+theta, light part otherwise
    s.path(sector(cx, cy, r, R, th, 180 + th), fill=HEAVY)
    s.path(sector(cx, cy, r, R, 180 + th, 360 + th), fill=LIGHT)
    # inner disc: heavy upper half, light lower half
    s.path(f"M {cx - r} {cy} A {r} {r} 0 0 1 {cx + r} {cy} Z", fill=HEAVY)
    s.path(f"M {cx - r} {cy} A {r} {r} 0 0 0 {cx + r} {cy} Z", fill=LIGHT)
    # interface outside the ring and the horizontal radius
    s.line(20, cy, cx - R, cy)
    s.line(cx + R, cy, 500, cy)
    s.line(cx - r, cy, cx + r, cy)
    # rotated radius and angle
    x, y = pt(cx, cy, R, th)
    s.line(cx, cy, x, y, w=2.2)
    a0 = pt(cx, cy, 55, 0)
    a1 = pt(cx, cy, 55, th)
    s.path(f"M {a0[0]:.1f} {a0[1]:.1f} A 55 55 0 0 0 {a1[0]:.1f} {a1[1]:.1f}")
    s.text(cx + 70, cy - 18, "θ", italic=True)
    s.text(cx - 40, cy - 12, "r", anchor="middle")
    s.text(40, cy - 14, "ρ_2")
    s.text(40, cy + 30, "ρ_1")
    s.save(OUT / "rotated-cylinder.svg")


def blob():
    W, H = 560, 380
    s = Svg(W, H, "A fluid element displaced upwards in a stratified medium",
            "A small circle at the bottom, with density rho and pressure p, is displaced upwards by "
            "a distance delta z, along a curved arrow, to a larger circle with density rho star and "
            "pressure p star. Next to the upper circle, the background has density rho(z + delta z) "
            "and pressure p(z + delta z). An arrow on the right points down and is labelled g.", "blob")
    cx = 200
    s.circle(cx, 300, 26)
    s.text(cx + 34, 325, "ρ, p")
    s.circle(cx, 110, 52)
    s.text(cx, 118, "ρ^{*}, p^{*}", anchor="middle")
    s.line(cx, 262, cx, 178, head=True)
    s.text(cx + 12, 228, "δz", anchor="start")
    s.path(f"M {cx - 30} 290 C {cx - 95} 250, {cx - 95} 170, {cx - 55} 140", head=True)
    s.text(300, 70, "ρ(z + δz)")
    s.text(300, 102, "p(z + δz)")
    s.text(300, 150, "background", italic=False, size=17)
    s.line(500, 150, 500, 250, head=True, w=2)
    s.text(512, 210, "g", anchor="start")
    s.save(OUT / "displaced-element.svg")


def cycle():
    W, H = 560, 360
    s = Svg(W, H, "Schematic convection cycle",
            "Four points at the corners of a rectangle, joined by arrows that go around clockwise. "
            "On the left side, a hot fluid element rises adiabatically. At the top, it gives heat to "
            "its surroundings and moves to the right. On the right side, the cool element sinks "
            "adiabatically. At the bottom, it takes heat from its surroundings and moves back to the left.",
            "cycle")
    x0, x1, y0, y1 = 170, 390, 90, 270
    for x, y in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        s.circle(x, y, 8, fill="#000")
    s.path(f"M {x0} {y1 - 14} C {x0 - 50} {y1 - 60}, {x0 - 50} {y0 + 60}, {x0} {y0 + 14}", head=True)
    s.path(f"M {x0 + 14} {y0} C {x0 + 80} {y0 - 40}, {x1 - 80} {y0 - 40}, {x1 - 14} {y0}", head=True)
    s.path(f"M {x1} {y0 + 14} C {x1 + 50} {y0 + 60}, {x1 + 50} {y1 - 60}, {x1} {y1 - 14}", head=True)
    s.path(f"M {x1 - 14} {y1} C {x1 - 80} {y1 + 40}, {x0 + 80} {y1 + 40}, {x0 + 14} {y1}", head=True)
    s.text(x0 - 48, (y0 + y1) / 2 + 6, "adiabatic", anchor="end", italic=False, size=18)
    s.text(x0 - 48, (y0 + y1) / 2 + 28, "rise", anchor="end", italic=False, size=18)
    s.text(x1 + 48, (y0 + y1) / 2 + 6, "adiabatic", anchor="start", italic=False, size=18)
    s.text(x1 + 48, (y0 + y1) / 2 + 28, "sinking", anchor="start", italic=False, size=18)
    s.text(W / 2, 36, "hot element heats its surroundings", anchor="middle", italic=False, size=18)
    s.text(W / 2, 336, "cool element takes heat from its surroundings", anchor="middle", italic=False, size=18)
    s.save(OUT / "convection-cycle.svg")


def sheet():
    W, H = 560, 300
    s = Svg(W, H, "Perturbed vortex sheet",
            "A horizontal sinusoidal curve separates two regions. Above it the fluid moves to the right "
            "with velocity V_2, below it with velocity V_1. A vertical arrow from the unperturbed "
            "position of the sheet to the crest of the curve is labelled xi, the displacement. Axes in "
            "the corner: x points up and y to the right.", "sheet")
    import math as m
    pts = [(40 + i * 3.6, 150 - 45 * m.sin(2 * m.pi * i / 100 * 1.25)) for i in range(101)]
    s.poly(pts, w=2.2)
    s.line(40, 150, 400, 150, dash="5 5", w=1.2)
    xc = 40 + 20 * 3.6
    s.line(xc, 150, xc, 108, head=True)
    s.text(xc + 8, 136, "ξ")
    s.line(180, 50, 280, 50, head=True, color=BLUE, w=2)
    s.text(290, 57, "V_2", fill=BLUE)
    s.line(180, 250, 260, 250, head=True, color=BLUE, w=2)
    s.text(270, 257, "V_1", fill=BLUE)
    ox, oy = 480, 200
    s.line(ox, oy, ox, oy - 60, head=True)
    s.line(ox, oy, ox + 60, oy, head=True)
    s.text(ox - 8, oy - 66, "x", anchor="end")
    s.text(ox + 62, oy + 24, "y", anchor="end")
    s.save(OUT / "vortex-sheet.svg")


def eigen():
    W, H = 900, 380
    s = Svg(W, H, "Sketch of the eigenfrequencies in the complex plane",
            "Two panels, each with the real part of omega on the horizontal axis and the imaginary part "
            "on the vertical axis. Left panel: six crosses below the horizontal axis (stable modes), "
            "each with an arrow pointing upwards; as the Reynolds number increases, they cross the axis "
            "into the upper half plane (unstable modes). Right panel: dots for the modes of a shear "
            "layer with different wave numbers. Starting from the origin, the dots rise along a straight "
            "line, reach a maximum, and then bend down, crossing the axis: modes with large wave numbers "
            "are damped by viscosity. Arrows show the dots moving upwards as the Reynolds number increases.",
            "eigen")
    # left panel
    ox, oy = 210, 190
    s.line(40, oy, 400, oy, head=True)
    s.line(ox, 340, ox, 40, head=True)
    s.text(400, oy + 30, "ω_r", anchor="end")
    s.text(ox + 10, 52, "ω_i")
    for x, y in ((80, 260), (130, 250), (165, 265), (250, 255), (300, 262), (345, 248)):
        s.text(x, y + 7, "×", anchor="middle", italic=False, size=22)
        s.path(f"M {x} {y - 10} C {x + 8} {y - 40}, {x - 8} {y - 70}, {x + 4} {y - 105}", head=True, color=BLUE)
    s.text(270, 100, "unstable modes", anchor="start", italic=False, size=18)
    s.text(250, 315, "stable modes", anchor="start", italic=False, size=18)
    s.text(52, 66, "Re increasing", anchor="start", italic=False, size=18, fill=BLUE)
    # right panel
    ox, oy = 520, 250
    s.line(480, oy, 880, oy, head=True)
    s.line(ox, 350, ox, 40, head=True)
    s.text(880, oy + 30, "ω_r", anchor="end")
    s.text(ox + 10, 52, "ω_i")
    # omega_r ~ k and omega_i ~ k (1 - k / k_c): growth at long wavelengths, viscous damping at short ones
    dots = [(ox + 24 * k, oy - 36 * k * (1 - k / 11)) for k in range(0, 14)]
    for x, y in dots:
        s.circle(x, y, 4, fill="#000", stroke="none")
    for x, y in dots[7:]:
        s.line(x, y - 8, x, y - 40, head=True, color=BLUE)
    s.text(590, 330, "damped by viscosity", anchor="start", italic=False, size=18)
    s.text(880, 80, "Re increasing", anchor="end", italic=False, size=18, fill=BLUE)
    s.save(OUT / "eigenvalues.svg")


if __name__ == "__main__":
    ring()
    blob()
    cycle()
    sheet()
    eigen()
