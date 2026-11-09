#!/usr/bin/env python3
"""Plot of the blast-wave radius versus time (data in fireball.dat)."""

import matplotlib.pyplot as plt
import numpy as np

dset = np.loadtxt("fireball.dat", unpack=True)

plt.figure(figsize=(8, 4))
plt.plot(dset[0], dset[1], "ko")

plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"$t\ ({\rm ms})$")
plt.ylabel(r"$R\ ({\rm m})$")
plt.grid(which="both")

plt.xlim(0.07, 1.2)
plt.ylim(15, 120)

plt.savefig("fireball.pdf", bbox_inches="tight")
