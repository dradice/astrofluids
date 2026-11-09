import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from scipy.linalg import solve_banded

plt.rcParams.update({"svg.fonttype": "none", "font.size": 14})


class AccretionDisk:
    """
    A class solving the equation for the viscous spreading of an accretion disk:

        dS/dt = d^2(S X^-2)/dX^2

    This class uses 2nd order finite differencing in space and 1st order
    backward-Euler integration in time.
    """

    def __init__(self, X_min: float, X_max: float, NX: int):
        """
        Initialize the disk grid
        """
        self.X = np.linspace(X_min, X_max, NX + 1)
        self.DX = self.X[1] - self.X[0]

        # Assemble banded matrix (see solve_banded documentation for the fmt)
        self.A = np.zeros((3, NX - 1))

        # Maps matrix indices i,j into indices for ab
        index_map = lambda i, j: (1 + i - j, j)

        # First row
        self.A[index_map(0, 0)] = -2 * self.X[1] ** (-2)
        self.A[index_map(0, 1)] = self.X[2] ** (-2)
        # Middle rows
        for r in range(1, NX - 2):
            self.A[index_map(r, r - 1)] = self.X[r] ** (-2)
            self.A[index_map(r, r)] = -2 * self.X[r + 1] ** (-2)
            self.A[index_map(r, r + 1)] = self.X[r + 2] ** (-2)
        # Last row
        self.A[index_map(NX - 2, NX - 2)] = -2 * self.X[NX - 1] ** (-2)
        self.A[index_map(NX - 2, NX - 3)] = self.X[NX - 2] ** (-2)

    def step(self, Sn:np.ndarray, DT:float):
        """
        steps the solution forward in time by one timestep

        parameters
        ----------
        sn : (nx - 1) array
             solution at the beginning of the timestep (excluding boundary data)
        dt : float
             timestep

        returns
        -------
        snew : (nx - 1) array
               solution at the end of the timestep (excluding boundary data)
        """
        # Assemble the matrix to invert
        self.ab = -(DT / self.DX**2) * self.A

        index_map = lambda i, j: (1 + i - j, j)

        for r in range(0, self.ab.shape[1]):
            self.ab[index_map(r, r)] += 1.0

        return solve_banded((1, 1), self.ab, Sn)


if __name__ == "__main__":
    # Setup the simulation
    X_min = 1.0
    X_max = 100.0
    NX = 1024
    T_max = 1000.0
    disk = AccretionDisk(X_min, X_max, NX)

    # Create initial data
    X = disk.X
    S0 = np.exp(-(X-10)**2)
    S0[0] = S0[-1] = 0.0

    # State vector
    S = S0.copy()

    # Prepare plotting
    cmap = cm.turbo
    norm = mcolors.Normalize(vmin=0.0, vmax=T_max)
    plt.loglog(disk.X, S, color=cmap(norm(0.0)))

    # Counters for the time integration
    istep = 0
    T = 0
    DT = 1
    while T < T_max:
        S[1:-1] = disk.step(S[1:-1], DT)
        T += DT
        istep += 1
        if istep % 10 == 0:
            plt.loglog(disk.X, S, color=cmap(norm(T)))

    # Final touches for the plot
    plt.ylim(1e-4, 1)
    plt.xlabel(r"$X$")
    plt.ylabel(r"$S$")

    # Add a colorbar
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # Dummy array for colorbar
    cbar = plt.colorbar(sm, ax=plt.gca())
    cbar.set_label("$T$")

    # Save figure
    # Usage: python3 accretion-disk.py [output-file]
    out = sys.argv[1] if len(sys.argv) > 1 else "accretion-disk-plot.svg"
    plt.savefig(out, bbox_inches="tight")


