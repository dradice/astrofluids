"""Generate figures/plasma/em-wave-electron.svg (no dependencies).

A linearly polarized electromagnetic wave travelling along x (Poynting vector S),
with E oscillating in the vertical plane and B in the horizontal plane (drawn in
oblique projection). On the right, an electron in the wave: E points up, the
electron is pushed down (velocity v), and the magnetic part of the Lorentz force
F points along the direction of propagation.
Run from the repository root: python3 figures-src/plasma/em-wave-electron.py
"""
import math

W, H = 660, 380
Y0 = 200            # height of the x axis
XA, XB = 20, 400    # one wavelength of the wave
AE, AB = 120, 80    # amplitudes of E (vertical) and B (oblique)
OB = (-0.55, 0.45)  # screen direction of the z axis (oblique projection)
XE = 500            # position of the electron
FONT = "'Latin Modern Math', 'STIX Two Math', 'Cambria Math', serif"
RED, BLUE, GREEN = "#b2182b", "#2166ac", "#1b7837"


def phase(x):
    return math.sin(2 * math.pi * (x - XA) / (XB - XA))


def e_point(x):
    return x, Y0 - AE * phase(x)


def b_point(x):
    b = AB * phase(x)
    return x + OB[0] * b, Y0 + OB[1] * b


def poly(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


xs = [XA + i for i in range(XB - XA + 1)]
out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">',
    '<title id="title">Lorentz force on an electron in an electromagnetic wave</title>',
    '<desc id="desc">An electromagnetic wave travels to the right along the x axis, in the direction of the '
    'Poynting vector S. The electric field E oscillates in the vertical plane and the magnetic field B, in phase '
    'with it, in the perpendicular horizontal plane. On the right, an electron sits in a plane perpendicular to the '
    'direction of propagation, where E points up: the electric force accelerates the electron downwards, giving it '
    'a velocity v, and the magnetic force F, proportional to v cross B, points to the right, along the direction '
    'of propagation.</desc>',
    '<defs>'
    + "".join(
        f'<marker id="a{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="{s}" markerHeight="{s}" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 Z" fill="{c}"/></marker>'
        for n, c, s in [("k", "#000", 7), ("r", RED, 5), ("b", BLUE, 5), ("g", GREEN, 5), ("rb", RED, 6), ("bb", BLUE, 6)]
    )
    + "</defs>",
    f'<rect width="{W}" height="{H}" fill="#fff"/>',
]
# plane through the electron, perpendicular to x (oblique projection)
p = [(XE + 70 * OB[0] * -1, Y0 - 150 + 70 * OB[1] * -1), (XE + 70 * OB[0], Y0 - 150 + 70 * OB[1]),
     (XE + 70 * OB[0], Y0 + 150 + 70 * OB[1]), (XE - 70 * OB[0], Y0 + 150 - 70 * OB[1])]
out.append(f'<polygon points="{poly(p)}" fill="#e3eef0" stroke="#7a9ca3" stroke-width="1"/>')
# B: hatching and curve (dashed, so it is distinguishable without colour)
for x in range(XA + 15, XB, 22):
    bx, by = b_point(x)
    if abs(phase(x)) > 0.12:
        out.append(f'<line x1="{x}" y1="{Y0}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE}" stroke-width="1.4" marker-end="url(#ab)"/>')
out.append(f'<polyline points="{poly(b_point(x) for x in xs)}" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="7 4"/>')
# E: arrows and curve
for x in range(XA + 15, XB, 22):
    ex, ey = e_point(x)
    if abs(phase(x)) > 0.12:
        out.append(f'<line x1="{x}" y1="{Y0}" x2="{ex}" y2="{ey:.1f}" stroke="{RED}" stroke-width="1.4" marker-end="url(#ar)"/>')
out.append(f'<polyline points="{poly(e_point(x) for x in xs)}" fill="none" stroke="{RED}" stroke-width="2"/>')
# x axis
out.append(f'<line x1="{XA}" y1="{Y0}" x2="{W - 30}" y2="{Y0}" stroke="#000" stroke-width="1.6" marker-end="url(#ak)"/>')
# S arrow
out.append(f'<line x1="170" y1="40" x2="270" y2="40" stroke="#000" stroke-width="3" marker-end="url(#ak)"/>')
# vectors at the electron
out.append(f'<line x1="{XE}" y1="{Y0}" x2="{XE}" y2="{Y0 - 110}" stroke="{RED}" stroke-width="3" marker-end="url(#arb)"/>')
out.append(f'<line x1="{XE}" y1="{Y0}" x2="{XE}" y2="{Y0 + 80}" stroke="{GREEN}" stroke-width="3" marker-end="url(#ag)"/>')
bx, by = XE + 75 * OB[0] / math.hypot(*OB), Y0 + 75 * OB[1] / math.hypot(*OB)
out.append(f'<line x1="{XE}" y1="{Y0}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BLUE}" stroke-width="3" marker-end="url(#abb)"/>')
out.append(f'<line x1="{XE}" y1="{Y0}" x2="{XE + 75}" y2="{Y0}" stroke="{RED}" stroke-width="3" marker-end="url(#arb)"/>')
out.append(f'<circle cx="{XE}" cy="{Y0}" r="7" fill="#555" stroke="#000"/>')
# labels
T = f'font-family="{FONT}" font-size="20" fill="#000"'
labels = [
    (205, 30, '<tspan font-weight="bold">S</tspan>'),
    (55, 105, '<tspan font-weight="bold">E</tspan>'),
    (22, 252, '<tspan font-weight="bold">B</tspan>'),
    (XE + 10, Y0 - 95, '<tspan font-weight="bold">E</tspan>'),
    (XE + 10, Y0 + 72, '<tspan font-weight="bold">v</tspan>'),
    (bx - 28, by + 12, '<tspan font-weight="bold">B</tspan>'),
    (XE + 48, Y0 - 10, '<tspan font-weight="bold">F</tspan>'),
    (XE - 28, Y0 - 12, '<tspan font-style="italic">e</tspan><tspan baseline-shift="super" font-size="15">−</tspan>'),
    (W - 28, Y0 + 26, '<tspan font-style="italic">x</tspan>'),
]
for x, y, t in labels:
    out.append(f'<text x="{x:.0f}" y="{y:.0f}" {T}>{t}</text>')
out.append("</svg>")
open("figures/plasma/em-wave-electron.svg", "w").write("\n".join(out) + "\n")
