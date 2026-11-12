#!/usr/bin/env python3
"""Single source of truth for the book's chapter list.

Each entry: (slug, key, title, status)
  slug   file name in chapters/ (or appendices/) without .qmd; never renamed
  key    short prefix for labels: #sec-<key>, #eq-<key>-..., #exr-<key>-...
  title  chapter title
  status "port" | "port+" | "new"

Usage:
  python3 tools/chapters.py stubs   create missing chapter stubs (never overwrites)
  python3 tools/chapters.py yaml    print the book.chapters block for _quarto.yml
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PARTS = [
    ("Foundations", [
        ("fluids-as-continua", "continua", "Fluids as Continua", "port"),
        ("thermodynamics", "thermo", "Thermodynamics Refresher", "port"),
        ("supernovae", "sn", "Supernovae", "port"),
        ("euler-equation", "euler", "The Euler Equation", "port"),
        ("eulerian-lagrangian", "lagrange", "Eulerian and Lagrangian Descriptions", "port"),
        ("conservation-laws", "conserv", "Conservation Laws", "port"),
        ("gravitational-potential", "grav", "The Gravitational Potential", "new"),
        ("hydrostatic-equilibrium", "hydro", "Hydrostatic Equilibrium and the Virial Theorem", "port+"),
    ]),
    ("Waves, Shocks, and Outflows", [
        ("sound-waves", "sound", "Sound Waves and the Doppler Effect", "port+"),
        ("stratified-atmospheres", "strat", "Waves in Stratified Atmospheres", "port+"),
        ("shock-waves", "shock", "Shock Waves", "new"),
        ("blast-waves", "blast", "Blast Waves", "new"),
        ("winds-and-accretion", "wind", "Stellar Winds and Spherical Accretion", "new"),
    ]),
    ("Instabilities, Viscosity, Disks, and Turbulence", [
        ("instabilities-convection", "conv", "Fluid Instabilities I: Convection", "new"),
        ("instabilities-rt-kh", "rtkh", "Fluid Instabilities II: Rayleigh–Taylor and Kelvin–Helmholtz", "new"),
        ("instabilities-thermal-gravitational", "tginst", "Fluid Instabilities III: Thermal and Gravitational Instabilities", "new"),
        ("viscous-flows", "visc", "Diffusion and Viscous Flows", "new"),
        ("accretion-disks-structure", "disk", "Accretion Disks I: Structure and Viscous Evolution", "new"),
        ("accretion-disks-spectra", "diskspec", "Accretion Disks II: Steady Disks and Spectra", "new"),
        ("turbulence", "turb", "Turbulence", "port"),
    ]),
    ("Plasma and Magnetohydrodynamics", [
        ("plasma", "plasma", "Introduction to Plasma", "port"),
        ("mhd-equations", "mhd", "The MHD Equations", "port"),
        ("flux-freezing", "flux", "Flux Freezing", "port"),
        ("magnetic-tension", "tension", "Magnetic Tension and Hydromagnetic Equilibria", "port"),
        ("mhd-waves", "mhdwaves", "MHD Waves", "port"),
        ("mri", "mri", "The Magnetorotational Instability", "port"),
    ]),
]

APPENDICES = [
    ("vector-calculus", "vec", "Vector Calculus", "new"),
]

NOTE = {
    "port": "This chapter is being ported from the 2025 lecture notes.",
    "port+": "This chapter is being ported from the 2025 lecture notes and expanded.",
    "new": "This chapter is in preparation.",
}


def stub(key, title, status):
    return (
        f"# {title} {{#sec-{key}}}\n\n"
        "::: {.callout-note}\n"
        f"{NOTE[status]}\n"
        ":::\n"
    )


def make_stubs():
    made = 0
    entries = [("chapters", c) for _, cs in PARTS for c in cs]
    entries += [("appendices", a) for a in APPENDICES]
    for folder, (slug, key, title, status) in entries:
        path = ROOT / folder / f"{slug}.qmd"
        if not path.exists():
            path.write_text(stub(key, title, status), encoding="utf-8")
            made += 1
    print(f"created {made} stub(s)")


def print_yaml():
    lines = ["  chapters:", "    - index.qmd"]
    for part, cs in PARTS:
        lines.append(f'    - part: "{part}"')
        lines.append("      chapters:")
        lines += [f"        - chapters/{slug}.qmd" for slug, *_ in cs]
    lines.append("  appendices:")
    lines += [f"    - appendices/{slug}.qmd" for slug, *_ in APPENDICES]
    print("\n".join(lines))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "stubs":
        make_stubs()
    elif cmd == "yaml":
        print_yaml()
    else:
        sys.exit(__doc__)
