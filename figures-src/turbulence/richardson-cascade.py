"""Generate figures/turbulence/richardson-cascade.svg (hand-tuned SVG, no dependencies).

Rows of wobbly eddies whose size shrinks by a factor r per generation, from the
injection scale l0 down to the dissipation scale l_d; arrows on the right show
the energy injection, the constant flux across scales, and the dissipation.
Run from the repository root: python3 figures-src/turbulence/richardson-cascade.py
"""
import math, random

random.seed(3)
W, H = 700, 470
FONT = "'Latin Modern Math', 'STIX Two Math', 'Cambria Math', serif"


def blob(cx, cy, rx, ry):
    """Closed wobbly curve around (cx, cy) as an SVG path (smooth, via midpoints)."""
    n = 10
    phase = random.uniform(0, 2 * math.pi)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        f = 1 + 0.12 * math.sin(3 * t + phase) + 0.06 * random.uniform(-1, 1)
        pts.append((cx + rx * f * math.cos(t), cy + ry * f * math.sin(t)))
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f"M {mids[-1][0]:.1f} {mids[-1][1]:.1f} "
    for i in range(n):
        d += f"Q {pts[i][0]:.1f} {pts[i][1]:.1f} {mids[i][0]:.1f} {mids[i][1]:.1f} "
    return f'<path d="{d}Z" fill="none" stroke="#000" stroke-width="1.6"/>'


rows = [  # (label, y, count, rx, ry)
    ("ℓ<tspan baseline-shift='sub' font-size='15'>0</tspan>", 75, 3, 58, 42),
    ("rℓ<tspan baseline-shift='sub' font-size='15'>0</tspan>", 175, 5, 36, 26),
    ("r<tspan baseline-shift='super' font-size='15'>2</tspan>ℓ<tspan baseline-shift='sub' font-size='15'>0</tspan>", 248, 9, 20, 14),
    ("r<tspan baseline-shift='super' font-size='15'>3</tspan>ℓ<tspan baseline-shift='sub' font-size='15'>0</tspan>", 298, 16, 11, 8),
]
x0, x1 = 100, 470
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="title desc">',
       '<title id="title">The Richardson cascade</title>',
       '<desc id="desc">Rows of eddies of decreasing size: a few large eddies of size l0 at the top, then more '
       'eddies of size r l0, r squared l0, r cubed l0, down to the dissipation scale l_d, drawn as a dotted line. '
       'Arrows on the right show energy injected at the rate P at the top, a constant flux of energy P '
       'from large to small scales, and dissipation of energy at the rate P at the bottom.</desc>',
       '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
       '<path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="#000" stroke-width="1.6"/></marker></defs>',
       f'<rect width="{W}" height="{H}" fill="#fff"/>']
for label, y, count, rx, ry in rows:
    step = (x1 - x0) / count
    for i in range(count):
        out.append(blob(x0 + step * (i + 0.5), y, rx * 0.95, ry))
    out.append(f'<text x="30" y="{y + 7}">{label}</text>')
out.append(f'<line x1="{(x0 + x1) / 2}" y1="330" x2="{(x0 + x1) / 2}" y2="385" stroke="#000" stroke-width="1.6" stroke-dasharray="2 6"/>')
out.append(f'<line x1="{x0}" y1="420" x2="{x1}" y2="420" stroke="#000" stroke-width="1.6" stroke-dasharray="2 6"/>')
out.append('<text x="34" y="427">ℓ<tspan baseline-shift="sub" font-size="15">d</tspan></text>')
# arrows and labels on the right
out.append('<line x1="545" y1="15" x2="505" y2="55" stroke="#000" stroke-width="1.8" marker-end="url(#arrow)"/>')
out.append('<text x="520" y="80" font-style="normal">Injection of</text><text x="520" y="104" font-style="normal">energy <tspan font-style="italic">𝒫</tspan></text>')
out.append('<line x1="505" y1="125" x2="505" y2="380" stroke="#000" stroke-width="1.8" marker-end="url(#arrow)"/>')
out.append('<text x="520" y="245" font-style="normal">Flux of</text><text x="520" y="269" font-style="normal">energy <tspan font-style="italic">𝒫</tspan></text>')
out.append('<line x1="505" y1="400" x2="545" y2="440" stroke="#000" stroke-width="1.8" marker-end="url(#arrow)"/>')
out.append('<text x="555" y="425" font-style="normal">Dissipation of</text><text x="555" y="449" font-style="normal">energy <tspan font-style="italic">𝒫</tspan></text>')
out.append('</svg>')
svg = "\n".join(out).replace("<text ", f'<text font-family="{FONT}" font-size="20" fill="#000" font-style="italic" ', )
# The labels above already set font-style where it differs; later attributes win in our order, so fix duplicates:
import re
svg = re.sub(r'font-style="italic" (x="[^"]*" y="[^"]*") font-style="normal"', r'\1 font-style="normal"', svg)
svg = re.sub(r'font-style="italic" (x="[^"]*" y="[^"]*") font-style="italic"', r'\1 font-style="italic"', svg)
open("figures/turbulence/richardson-cascade.svg", "w").write(svg + "\n")
