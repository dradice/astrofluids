"""Velocity field v = (-y, x, 0) of the rotating flow example.

Regenerates figures/fluids-as-continua/velocity-field.svg:
    python3 figures-src/fluids-as-continua/velocity-field.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "fluids-as-continua" / "velocity-field.svg"

plt.rcParams.update({"svg.fonttype": "none", "font.size": 14})

x = np.linspace(-1.5, 1.5, 13)
X, Y = np.meshgrid(x, x)
fig, ax = plt.subplots(figsize=(5.6, 5.0))
ax.quiver(X, Y, -Y, X, color="black", width=0.004)
ax.set_xlim(-1.65, 1.65)
ax.set_ylim(-1.65, 1.65)
ax.set_aspect("equal")
ax.set_xlabel("x", fontstyle="italic")
ax.set_ylabel("y", fontstyle="italic")
ax.set_title("Velocity field")
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, format="svg")
