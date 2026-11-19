#!/usr/bin/env python3
"""Figures of Ch. 16 (Accretion disks).

Regenerates, in figures/accretion-disks/:
    vertical-gravity.svg   sketch for the solution of Exercise 16.1, redrawn from the 2025 drawing
    spreading-ring.svg     viscous spreading of a ring (Lynden-Bell & Pringle 1974 solution)
    steady-disk.svg        surface density and effective temperature of a steady disk
    disk-spectrum.svg      spectrum of a steady disk, replaces Pringle (1981) on the 2023 slides
    3c273-sed.svg          NED photometry of 3C 273 (data in 3c273-ned.txt) compared with a
                           steady disk around a 10^9 M_sun black hole

Usage: python3 figures-src/accretion-disks/make-figures.py   (from the notes/ directory)
The plot figure of Exercise 16.3 is made by solutions/code/accretion-disks/accretion-disk.py.
"""
import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy.special import ive  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from svgkit import *  # noqa: E402,F403

OUT = Path(__file__).resolve().parent.parent.parent / "figures" / "accretion-disks"


def vertical_gravity():
    s = Svg(400, 220, "Vertical component of the gravitational acceleration in a disk",
            "A right triangle with a horizontal leg of length R along the disk midplane, a vertical "
            "leg of height z, and the hypotenuse of length r pointing to the central object at the "
            "left. A fluid element, drawn as a small square at the top of the vertical leg, feels the "
            "gravitational acceleration g directed along the hypotenuse towards the central object; "
            "its vertical component g_z points down.", "vertgrav")
    A, B, C = (50, 180), (320, 180), (320, 95)
    s.line(*A, *B)
    s.line(*B, *C)
    s.line(*A, *C)
    s.rect(C[0] - 17, C[1] - 17, 34, 34, stroke="#000", sw=2.4)
    # g: from the element towards the central object, along the hypotenuse
    ux, uy = (A[0] - C[0]), (A[1] - C[1])
    n = (ux * ux + uy * uy) ** 0.5
    s.line(C[0], C[1], C[0] + 130 * ux / n, C[1] + 130 * uy / n, w=2.6, head=True)
    s.line(C[0], C[1], C[0], C[1] + 52, w=2.6, head=True)
    s.text(245, 98, "g", anchor="middle", bold=True, italic=False)
    s.text(296, 145, "g_z", anchor="middle")
    s.text(335, 145, "z")
    s.text(170, 134, "r", anchor="middle")
    s.text(185, 207, "R", anchor="middle")
    s.save(OUT / "vertical-gravity.svg")


