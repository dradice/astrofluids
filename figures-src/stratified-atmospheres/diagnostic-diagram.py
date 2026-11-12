"""Dispersion relation of waves in an isothermal atmosphere (Ch. 10), K = 0.

Regenerates figures/stratified-atmospheres/diagnostic-diagram.svg:
    python3 figures-src/stratified-atmospheres/diagnostic-diagram.py
Solves w^4 - w^2 (X^2 + 1) + n^2 X^2 = 0, with w = omega / omega_ac,
X = c_s k_x / omega_ac and n = N / omega_ac = 2 sqrt(Gamma - 1) / Gamma.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import re  # noqa: E402

import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "stratified-atmospheres" / "diagnostic-diagram.svg"

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "hatch.linewidth": 0.6,
})

gamma = 5 / 3
n = 2 * np.sqrt(gamma - 1) / gamma
X = np.linspace(0, 3, 400)
S = X**2 + 1
D = np.sqrt(S**2 - 4 * n**2 * X**2)
wp = np.sqrt((S + D) / 2)
wg = np.sqrt((S - D) / 2)
top = 3.2

fig, ax = plt.subplots(figsize=(7, 4.4))
ax.fill_between(X, wp, top, facecolor="#dbe9f6", edgecolor="#0072B2", hatch="//", lw=0)
ax.fill_between(X, 0, wg, facecolor="#fbe3d4", edgecolor="#D55E00", hatch="\\\\", lw=0)
ax.plot(X, wp, color="#0072B2", lw=2)
ax.plot(X, wg, color="#D55E00", lw=2, ls="--")
ax.plot(X, X, color="#000000", lw=1.4, ls=":")
ax.axhline(1, color="#777777", lw=0.8)
ax.axhline(n, color="#777777", lw=0.8)
ax.text(3.02, 1.0, "ω_ac", va="bottom", fontsize=11)
ax.text(3.02, n, "N", va="top", fontsize=11)
ax.text(0.9, 2.6, "acoustic waves (p-modes)", ha="center", fontsize=12,
        bbox=dict(facecolor="white", edgecolor="none", pad=2))
ax.text(1.9, 0.45, "gravity waves (g-modes)", ha="center", fontsize=12,
        bbox=dict(facecolor="white", edgecolor="none", pad=2))
ax.annotate("Lamb wave", xy=(0.93, 0.93), xytext=(1.75, 1.3), fontsize=11,
            arrowprops=dict(arrowstyle="->", color="#000000", lw=1))
ax.set_xlim(0, 3)
ax.set_ylim(0, top)
ax.set_xlabel("c_s k_x / ω_ac", fontstyle="italic")
ax.set_ylabel("ω / ω_ac", fontstyle="italic")
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor="white")
# Subscripts without mathtext: turn "_ab" inside <text> elements into SVG subscripts.
svg = OUT.read_text()
svg = re.sub(r"(<text[^>]*>)([^<]*)(</text>)",
             lambda m: m.group(1) + re.sub(r"_([A-Za-z]+)",
                                           r'<tspan baseline-shift="sub" font-size="75%">\1</tspan>',
                                           m.group(2)) + m.group(3), svg)
OUT.write_text(svg)
print(f"wrote {OUT}", n)
