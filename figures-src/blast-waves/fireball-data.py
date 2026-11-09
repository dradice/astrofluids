"""Blast-wave radius versus time for the atmospheric explosion of the in-class worksheet.

Regenerates figures/blast-waves/fireball-data.svg:
    python3 figures-src/blast-waves/fireball-data.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "code" / "blast-waves" / "fireball.dat"
OUT = ROOT / "figures" / "blast-waves" / "fireball-data.svg"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 15})

t, r = np.loadtxt(DATA, unpack=True)
fig, ax = plt.subplots(figsize=(6, 3.6))
ax.plot(t, r, "ko", ms=6)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("t (ms)")
ax.set_ylabel("R (m)")
ax.grid(which="both", color="#bbbbbb", lw=0.6)
ax.set_xlim(0.07, 1.2)
ax.set_ylim(15, 120)
# plain tick labels: mathtext superscripts (10^1) do not survive svg.fonttype = none
from matplotlib.ticker import FixedLocator, FuncFormatter, NullFormatter  # noqa: E402
ax.xaxis.set_major_locator(FixedLocator([0.1, 0.2, 0.5, 1.0]))
ax.yaxis.set_major_locator(FixedLocator([20, 30, 50, 100]))
plain = FuncFormatter(lambda v, _: f"{v:g}")
ax.xaxis.set_major_formatter(plain)
ax.yaxis.set_major_formatter(plain)
ax.xaxis.set_minor_formatter(NullFormatter())
ax.yaxis.set_minor_formatter(NullFormatter())
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor="white")
print(f"wrote {OUT}")
