"""Figures for Ch. 15 (Diffusion and viscous flows), redrawn from the 2023 slides.

Regenerates, in figures/viscous-flows/:
    random-walk-paths.svg     sample random walks and the envelope x = ±sqrt(n) h
    fundamental-solution.svg  fundamental solution of the diffusion equation, D = 1

    python3 figures-src/viscous-flows/make-figures.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "viscous-flows"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "svg.fonttype": "none",
    "svg.hashsalt": "visc",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00"]
STYLES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1, 1, 1))]


def random_walk_paths():
    rng = np.random.default_rng(442)
    nsteps = 1000
    n = np.arange(nsteps + 1)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for i in range(5):
        steps = rng.choice([-1, 1], size=nsteps)
        x = np.concatenate([[0], np.cumsum(steps)])
        ax.plot(n, x, color=COLORS[i], lw=1.1, ls=STYLES[i])
    env = np.sqrt(n)
    ax.plot(n, env, color="black", lw=2)
    ax.plot(n, -env, color="black", lw=2)
    ax.text(1005, env[-1], "+√n", va="center", fontsize=12)
    ax.text(1005, -env[-1], "−√n", va="center", fontsize=12)
    ax.axhline(0, color="#777777", lw=0.8)
    ax.set_xlim(0, 1000)
    ax.set_xlabel("number of steps n", fontstyle="italic")
    ax.set_ylabel("x / h", fontstyle="italic")
    fig.tight_layout()
    fig.savefig(OUT / "random-walk-paths.svg", facecolor="white")
    plt.close(fig)


def fundamental_solution():
    x = np.linspace(-6, 6, 600)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for i, t in enumerate([1, 2, 4, 16]):
        gam = np.exp(-x**2 / (4 * t)) / np.sqrt(4 * np.pi * t)
        ax.plot(x, gam, color=COLORS[i], ls=STYLES[i], lw=2, label=f"t = {t}")
    ax.set_xlim(-6, 6)
    ax.set_ylim(0, 0.3)
    ax.set_xlabel("x", fontstyle="italic")
    ax.set_ylabel("Γ(t, x)", fontstyle="italic")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "fundamental-solution.svg", facecolor="white")
    plt.close(fig)


random_walk_paths()
fundamental_solution()
print(f"wrote figures to {OUT}")