plt.rcParams.update({
    "svg.fonttype": "none",
    "svg.hashsalt": "disk",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

COLORS = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00"]
STYLES = ["-", "--", "-.", ":", (0, (5, 1, 1, 1, 1, 1))]


def save(fig, name):
    """Save a matplotlib figure, turning "_ab" in text labels into SVG subscripts (and ν^(1/3))."""
    path = OUT / name
    fig.savefig(path, facecolor="white")
    plt.close(fig)
    svg = path.read_text()
    svg = re.sub(r"(<text[^>]*>)([^<]*)(</text>)",
                 lambda m: m.group(1) + re.sub(r"_([A-Za-z0-9ν*⊙]+)",
                                               r'<tspan baseline-shift="sub" font-size="75%">\1</tspan>',
                                               m.group(2)) + m.group(3), svg)
    svg = svg.replace("ν^(1/3)", 'ν<tspan baseline-shift="super" font-size="75%">1/3</tspan>')
    path.write_text(svg)


def ring_sigma(x, tau):
    """pi R_0^2 Sigma / m for a ring of mass m released at R_0 (x = R/R_0, tau = 12 nu t/R_0^2)."""
    z = 2 * x / tau
    return x**-0.25 / tau * np.exp(-(1 + x * x) / tau + z) * ive(0.25, z)


def spreading_ring():
    x = np.linspace(1e-3, 2.5, 1000)
    fig, ax = plt.subplots(figsize=(7, 3.8))
    for i, tau in enumerate([0.008, 0.032, 0.128, 0.512]):
        ax.plot(x, ring_sigma(x, tau), color=COLORS[i], ls=STYLES[i], lw=2, label=f"τ = {tau}")
    ax.set_xlim(0, 2.5)
    ax.set_ylim(0, 3.5)
    ax.set_xlabel("x = R / R_0", fontstyle="italic")
    ax.set_ylabel("π R_0² Σ / m", fontstyle="italic")
    ax.legend(frameon=False)
    fig.tight_layout()
    save(fig, "spreading-ring.svg")


def steady_disk():
    r = np.logspace(0, 2, 600)
    f = 1 - r**-0.5
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.semilogx(r, f, color=COLORS[0], lw=2, label="3πνΣ / Ṁ")
    ax.semilogx(r, (f / r**3) ** 0.25, color=COLORS[1], ls="--", lw=2, label="T_eff / T_*")
    ax.set_xlim(1, 100)
    ax.set_ylim(0, 1)
    ax.set_xlabel("R / R_*", fontstyle="italic")
    ax.legend(frameon=False, loc="center right")
    fig.tight_layout()
    save(fig, "steady-disk.svg")


def disk_spectrum():
    rout = 1e4
    r = np.logspace(0, np.log10(rout), 4000)[1:]
    teff = (r**-3 * (1 - r**-0.5)) ** 0.25          # T_eff / T_*
    x = np.logspace(-5.5, 1.3, 400)                    # h nu / k_B T_*
    arg = x[:, None] / teff[None, :]
    bnu = x[:, None] ** 3 / np.expm1(np.minimum(arg, 700))
    fnu = np.trapezoid(bnu * r**2, np.log(r), axis=1)  # int B_nu R dR = int B_nu R^2 dln R
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.loglog(x, fnu, color="black", lw=2)
    tout = teff[-1]
    # guide lines through the computed spectrum
    i2 = np.searchsorted(x, 0.03 * tout)
    i13 = np.searchsorted(x, 3e-3)
    xs = np.array([x[0], 3 * tout])
    ax.loglog(xs, fnu[i2] * (xs / x[i2]) ** 2, color=COLORS[0], ls="--", lw=1.5)
    xs = np.array([3 * tout, 0.3])
    ax.loglog(xs, fnu[i13] * (xs / x[i13]) ** (1 / 3), color=COLORS[1], ls="-.", lw=1.5)
    ax.text(2e-5, fnu[i2] * (2e-5 / x[i2]) ** 2 * 6, "ν²", fontsize=13, color=COLORS[0])
    ax.text(3e-3, fnu[i13] * 3.0, "ν^(1/3)", fontsize=13, color=COLORS[1])
    ax.text(3.0, fnu.max() * 0.3, "Wien\ncutoff", fontsize=11)
    for xv, lab in [(tout, "k_B T_out"), (1.0, "k_B T_*")]:
        ax.axvline(xv, color="#777777", lw=0.8, ls=":")
        ax.text(xv * 1.15, fnu.max() * 1e-6, lab, fontsize=11, rotation=90, va="bottom")
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(fnu.max() * 1e-7, fnu.max() * 5)
    ax.set_xlabel("h ν / k_B T_*", fontstyle="italic")
    ax.set_ylabel("F_ν (arbitrary units)", fontstyle="italic")
    fig.tight_layout()
    save(fig, "disk-spectrum.svg")


def sed_3c273(mbh=1e9, mdot_yr=5.0, rout=1e3, z=0.158, dl_mpc=755.0, dbin=0.25, cosi=1.0):
    """NED photometry of 3C 273 against the spectrum of a steady disk.

    The data are isotropic-equivalent luminosities, 4 pi d_L^2 F_nu, so the model is plotted in the
    same way: from Eq. (disk-spectrum), 4 pi d^2 F_nu = 8 pi^2 cos(i) int B_nu R dR (3C 273 is seen
    nearly face on, cos i = 1). This is 2 cos(i) times the true L_nu = 4 pi^2 int B_nu R dR.

    The luminosity distance is for z = 0.158, H_0 = 70 km/s/Mpc, Omega_m = 0.3, flat.
    The data are binned in log10(nu) with width dbin (dex).
    """
    G, c, h, kB, sig = 6.674e-11, 2.998e8, 6.626e-34, 1.381e-23, 5.670e-8
    msun, yr, mpc = 1.989e30, 3.156e7, 3.086e22
    M = mbh * msun
    mdot = mdot_yr * msun / yr
    rin = 6 * G * M / c**2
    tstar = (3 * G * M * mdot / (8 * np.pi * sig * rin**3)) ** 0.25
    r = rin * np.logspace(0, np.log10(rout), 3000)[1:]
    teff = tstar * ((rin / r) ** 3 * (1 - (rin / r) ** 0.5)) ** 0.25
    lognu = np.linspace(12, 17, 500)
    nu = 10**lognu
    arg = np.minimum(h * nu[:, None] / (kB * teff[None, :]), 700)
    bnu = 2 * h * nu[:, None] ** 3 / c**2 / np.expm1(arg)
    lnu = 4 * np.pi**2 * np.trapezoid(bnu * r**2, np.log(r), axis=1)   # true L_nu
    lum = np.trapezoid(lnu, nu)
    lnu_iso = 2 * cosi * lnu                                            # 4 pi d^2 F_nu
    print(f"sed_3c273: T_* = {tstar:.3g} K, L = {lum:.3g} W (GM Mdot/2R_* = {G * M * mdot / (2 * rin):.3g} W)")

    # observed frequency (Hz), flux density (Jy) -> rest frequency, nu L_nu (W)
    data = np.genfromtxt(Path(__file__).resolve().parent / "3c273-ned.txt", usecols=(0, 1))
    refs = np.genfromtxt(Path(__file__).resolve().parent / "3c273-ned.txt", usecols=2, dtype=str)
    # The Chandra Source Catalog entries (refcode 2020CSC...) are 1.5-3.5 dex below all other X-ray
    # measurements: probably the piled-up core and the X-ray knots of the jet. A few other outliers
    # (two Chandra and two optical V points, about 1-2 dex off) are left in: the bin medians reject them.
    data = data[~np.char.startswith(refs, "2020CSC")]
    dl = dl_mpc * mpc
    nurest = data[:, 0] * (1 + z)
    nulnu = 4 * np.pi * dl**2 * data[:, 0] * data[:, 1] * 1e-26
    fig, ax = plt.subplots(figsize=(7, 4))
    # bin in log(nu): median, with error bars from the 16th to the 84th percentile
    x, y = np.log10(nurest), np.log10(nulnu)
    edges = np.arange(9.0, 20.01, dbin)
    idx = np.digitize(x, edges)
    xb, yb, lo, hi = [], [], [], []
    for k in np.unique(idx):
        sel = idx == k
        if not (0 < k < len(edges)):
            continue
        xb.append(np.median(x[sel]))
        yb.append(np.median(y[sel]))
        lo.append(yb[-1] - np.percentile(y[sel], 16))
        hi.append(np.percentile(y[sel], 84) - yb[-1])
    ax.errorbar(xb, yb, yerr=[lo, hi], fmt="o", ms=5, color=COLORS[0], ecolor=COLORS[0],
                elinewidth=1.2, capsize=2.5, label="3C 273 (NED), binned")
    ax.plot(lognu, np.log10(np.maximum(nu * lnu_iso, 1e-30)), color=COLORS[1], ls="--", lw=2,
            label="steady disk, 10⁹ M_⊙")
    for x, lab in [(10.0, "radio"), (13.0, "IR"), (14.6, "optical"), (15.7, "UV"), (18.0, "X-rays")]:
        ax.text(x, 40.25, lab, ha="center", fontsize=11, color="#555555")
    # components of the spectrum (see the text of Ch. 16)
    for x, yy, lab in [(10.6, 38.35, "jet"), (13.6, 39.25, "hot dust"), (15.1, 37.4, "disk"),
                       (18.2, 39.4, "corona + jet")]:
        ax.text(x, yy, lab, ha="center", fontsize=12, fontstyle="italic", color="#333333")
    ax.set_xlim(9, 20)
    ax.set_ylim(36, 40.6)
    ax.set_xlabel("log₁₀(ν / Hz), rest frame", fontstyle="italic")
    ax.set_ylabel("log₁₀(ν L_ν / W)", fontstyle="italic")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(0.0, 0.92))
    fig.tight_layout()
    save(fig, "3c273-sed.svg")


if __name__ == "__main__":
    vertical_gravity()
    spreading_ring()
    steady_disk()
    disk_spectrum()
    sed_3c273()
    print(f"wrote figures to {OUT}")
