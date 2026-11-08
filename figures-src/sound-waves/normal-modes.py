"""Normal modes of a gas in a pipe closed at both ends: sin(n pi z / L), n = 1..5.

Regenerates figures/sound-waves/normal-modes.svg:
    python3 figures-src/sound-waves/normal-modes.py
Modes are distinguished by line style as well as colour, and all colours have
at least 3:1 contrast against white.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "sound-waves" / "normal-modes.svg"

plt.rcParams.update({
    "svg.fonttype": "none",  # keep text as text in the SVG (no mathtext!)
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Okabe-Ito / Tol colours (colour-blind safe), each >= 3:1 contrast on white
colors = ["#0072B2", "#D55E00", "#009E73", "#AA4499", "#000000"]
styles = ["-", "--", "-.", ":", (0, (5, 1, 1, 1, 1, 1))]

z = np.linspace(0, 1, 500)
fig, ax = plt.subplots(figsize=(7, 3.6))
for n, (c, ls) in enumerate(zip(colors, styles), start=1):
    ax.plot(z, np.sin(n * np.pi * z), color=c, ls=ls, lw=2, label=f"n = {n}")
ax.axhline(0, color="#777777", lw=0.8)
ax.set_xlim(0, 1)
ax.set_ylim(-1.05, 1.05)
ax.set_xlabel("z / L", fontstyle="italic")
ax.set_ylabel("sin(nπz / L)")
ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False, handlelength=3)
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor="white")
print(f"wrote {OUT}")
