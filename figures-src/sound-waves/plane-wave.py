"""A plane sound wave at t = 0: displacement, density perturbation, and fluid elements.

Regenerates figures/sound-waves/plane-wave.svg:
    python3 figures-src/sound-waves/plane-wave.py
xi_z = A cos(kz) and delta rho / rho_0 = kA sin(kz) (Eq. 9.22 with B = 0).
Curves are distinguished by line style as well as colour.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "sound-waves" / "plane-wave.svg"

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

x = np.linspace(0, 2, 600)  # kz / 2 pi
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 4.6), sharex=True,
                               gridspec_kw={"height_ratios": [2, 1.1]})
ax1.plot(x, np.cos(2 * np.pi * x), color="#0072B2", lw=2, label="displacement ξ / A")
ax1.plot(x, np.sin(2 * np.pi * x), color="#D55E00", lw=2, ls="--", label="density δρ / (kAρ₀)")
ax1.axhline(0, color="#777777", lw=0.8)
ax1.set_ylim(-1.15, 1.15)
ax1.legend(loc="upper center", bbox_to_anchor=(0.5, 1.22), ncol=2, frameon=False, handlelength=3)

# fluid elements: equally spaced, then displaced by a cos(kz) with ka = 0.6
z0 = np.arange(0, 2, 1 / 20) + 1 / 40
a = 0.6 / (2 * np.pi)
zd = z0 + a * np.cos(2 * np.pi * z0)
ax2.scatter(z0, np.full_like(z0, 1.0), s=18, color="#8c8c8c")
ax2.scatter(zd, np.zeros_like(zd), s=30, color="#000000")
ax2.set_ylim(-0.6, 1.6)
ax2.set_yticks([0, 1])
ax2.set_yticklabels(["displaced", "at rest"])
ax2.spines["left"].set_visible(False)
ax2.tick_params(axis="y", length=0)
for xc in (0.25, 1.25):
    for ax in (ax1, ax2):
        ax.axvline(xc, color="#777777", lw=0.8, ls=":")
    ax2.text(xc, -0.55, "compression", ha="center", fontsize=11)
for xr in (0.75, 1.75):
    ax2.text(xr, -0.55, "rarefaction", ha="center", fontsize=11)
ax2.set_xlim(0, 2)
ax2.set_xlabel("kz / 2π", fontstyle="italic")
fig.tight_layout()
fig.savefig(OUT, facecolor="white")
print(f"wrote {OUT}")
