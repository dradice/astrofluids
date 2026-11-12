#!/usr/bin/env python3
"""Figures of Chapter 25 (Magnetic tension), redrawn from the 2025 TeXmacs drawings.

Usage: python3 figures-src/magnetic-tension/make-figures.py   (from the notes/ directory)
"""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "magnetic-tension"


def pressure_tension():
    s = Svg(760, 300, "Magnetic pressure and magnetic tension forces",
            "Left panel: a bundle of field lines pointing out of the page (circled dots, with "
            "unit vector b-hat); four arrows pointing diagonally outward show the magnetic "
            "pressure force, minus the perpendicular gradient of B squared over 8 pi. Right "
            "panel: a curved field line (blue) with direction b-hat; an arrow from the curve "
            "towards its centre of curvature shows the tension force B squared over 4 pi times "
            "(b-hat dot nabla) b-hat.", "pt")
    cx, cy = 150, 165
    for dx, dy in ((0, 0), (-65, 0), (65, 0), (0, -65), (0, 65)):
        s.out_of_plane(cx + dx, cy + dy)
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        s.line(cx + sx * 26, cy + sy * 26, cx + sx * 80, cy + sy * 80, head=True)
    s.text(cx + 82, cy + 8, "b̂", bold=True, size=22)
    s.text(48, 52, "−∇_⊥ B^2/8π", italic=True, size=20)
    # tension panel
    s.path("M 455 265 C 455 190 480 120 620 115", BLUE, 2.6, head=True)
    s.text(595, 150, "b̂", bold=True, fill=BLUE, size=22)
    s.line(490, 160, 590, 260, w=1.5, head=True)
    s.text(600, 243, "(B^2/4π) (b̂·∇) b̂", size=20)
    s.save(OUT / "tension-pressure-tension.svg")


def prominence():
    s = Svg(560, 360, "Force diagram for a Solar prominence",
            "A grey ellipse (the prominence) inside a rectangular control volume V above the "
            "curved solar photosphere. Blue magnetic field lines rise from the photosphere, "
            "arch over the prominence and come back down, passing through the volume above and "
            "to the sides of the prominence. The gravitational acceleration g points down, "
            "towards the photosphere.", "prom")
    s.rect(160, 110, 156, 62)
    s.ellipse(238, 141, 78, 25, fill=GRAY)
    s.path("M 10 300 Q 238 190 468 300", w=1.6)  # photosphere
    s.text(240, 330, "Solar photosphere", anchor="middle", italic=False, size=20)
    s.text(240, 62, "prominence", anchor="middle", italic=False, size=20)
    s.text(272, 211, "V", size=20)
    s.line(176, 198, 176, 250, w=1.5, head=True)
    s.text(147, 224, "g", bold=True, size=20)
    s.text(97, 202, "B", bold=True, fill=BLUE, size=24)
    s.path("M 22 280 C 8 160 10 55 70 55 C 105 55 140 80 186 112", BLUE, 1.7, head=True)
    s.path("M 62 262 C 52 160 62 90 95 92 C 115 94 133 112 158 133", BLUE, 1.7, head=True)
    s.path("M 318 134 C 360 100 380 100 395 135 C 410 175 418 240 400 270", BLUE, 1.7, head=True)
    s.path("M 290 112 C 340 58 370 32 392 38 C 430 48 465 120 470 290", BLUE, 1.7, head=True)
    s.save(OUT / "tension-prominence-forces.svg")


def atmosphere():
    s = Svg(700, 520, "Plane-parallel magnetized atmosphere",
            "Axes y (horizontal) and z (vertical). Three horizontal green lines represent the "
            "magnetic field B(y, z), parallel to the y axis. Blue dots represent the gas, which "
            "is denser at the bottom than at the top. A blue arrow pointing down is labelled "
            "minus nabla Psi, the direction of gravity.", "atm")
    s.line(15, 460, 685, 460, w=1.6)
    s.line(348, 460, 348, 15, w=1.6)
    s.text(360, 30, "z", size=22, fill=BLUE)
    s.text(668, 492, "y", size=22, fill=BLUE)
    for y in (126, 237, 347):
        s.line(15, y, 685, y, GREEN, 3.2)
    s.text(526, 112, "B(y, z)", fill=GREEN, size=22)
    s.line(238, 103, 238, 215, BLUE, 3, head=True)
    s.text(130, 168, "−∇Ψ", fill=BLUE, size=22)
    rnd = random.Random(7)
    n = 0
    while n < 170:
        x = rnd.uniform(15, 683)
        y = rnd.uniform(60, 452)
        if abs(x - 348) < 8:
            continue
        if rnd.random() < math.exp(-(452 - y) / 120.0):
            s.circle(x, y, 2.2, fill=BLUE, stroke=BLUE, w=1)
            n += 1
    s.save(OUT / "tension-atmosphere.svg")


def reconnection():
    s = Svg(700, 430, "Explosive reconnection between two plates",
            "Panel (a): two grey conducting plates, one above the other, a distance 2D apart. "
            "Two field lines B (blue) are anchored on the plates and bowed towards each other, "
            "with height l; black arrows labelled f show the external force that "
            "stretches them, and the horizontal extent of each arc is D. Panel (b): after "
            "reconnection the field lines are straight, running between the plates, and arrows "
            "labelled v show the plasma moving outwards.", "recon")
    # (a)
    s.text(258, 22, "(a)", anchor="middle", size=18)
    s.rect(187, 40, 142, 22, fill=GRAY)
    s.rect(187, 360 - 22, 142, 22, fill=GRAY)
    s.path("M 313 61 C 301 130 281 142 258 142 C 235 142 215 130 205 61", BLUE, 2.4, head=True)
    s.path("M 205 338 C 215 270 235 190 258 190 C 281 190 301 270 311 338", BLUE, 2.4, head=True)
    s.line(258, 85, 258, 125, w=1.5, head=True)
    s.line(258, 255, 258, 205, w=1.5, head=True)
    s.text(272, 85, "f", bold=True, size=20)
    s.text(295, 228, "B", bold=True, fill=BLUE, size=22)
    s.bracket(167, 190, 167, 338)
    s.text(148, 270, "ℓ", anchor="middle", size=22)
    s.bracket(205, 395, 258, 395)
    s.text(231, 417, "D", anchor="middle", size=22)
    # (b)
    s.text(542, 22, "(b)", anchor="middle", size=18)
    s.rect(471, 40, 142, 22, fill=GRAY)
    s.rect(471, 338, 142, 22, fill=GRAY)
    s.line(488, 337, 488, 62, BLUE, 2.4, head=True)
    s.line(591, 62, 591, 337, BLUE, 2.4, head=True)
    s.bracket(450, 62, 450, 338)
    s.text(432, 205, "2D", anchor="end", size=22)
    s.line(535, 205, 492, 205, w=1.5, head=True)
    s.line(548, 205, 590, 205, w=1.5, head=True)
    s.text(542, 188, "v", bold=True, anchor="middle", size=20)
    s.save(OUT / "tension-reconnection.svg")


if __name__ == "__main__":
    pressure_tension()
    prominence()
    atmosphere()
    reconnection()
