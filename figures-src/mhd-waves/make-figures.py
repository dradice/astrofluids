#!/usr/bin/env python3
"""Figures of Chapter 26 (MHD waves), redrawn from the 2025 TeXmacs drawings.

Usage: python3 figures-src/mhd-waves/make-figures.py   (from the notes/ directory)
The Friedrichs diagrams are computed from the dispersion relation with c_s = 1, v_A = 2
(left) and c_s = 2, v_A = 1 (right).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "mhd-waves"


def vec(s, ox, oy, deg, length, color="#000", w=3.0):
    """Arrow from (ox, oy) at `deg` degrees above the +z (right) direction."""
    a = math.radians(deg)
    x, y = ox + length * math.cos(a), oy - length * math.sin(a)
    s.line(ox, oy, x, y, color, w, head=True)
    return x, y


def triad(s, ox, oy, up=165, right=170, left=45, down=45, ylen=115):
    """Axes: x up, z right, y towards the lower left (out of the page)."""
    s.line(ox, oy - up, ox, oy + down, w=1.5)
    s.line(ox - left, oy, ox + right, oy, w=1.5)
    s.line(ox, oy, ox - 0.5 * ylen, oy + 0.75 * ylen, w=1.5)
    s.text(ox + 12, oy - up + 12, "x", size=20)
    s.text(ox + right + 4, oy + 22, "z", size=20)
    s.text(ox - 0.5 * ylen - 6, oy + 0.75 * ylen + 20, "y", size=20, anchor="end")


def alfven_geometry(s, ox, oy):
    triad(s, ox, oy)
    vec(s, ox, oy, 0, 145, w=3.0)
    s.text(ox + 105, oy - 22, "B_0", bold=True, size=22)
    vec(s, ox, oy, 45, 95)
    s.text(ox + 78, oy - 78, "k", bold=True, size=22)
    vec(s, ox, oy, 135, 95)
    s.text(ox - 118, oy - 85, "k̂_⊥", bold=True, size=22)
    # right-angle mark between k and k-perp
    s.poly([(ox - 12, oy - 12), (ox, oy - 24), (ox + 12, oy - 12)], w=1.2)
    s.path(f"M {ox + 38} {oy} A 38 38 0 0 0 {ox + 27} {oy - 27}", w=1.4)
    s.text(ox + 62, oy - 16, "θ", size=20)


def alfven():
    s = Svg(360, 340, "Geometry of the Alfvén wave",
            "Axes: x up, z to the right, y towards the lower left. The background field B0 "
            "lies along z. The wave vector k lies in the xz-plane at angle theta from z; "
            "the unit vector k-perp is perpendicular to k in the same plane. The displacement "
            "xi points along y, perpendicular to both k and B0.", "alf")
    ox, oy = 150, 190
    alfven_geometry(s, ox, oy)
    x, y = vec(s, ox, oy, 233.13, 80)
    s.text(x - 8, y + 6, "ξ", bold=True, size=24, anchor="end")
    s.save(OUT / "waves-alfven-geometry.svg")


def magnetosonic():
    s = Svg(360, 340, "Geometry of the magnetosonic wave",
            "Same axes as for the Alfvén wave: x up, z to the right, y towards the lower "
            "left, B0 along z, k in the xz-plane at angle theta from z and k-perp "
            "perpendicular to it. The displacement xi now lies in the xz-plane, pointing "
            "slightly below the z axis.", "ms")
    ox, oy = 150, 190
    alfven_geometry(s, ox, oy)
    x, y = vec(s, ox, oy, -18, 110)
    s.text(x + 4, y + 22, "ξ", bold=True, size=24)
    s.save(OUT / "waves-magnetosonic-geometry.svg")


def parallel():
    s = Svg(720, 330, "Polarizations of MHD waves propagating along the field",
            "Two panels with axes x up, z right and y to the lower left; B0 and k both lie "
            "along z. Left, for v_A > c_s: the fast mode is polarized along x, the slow mode "
            "along z and the Alfvén mode along y. Right, for v_A < c_s the fast and slow modes "
            "exchange polarizations: the slow mode is along x and the fast mode along z. "
            "Below each panel are the corresponding frequencies.", "par")
    for ox, label, up, down, eq in (
            (130, "v_A > c_s", "f", "s", ("ω_s^2 = c_s^2 k^2,", "ω_f^2 = ω_A^2 = v_A^2 k^2.")),
            (490, "v_A < c_s", "s", "f", ("ω_f^2 = c_s^2 k^2,", "ω_s^2 = ω_A^2 = v_A^2 k^2."))):
        oy = 175
        s.text(ox + 55, 28, label, anchor="middle", size=20)
        triad(s, ox, oy, up=130, right=190, left=45, down=45, ylen=92)
        vec(s, ox, oy, 90, 85)
        s.text(ox + 12, oy - 82, f"ξ_{up}", bold=True, size=22)
        vec(s, ox, oy, 0, 90)
        s.text(ox + 62, oy - 12, "k", bold=True, size=22)
        s.text(ox + 118, oy - 12, "B_0", bold=True, size=22)
        s.line(ox + 90, oy, ox + 175, oy, w=3.0, head=True)
        s.text(ox + 62, oy + 26, f"ξ_{down}", bold=True, size=22)
        x, y = vec(s, ox, oy, 233.13, 62)
        s.text(x - 8, y - 2, "ξ_A", bold=True, size=22, anchor="end")
        s.text(ox + 55, 282, eq[0], anchor="middle", size=19)
        s.text(ox + 55, 308, eq[1], anchor="middle", size=19)
    s.save(OUT / "waves-parallel-polarization.svg")


def limits():
    s = Svg(720, 300, "Slow and fast magnetosonic waves for weak and strong fields",
            "Two panels with axes x up, z right and y to the lower left, B0 along z and k in "
            "the xz-plane at 45 degrees from z. Left, weak field (c_s much larger than v_A): "
            "the fast displacement lies close to k, slightly steeper, and the slow displacement "
            "points up and to the left, nearly perpendicular to k. Right, strong field "
            "(v_A much larger than c_s): the fast displacement is close to the x axis, almost "
            "perpendicular to B0, and the slow displacement is nearly parallel to B0. In both "
            "panels the Alfvén displacement points along y.", "lim")
    for ox, label, fast, slow in ((130, "c_s ≫ v_A", 62, 150), (490, "v_A ≫ c_s", 80, -9)):
        oy = 175
        s.text(ox + 55, 28, label, anchor="middle", size=20)
        triad(s, ox, oy, up=135, right=190, left=45, down=45, ylen=92)
        vec(s, ox, oy, 0, 140, w=3.0)
        s.text(ox + 118, oy - 14, "B_0", bold=True, size=22)
        x, y = vec(s, ox, oy, 45, 70)
        s.text(x + 10, y + 10, "k", bold=True, size=22)
        x, y = vec(s, ox, oy, fast, 110)
        s.text(x + 10, y + 4, "ξ_f", bold=True, size=22)
        x, y = vec(s, ox, oy, slow, 85 if slow > 0 else 85)
        s.text(x + (-10 if slow > 90 else 8), y + (-4 if slow > 90 else 26), "ξ_s", bold=True, size=22,
               anchor="end" if slow > 90 else "start")
        x, y = vec(s, ox, oy, 233.13, 62)
        s.text(x + 4, y + 22, "ξ_A", bold=True, size=22, anchor="start")
    s.save(OUT / "waves-weak-strong-field.svg")


def lagrangian():
    s = Svg(620, 440, "Lagrangian displacement of a fluid element",
            "A small square fluid element at position x, where a quantity has the value q, is "
            "displaced by the vector xi, shown as a curved arrow, to the position x plus xi, "
            "where the quantity has the value q plus delta q. The Eulerian perturbation at x "
            "is q'(x) = delta q minus xi dot nabla q.", "lag")
    s.rect(18, 300, 125, 110, stroke="#000", sw=2)
    s.text(80, 365, "x", bold=True, anchor="middle", size=22)
    s.text(158, 405, "q", size=22)
    s.rect(300, 18, 125, 110, stroke="#000", sw=2)
    s.text(362, 88, "x + ξ", bold=True, anchor="middle", size=22)
    s.text(450, 88, "q + δq", size=22)
    s.path("M 75 280 C 105 185 190 110 292 82", w=2.6, head=True)
    s.text(225, 200, "ξ", bold=True, size=24)
    s.text(238, 360, "q′(x) = δq − ξ·∇q", size=22)
    s.save(OUT / "waves-lagrangian-displacement.svg")


def shock():
    s = Svg(480, 290, "Isothermal shock with perpendicular magnetic field",
            "A vertical line marks the shock. The gas ahead of it (right) has density rho1, "
            "velocity u1 and field B1; the gas behind it (left) has density rho2, velocity u2 "
            "and field B2. The magnetic field points out of the page (circled dots) on both "
            "sides, and the flow u (blue arrow) moves leftwards, through the shock. The gas "
            "is isothermal, p = c_iso^2 rho.", "shock")
    s.line(262, 30, 262, 255, w=3.0)
    s.text(40, 52, "p = c_{iso}^2 ρ", size=22)
    for x, y in ((185, 105), (312, 105), (185, 220), (312, 220)):
        s.out_of_plane(x, y, GREEN, r=12)
    s.text(332, 138, "B", bold=True, fill=GREEN, size=26)
    s.line(300, 160, 215, 160, BLUE, 1.7, head=True)
    s.text(150, 172, "u", bold=True, fill=BLUE, size=24)
    s.text(18, 278, "ρ_2, u_2, B_2", size=22)
    s.text(300, 278, "ρ_1, u_1, B_1", size=22)
    s.save(OUT / "waves-isothermal-shock.svg")


def friedrichs():
    import matplotlib
    matplotlib.use("svg")
    import matplotlib.pyplot as plt
    import numpy as np
    plt.rcParams.update({"svg.fonttype": "none", "font.size": 17, "xtick.labelsize": 15, "ytick.labelsize": 15,
                         "font.family": ["Latin Modern Math", "STIX Two Math", "DejaVu Serif"]})
    th = np.linspace(0, 2 * np.pi, 721)
    fig, axs = plt.subplots(1, 2, subplot_kw={"projection": "polar"}, figsize=(8.0, 4.7))
    for ax, (cs, va, title) in zip(axs, ((1.0, 2.0, r"$v_A > c_s$"), (2.0, 1.0, r"$v_A < c_s$"))):
        disc = np.sqrt((va**2 - cs**2) ** 2 + 4 * cs**2 * va**2 * np.sin(th) ** 2)
        fast = np.sqrt(0.5 * (va**2 + cs**2 + disc))
        slow = np.sqrt(0.5 * (va**2 + cs**2 - disc))
        alf = va * np.abs(np.cos(th))
        ax.plot(th, slow, color="#1f4fbf", ls="-", lw=2, label="Slow wave")
        ax.plot(th, alf, color="#c55a00", ls="--", lw=2, label="Alfvén wave")
        ax.plot(th, fast, color="#0b6e0b", ls=":", lw=2.6, label="Fast wave")
        ax.set_rlabel_position(60)
        ax.set_ylim(0, 2.4)
        ax.set_yticks([0.5, 1.0, 1.5, 2.0])
        ax.grid(True, color="#999999", lw=0.8)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, fontsize=16, frameon=False)
    fig.tight_layout(rect=(0, 0.08, 1, 0.89))
    fig.canvas.draw()
    path = OUT / "waves-friedrichs-diagrams.svg"
    fig.savefig(path)
    # panel titles and accessible name, written as real text with sub-scripts
    w_pt, h_pt = fig.get_size_inches() * 72
    lab = Svg(1, 1, "", "", "x")
    for ax, t in zip(axs, ("v_A > c_s", "v_A < c_s")):
        bb = ax.get_position()
        lab.text(f"{(bb.x0 + bb.x1) / 2 * w_pt:.1f}", 20, t, anchor="middle", size=19)
    desc = ("Two polar plots of the phase speeds of the slow (solid), Alfvén (dashed) and fast "
            "(dotted) modes as a function of the angle from the magnetic field (0 degrees to the "
            "right). Left, v_A = 2 c_s: the fast mode is almost circular with radius about 2.2, "
            "the Alfvén mode is a pair of lobes reaching 2 along the field and the slow mode "
            "a pair of smaller lobes reaching 1. Right, v_A = c_s / 2: the fast mode is again "
            "almost circular, with radius about 2.2, and the Alfvén and slow modes are two nearly "
            "identical lobes reaching 1 along the field.")
    txt = path.read_text()
    txt = txt.replace("</svg>", '<g font-family="%s">%s</g>\n</svg>' % (FONT, "".join(lab.body)))
    k = txt.index(">", txt.index("<svg")) + 1
    txt = (txt[:k] + '\n<title id="fr-t">Friedrichs diagrams for ideal MHD</title>'
           '<desc id="fr-d">%s</desc>' % desc + txt[k:])
    txt = txt.replace("<svg ", '<svg role="img" aria-labelledby="fr-t fr-d" ', 1)
    txt = txt.replace(f"{w_pt:.1f}pt", f"{w_pt:.1f}").replace(f"{h_pt:.1f}pt", f"{h_pt:.1f}")
    path.write_text(txt)


if __name__ == "__main__":
    alfven()
    magnetosonic()
    parallel()
    limits()
    lagrangian()
    shock()
    friedrichs()
