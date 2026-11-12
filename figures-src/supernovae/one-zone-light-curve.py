"""One-zone supernova light curves (Ch. 3): a red-supergiant explosion, and a compact
(blue-supergiant) explosion with and without radioactive heating.

Integrates the first law for the whole ejecta,
    dE/dt = -E Rdot/R - L + Qdot_heat,   L = E / tau_d,   tau_d = kappa M / (beta c R),
with R = R0 + v t. Heating from 56Ni -> 56Co -> 56Fe
(energy generation rates and lifetimes from Nadyozhin 1994).

Regenerates figures/supernovae/one-zone-light-curve.svg:
    python3 figures-src/supernovae/one-zone-light-curve.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.integrate import solve_ivp  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "figures" / "supernovae" / "one-zone-light-curve.svg"

plt.rcParams.update({
    "svg.fonttype": "none",
    "font.size": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# SI units throughout; the luminosity is converted to erg/s only for the plot.
MSUN, C, DAY, ERG = 1.989e30, 2.998e8, 86400.0, 1e-7
M = 10 * MSUN          # ejecta mass [kg]
R_RSG, R_BSG = 1e12, 3e10   # progenitor radii [m]
V = 3e6                # expansion velocity [m/s]
E0 = 5e50 * ERG        # initial thermal energy [J]
KAPPA, BETA = 0.04, 13.8    # opacity [m^2/kg] (0.4 cm^2/g)
M_NI = 0.07 * MSUN     # mass of 56Ni
EPS_NI, EPS_CO = 3.9e6, 6.78e5      # W kg^-1 (3.9e10, 6.78e9 erg g^-1 s^-1)
TAU_NI, TAU_CO = 8.8 * DAY, 111.3 * DAY


def heating(t):
    return M_NI * (EPS_NI * np.exp(-t / TAU_NI)
                   + EPS_CO * (np.exp(-t / TAU_CO) - np.exp(-t / TAU_NI)))


def rhs(t, y, R0, mni):
    E = y[0]
    R = R0 + V * t
    tau_d = KAPPA * M / (BETA * C * R)
    q = heating(t) if mni else 0.0
    return [-E * V / R - E / tau_d + q]


t = np.linspace(0, 250 * DAY, 2001)
curves = {}
for key, R0, mni in (("rsg", R_RSG, False), ("bsg", R_BSG, False), ("bsg-ni", R_BSG, True)):
    sol = solve_ivp(rhs, (t[0], t[-1]), [E0], t_eval=t, args=(R0, mni), rtol=1e-8, atol=1e23)
    curves[key] = sol.y[0] * BETA * C * (R0 + V * t) / (KAPPA * M) / ERG   # erg/s

fig, ax = plt.subplots(figsize=(7.5, 5.2))
d = t / DAY
ax.plot(d, np.log10(curves["rsg"]), color="#0072B2", lw=2.2, ls="-",
        label="red supergiant, no heating")
ax.plot(d, np.log10(curves["bsg"]), color="#009E73", lw=2.2, ls="-.",
        label="blue supergiant, no heating")
ax.plot(d, np.log10(curves["bsg-ni"]), color="#D55E00", lw=2.2, ls="--",
        label="blue supergiant, 0.07 M⊙ of ⁵⁶Ni")
ax.plot(d[1:], np.log10(heating(t[1:]) / ERG), color="#555555", lw=1.6, ls=":",
        label="radioactive heating rate")
ax.set_xlim(0, 250)
ax.set_ylim(39.5, 42.9)
ax.set_xlabel("time since explosion [days]")
ax.set_ylabel("log₁₀ L  [erg s⁻¹]")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=12)
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, facecolor="white")
print(f"wrote {OUT}")
for key, L in curves.items():
    i = np.argmax(L[d > 5]) + np.sum(d <= 5)
    print(key, "max after day 5:", round(d[i]), "d, log L =", round(np.log10(L[i]), 2))
