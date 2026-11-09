#!/usr/bin/env python3
"""Figures of Chapter 24 (Flux freezing), redrawn from the 2025 TeXmacs drawings.

Usage: python3 figures-src/flux-freezing/make-figures.py   (from the notes/ directory)
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "flux-freezing"


def tube():
    s = Svg(700, 340, "Deformation of a magnetic flux tube",
            "A flux tube with a magnetic field line along its axis is carried by the flow "
            "from a gently bent shape to a more strongly bent and narrower shape; the field "
            "line stays inside the tube.", "tube")
    for p, w0, w1 in (((( 50, 305), (95, 150), (150, 105), (290, 40)), 27, 27),
                      (((505, 300), (430, 215), (470, 95), (650, 40)), 27, 15)):
        c = bezier(*p)
        l, r = offset_edges(c, lambda t: w0 + (w1 - w0) * t)
        s.poly(l + r[::-1], closed=True, fill="#fff")
        x0, y0 = c[0]
        ang = math.degrees(math.atan2(c[1][1] - c[0][1], c[1][0] - c[0][0]))
        s.ellipse(x0, y0, w0 * 0.45, w0, rot=ang, fill="#fff")
        s.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in c[2:]), BLUE, 2.4, head=True)
    s.line(250, 212, 410, 212, head=True)
    s.text(272, 118, "B", bold=True, fill=BLUE, size=24)
    s.text(630, 118, "B", bold=True, fill=BLUE, size=24)
    s.save(OUT / "flux-tube.svg")


def compress_parallel():
    s = Svg(700, 190, "Compression of a flux tube along the field",
            "A horizontal flux tube of length l and cross-section A, with the magnetic field B "
            "pointing along its axis to the right. Arrows v at both ends point inwards: the "
            "tube is squeezed along the field and the cross-section does not change.", "para")
    cy, ry, rx = 80, 42, 21
    x1, x2 = 150, 530
    s.line(x1, cy - ry, x2, cy - ry)
    s.line(x1, cy + ry, x2, cy + ry)
    s.ellipse(x1, cy, rx, ry, fill="#fff")
    s.ellipse(x2, cy, rx, ry, fill="#fff")
    s.line(x1, cy, x2 - 70, cy, BLUE, 2.4, head=True)
    s.text(x2 - 56, cy + 8, "B", bold=True, fill=BLUE, size=24)
    s.text(x1 + 2, cy + 35, "A")
    s.text((x1 + x2) / 2, 165, "ℓ", anchor="middle")
    s.line(25, cy, 100, cy, w=2, head=True)
    s.line(675, cy, 600, cy, w=2, head=True)
    s.text(62, 38, "v", bold=True, anchor="middle")
    s.text(640, 38, "v", bold=True, anchor="middle")
    s.save(OUT / "flux-compression-parallel.svg")


def resistive():
    s = Svg(700, 520, "Resistive smoothing of a magnetic field line",
            "Three snapshots of one field line B that points upwards. At first it is bent and "
            "has small-scale wiggles; later the wiggles are gone and only the large-scale bend "
            "remains; finally the line is straight. Arrows labelled t between the snapshots "
            "show the passage of time.", "resist")

    def base(y, x0):
        u = (500 - y) / 470.0
        return x0 + 60 * math.sin(2.2 * math.pi * u) * (1 - 0.5 * u) - 20 * u

    def curve(x0, wig, flat=False):
        pts = []
        for i in range(0, 471, 2):
            y = 500 - i
            x = x0 if flat else base(y, x0)
            if wig:
                x += 5 * math.sin(i / 7.0)
            pts.append((x, y))
        return pts

    s.poly(curve(80, True), w=3.2, head=True)
    s.poly(curve(330, False), w=2.6, head=True)
    s.poly([(610, 500), (610, 30)], w=2.6, head=True)
    for x in (120, 380, 650):
        s.text(x, 100, "B", bold=True, size=24)
    s.line(175, 275, 265, 275, w=1.5, head=True)
    s.line(450, 275, 550, 275, w=1.5, head=True)
    s.text(220, 260, "t", anchor="middle", size=22)
    s.text(500, 260, "t", anchor="middle", size=22)
    s.save(OUT / "flux-resistive-smoothing.svg")


def ambipolar():
    s = Svg(560, 670, "Ambipolar diffusion",
            "A roughly circular region of neutral gas, drawn as a wavy circle, contains a few "
            "ions (dots). Two magnetic field lines labelled B enter from the bottom and leave "
            "at the top; they pass through the ion region, bowing inwards, and are tied to the "
            "ions, while the neutrals can move across them.", "ambi")
    cx, cy, rx, ry = 276, 370, 256, 226
    pts = []
    for i in range(0, 721):
        th = math.radians(i / 2.0)
        k = 1 + 0.03 * math.sin(60 * th)
        pts.append((cx + rx * k * math.cos(th), cy - ry * k * math.sin(th)))
    s.poly(pts, w=1.6, closed=True)
    s.path("M 22 566 C 80 530 135 470 152 385 C 160 300 130 190 78 98", BLUE, 3.2, head=True)
    s.path("M 444 560 C 408 520 354 440 358 345 C 362 270 420 185 460 112", BLUE, 3.2, head=True)
    for x, y in ((168, 227), (284, 227), (152, 345), (212, 388), (300, 373), (124, 417),
                 (182, 505), (358, 344), (416, 446), (358, 534), (432, 227)):
        s.circle(x, y, 6.5, fill=RED, stroke=RED, w=1)
    s.text(256, 440, "ions", anchor="middle", italic=False, fill=RED, size=22)
    s.text(552, 656, "neutrals", anchor="end", italic=False, size=22)
    s.text(116, 44, "B", bold=True, fill=BLUE, size=24)
    s.text(452, 56, "B", bold=True, fill=BLUE, size=24)
    s.save(OUT / "flux-ambipolar-diffusion.svg")


def toy():
    s = Svg(700, 375, "Toy model of the Io-Jupiter interaction",
            "Two thick horizontal walls at y = plus and minus D, between which a conductor of "
            "half-width d (the region between the two blue lines) moves to the right with "
            "velocity v. A magnetic field line B0 comes in from above, anchored in the walls, "
            "and is dragged by the conductor into a bent shape extending a distance L in the "
            "x direction. A current j points out of the page inside the conductor.", "toy")
    s.line(180, 72, 615, 72, w=3.2)
    s.line(180, 290, 615, 290, w=3.2)
    s.line(180, 137, 615, 137, BLUE, 3.2)
    s.line(180, 224, 615, 224, BLUE, 3.2)
    s.bracket(147, 72, 147, 290)
    s.text(100, 190, "2D", anchor="middle", fill=BLUE, size=22)
    s.line(268, 224, 268, 137, w=1.5, head=True, tail=True)
    s.text(228, 188, "2d", anchor="middle", fill=BLUE, size=22)
    s.out_of_plane(310, 181, GREEN, r=15)
    s.text(326, 250, "j", bold=True, fill=TEAL, size=24)
    s.line(360, 181, 515, 181, BLUE, 1.5)
    for x in (360, 515):
        s.line(x, 173, x, 189, BLUE, 1.5)
    s.text(437, 218, "L", anchor="middle", fill=BLUE, size=22)
    s.line(353, 72, 353, 20, w=1.6, head=True)
    s.line(398, 72, 398, 20, w=1.6, head=True)
    s.text(420, 36, "B_0", bold=True, size=24)
    s.path("M 353 72 L 480 142 Q 545 181 480 220 L 353 290 L 353 345", w=1.6)
    s.path("M 398 72 L 500 130 Q 553 165 548 181 Q 545 200 500 224 L 398 290 L 398 345", w=1.6)
    s.line(592, 181, 655, 181, BLUE, 1.7, head=True)
    s.text(672, 205, "v", bold=True, fill=BLUE, size=24, anchor="middle")
    s.line(48, 355, 48, 270, w=1.5)
    s.line(38, 322, 128, 322, w=1.5)
    s.text(18, 290, "y", size=22)
    s.text(110, 350, "x", size=22)
    s.save(OUT / "flux-toy-model.svg")


def dipole():
    s = Svg(460, 460, "Dipolar magnetic field of a sphere",
            "Field lines of a dipole around a sphere with north (N) and south (S) poles on the "
            "vertical axis. Outside the sphere the lines leave at S, loop around the equator "
            "and enter at N; arrows show that direction.", "dipole")
    R, cx, cy, half = 36, 230, 230, 225
    for L in (1.6, 2.4, 3.5, 4.8, 6.1):
        for side in (1, -1):
            th0 = math.asin(1 / math.sqrt(L))
            n = 400
            pts = [(cx + side * R * L * math.sin(t) ** 3, cy - R * L * math.sin(t) ** 2 * math.cos(t))
                   for t in [math.pi - th0 - (math.pi - 2 * th0) * i / n for i in range(n + 1)]]
            pts = [(x, y) for x, y in pts if abs(x - cx) < half and abs(y - cy) < half]
            if len(pts) < 10:
                continue
            s.poly(pts, w=1.3)
            for frac in (0.3, 0.7):
                i = int(frac * (len(pts) - 2))
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                s.line(x0, y0, x0 + 3 * (x1 - x0) / math.hypot(x1 - x0, y1 - y0),
                       y0 + 3 * (y1 - y0) / math.hypot(x1 - x0, y1 - y0), w=1.3, head=True)
    s.line(cx, cy + R + 2, cx, cy + half, w=1.3)
    s.line(cx, cy - half, cx, cy - R - 2, w=1.3)
    for dy in (60, 140):
        s.line(cx, cy - R - dy - 6, cx, cy - R - dy, w=1.3, head=True)
        s.line(cx, cy + R + dy, cx, cy + R + dy + 6, w=1.3, head=True)
    s.circle(cx, cy, R, fill="#fff", stroke="#000", w=1.8)
    s.path(f"M {cx - R} {cy} A {R} {R * 0.22} 0 0 0 {cx + R} {cy}", w=1.2)
    s.text(cx, cy - 12, "N", anchor="middle", italic=False, size=20)
    s.text(cx, cy + 32, "S", anchor="middle", italic=False, size=20)
    s.save(OUT / "flux-dipole-sphere.svg")

def compress_perp():
    s = Svg(700, 360, "Compression of a flux tube across the field",
            "A wide horizontal flux tube of cross-section A_1 with a magnetic field B_1 along its "
            "axis. Arrows v above and below it point towards the axis: the tube is squeezed from "
            "the sides into a much thinner tube of cross-section A_2 below, whose field B_2 is "
            "stronger, shown by a longer arrow.", "perp")
    x1, x2 = 150, 680
    cy, ry, rx = 100, 62, 24
    s.line(x1, cy - ry, x2, cy - ry)
    s.line(x1, cy + ry, x2, cy + ry)
    s.ellipse(x1, cy, rx, ry, fill="#fff")
    s.line(205, cy, 340, cy, BLUE, 2.4, head=True)
    s.text(350, cy + 28, "B_1", bold=True, fill=BLUE, size=24)
    s.text(60, cy + 6, "A_1", anchor="middle")
    s.line(420, 8, 420, 32, w=2, head=True)
    s.text(436, 28, "v", bold=True)
    s.line(420, 250, 420, 200, w=2, head=True)
    s.text(436, 232, "v", bold=True)
    cy2, ry2, rx2 = 300, 22, 9
    s.line(x1, cy2 - ry2, x2, cy2 - ry2)
    s.line(x1, cy2 + ry2, x2, cy2 + ry2)
    s.ellipse(x1, cy2, rx2, ry2, fill="#fff")
    s.line(190, cy2, 570, cy2, BLUE, 2.4, head=True)
    s.text(585, cy2 + 8, "B_2", bold=True, fill=BLUE, size=24)
    s.text(60, cy2 + 6, "A_2", anchor="middle")
    s.save(OUT / "flux-compression-perpendicular.svg")


def io_jupiter():
    s = Svg(700, 470, "Magnetic flux tube connecting Io and Jupiter",
            "View of Jupiter (circle) and the circular orbit of Io, seen from above the rotation "
            "axis. A thick blue flux tube joins Io to its foot on Jupiter, which is displaced by "
            "a longitude difference delta-phi (dashed lines) from the direction to Earth. Radio "
            "emission from the foot is beamed in a cone, drawn as two rays at an angle mu on "
            "either side of the direction perpendicular to the field; a downward arrow marks "
            "the direction to Earth.", "io")
    jx, jy, R = 300, 200, 52
    ro = 190
    s.circle(jx, jy, ro, w=1.5)
    ia = math.radians(-12)
    ix, iy = jx + ro * math.cos(ia), jy + ro * math.sin(ia)
    s.circle(ix, iy, 8, fill="#000")
    s.text(ix + 14, iy + 6, "Io", italic=False)
    s.text(jx - 40, jy - ro + 36, "Io's orbit", italic=False, anchor="middle")
    fa = math.radians(18)
    fx, fy = jx + R * math.cos(fa), jy + R * math.sin(fa)
    s.line(ix - 9, iy + 2, fx + 2, fy - 1, BLUE, 5)
    s.circle(jx, jy, R, fill="#fff", w=2)
    s.circle(fx, fy, 6, fill=BLUE, stroke=BLUE)
    s.circle(jx, jy, 3, fill="#000")
    s.text(jx - 8, jy - R - 12, "Jupiter", italic=False, anchor="middle")
    s.line(jx, jy, jx, jy + 150, w=1.5, dash="7 5")
    s.line(jx, jy, fx, fy, w=1.5, dash="7 5")
    s.path(f"M {jx} {jy + 34} A 34 34 0 0 0 {jx + 34 * math.cos(fa):.1f} {jy + 34 * math.sin(fa):.1f}",
           w=1.5, head=True)
    s.text(jx + 8, jy + 74, "\u0394\u03c6")
    dx, dy = fx - ix, fy - iy
    n = math.hypot(dx, dy)
    px, py = -dy / n, dx / n
    if py < 0:
        px, py = -px, -py
    mu = math.radians(24)
    L = 125
    for sg in (-1, 1):
        c, sn = math.cos(sg * mu), math.sin(sg * mu)
        s.line(fx, fy, fx + L * (px * c - py * sn), fy + L * (px * sn + py * c), w=1.5, head=True)
    s.line(fx, fy, fx + L * px, fy + L * py, w=1.2, dash="3 4")
    mx, my = fx + 0.8 * L * px, fy + 0.8 * L * py
    s.path(f"M {fx + 80 * (px * math.cos(mu) - py * math.sin(-mu)):.1f} "
           f"{fy + 80 * (px * math.sin(-mu) + py * math.cos(mu)):.1f} "
           f"A 80 80 0 0 1 {fx + 80 * (px * math.cos(mu) - py * math.sin(mu)):.1f} "
           f"{fy + 80 * (px * math.sin(mu) + py * math.cos(mu)):.1f}", w=1.2)
    s.text(mx + 8, my + 4, "\u03bc")
    s.text(fx + 70, fy - 128, "foot of Io's", italic=False, anchor="middle")
    s.text(fx + 70, fy - 106, "flux tube", italic=False, anchor="middle")
    s.line(fx + 56, fy - 94, fx + 6, fy - 12, w=1.2, head=True)
    s.line(630, 300, 630, 430, w=7, head=True)
    s.text(630, 458, "to Earth", italic=False, anchor="middle")
    s.save(OUT / "flux-io-jupiter-tube.svg")


def io_footprint():
    s = Svg(780, 330, "Footprint and cross-section of the Io flux tube",
            "Left: the footprint of the flux tube on Jupiter's atmosphere is an ellipse with "
            "semi-axes X along x and Y along y, surrounded by a thin shaded boundary layer of "
            "width 2 epsilon. Blue field lines pass over and under it. Right: Jupiter, of "
            "radius R_J, rotating about a vertical axis, and Io at distance a. The flux tube "
            "leaves the planet at colatitude theta_i and loops out to Io; arrows labelled I "
            "show the current flowing along the tube.", "foot")
    cx, cy, X, Y = 180, 160, 125, 75
    s.ellipse(cx, cy, X + 9, Y + 9, fill=GRAY, stroke="#000", w=1.4)
    s.ellipse(cx, cy, X, Y, fill="#fff", w=2)
    for yy in (-1, 1):
        ty = cy + yy * (Y + 5)
        for k in (-24, 0, 24):
            s.line(cx, ty, 8, ty + yy * k, BLUE, 1.6, head=True)
            s.line(cx, ty, 352, ty + yy * k, BLUE, 1.6, head=True)
    s.line(cx - 160, cy, cx + 175, cy, w=1.4, head=True)
    s.line(cx, cy + 105, cx, cy - 135, w=1.4, head=True)
    s.text(cx + 175, cy + 24, "x", anchor="end")
    s.text(cx + 8, cy - 118, "y")
    s.line(cx, cy + 36, cx - X, cy + 36, w=1.5, head=True, tail=True)
    s.text(cx - X / 2, cy + 28, "X", anchor="middle")
    s.line(cx - 28, cy, cx - 28, cy - Y, w=1.5, head=True, tail=True)
    s.text(cx - 52, cy - 28, "Y", anchor="middle")
    s.bracket(24, cy - Y - 5 - 24, 24, cy - Y - 5 + 24)
    s.text(16, cy - Y - 38, "2\u03b5")
    jx, jy, R = 430, 175, 52
    s.circle(jx, jy, R, fill="#fff", w=2)
    s.line(jx, jy - R - 40, jx, jy + R + 40, w=1.3)
    s.path(f"M {jx - 20} {jy - R - 42} A 22 8 0 0 1 {jx + 20} {jy - R - 42}", w=1.4, head=True)
    s.line(jx, jy, jx - R, jy, w=1.5)
    s.text(jx - 28, jy - 8, "R_J", anchor="middle")
    ix = 725
    s.line(jx + 6, jy, ix - 10, jy, w=1.5, head=True)
    s.text((jx + ix) / 2, jy - 8, "a", anchor="middle")
    s.circle(ix, jy, 6, fill="#000")
    s.text(ix + 4, jy + 30, "Io", italic=False, anchor="middle")
    th = math.radians(30)
    fx, fy = jx + R * math.sin(th), jy - R * math.cos(th)
    s.line(jx, jy, fx, fy, w=1.5)
    s.path(f"M {jx} {jy - 34} A 34 34 0 0 1 {jx + 34 * math.sin(th):.1f} {jy - 34 * math.cos(th):.1f}",
           w=1.5, head=True)
    s.text(jx - 30, jy - 30, "\u03b8_i")
    for sg in (1, -1):
        for k in (0, 1):
            y0 = jy + sg * (fy - jy)
            x0 = fx + 2 * k
            pts = bezier((x0, y0 - sg * 0), (x0 + 60, jy - sg * (140 + 8 * k)),
                         (ix + 30 + 8 * k, jy - sg * (115 + 8 * k)), (ix, jy), 80)
            s.poly(pts, w=1.5)
            if k == 0:
                i = 46
                (a, b), (c, d) = pts[i], pts[i + 1]
                if sg == -1:
                    (a, b), (c, d) = (c, d), (a, b)
                s.line(a, b, c, d, w=1.5, head=True)
    s.text(ix - 40, 24, "I")
    s.save(OUT / "flux-io-footprint.svg")


def pulsar():
    s = Svg(780, 520, "Schematic pulsar magnetosphere",
            "Half of an aligned pulsar magnetosphere in a plane containing the rotation axis "
            "(left edge), with the star at the lower left. Closed dipolar field lines form the "
            "hatched co-rotating magnetosphere, whose outer edge touches the light cylinder, a "
            "dashed vertical line. Open field lines leave the polar cap, within an angle theta_0 "
            "of the axis, and run out into the wind zone beyond the light cylinder. The upper "
            "open line carries electrons, the lower one protons, and the critical line between "
            "them reaches the light cylinder at the end of a thin dashed line along which minus "
            "and plus signs mark the charges of the plasma.", "pulsar")
    ox, oy, Rs = 50, 485, 38
    lc = 470
    RL = lc - ox

    def closed(L):
        t0 = math.asin(math.sqrt(Rs / L))
        out = []
        for i in range(241):
            t = t0 + (math.pi / 2 - t0) * i / 240
            r = L * math.sin(t) ** 2
            out.append((ox + r * math.sin(t), oy - r * math.cos(t)))
        return out

    s.raw('<defs><pattern id="hatch" width="14" height="14" patternUnits="userSpaceOnUse" '
          'patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="14" stroke="#000" '
          'stroke-width="1.2"/></pattern></defs>')
    s.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in closed(RL)) + f" L {ox + Rs} {oy} Z",
           fill="url(#hatch)", w=0)
    s.path("M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in closed(250)) + f" L {ox + Rs} {oy} Z",
           fill="#fff", w=0)
    s.poly(closed(RL), w=2.2)
    s.poly(closed(250), w=1.6)
    s.path(f"M {ox} {oy - Rs} A {Rs} {Rs} 0 0 1 {ox + Rs} {oy}", w=2.2, fill="#fff")
    s.line(lc, 8, lc, oy, w=1.8, dash="12 8")
    s.line(ox - 22, 440, ox - 22, 300, w=1.5, head=True)
    s.path(f"M {ox - 44} 290 A 22 8 0 0 1 {ox} 290", w=1.4, head=True)
    s.line(ox, oy, ox, oy - 140, w=1.2, dash="3 4")
    t0 = math.radians(17)
    s.line(ox, oy, ox - 90 * math.sin(t0), oy - 90 * math.cos(t0), w=1.2, dash="3 4")
    s.path(f"M {ox} {oy - 64} A 64 64 0 0 0 {ox - 64 * math.sin(t0):.1f} {oy - 64 * math.cos(t0):.1f}",
           w=1.3)
    s.text(ox - 22, oy - 72, "\u03b8_0")

    def start(deg):
        t = math.radians(deg)
        return ox + Rs * math.sin(t), oy - Rs * math.cos(t)

    def line_arrow(p0, segs, at, dist=4):
        pts = []
        cur = p0
        for c1, c2, e in segs:
            pts += bezier(cur, c1, c2, e, 80)
            cur = e
        s.poly(pts, w=2.2)
        (a, b), (c, d) = pts[at], pts[at + 1]
        k = dist / math.hypot(c - a, d - b)
        s.line(a, b, a + (c - a) * k * 3, b + (d - b) * k * 3, w=2.2, head=True)
        return pts

    line_arrow(start(5), [((110, 330), (330, 215), (480, 150)), ((560, 110), (640, 70), (740, 20))], 118)
    pb = line_arrow(start(10), [((140, 330), (300, 290), (470, 285)), ((540, 280), (620, 270), (740, 190))], 118)
    line_arrow(start(14), [((120, 350), (250, 335), (330, 340)), ((420, 345), (600, 420), (740, 355))], 118)
    s.line(ox + 22, oy - 12, lc, 285, w=1.2, dash="9 6")
    s.text(lc + 20, 100, "electrons", italic=False)
    s.text(lc + 20, 228, "wind zone", italic=False)
    s.text(lc + 20, 330, "protons", italic=False)
    ix = min(range(len(pb)), key=lambda i: abs(pb[i][0] - 250))
    s.text(160, 235, "critical line", italic=False, anchor="end")
    s.line(166, 240, pb[ix][0] - 3, pb[ix][1] - 4, w=1.2, head=True)
    s.text(lc - 54, 44, "light cylinder", italic=False, anchor="end")
    s.line(lc - 48, 38, lc - 5, 38, w=1.2, head=True)
    s.text(190, 440, "co-rotating", italic=False, anchor="middle")
    s.text(190, 464, "magnetosphere", italic=False, anchor="middle")
    for x in (385, 440, 520, 575):
        y = 485 - (x - 72) * (200 / 420) if x < lc else 285 - (x - lc) * 0.1
        s.text(x - 12, y - 10, "\u2212", italic=False, anchor="middle", size=24)
        s.text(x + 12, y + 24, "+", italic=False, anchor="middle", size=24)
    s.save(OUT / "flux-pulsar-magnetosphere.svg")


if __name__ == "__main__":
    tube()
    compress_parallel()
    resistive()
    ambipolar()
    toy()
    dipole()
    compress_perp()
    io_jupiter()
    io_footprint()
    pulsar()
