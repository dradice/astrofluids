from math import pi, sqrt
import matplotlib.pyplot as plt
import numpy as np

class RandomWalk:
    """
    Class representing an ensamble of random walks
    """
    def __init__(self, nwalkers, type="brownian"):
        """
        Initializes the random walks

        Parameters
        ----------
        nwalkers: int
                  number of walkers
        type: "brownian" or "levy"
              type of random walk
        """
        assert (type in ["brownian", "levy"])
        self.type = type
        self.xp = np.zeros((3, nwalkers))
        self.R = []

    def step(self):
        """
        Makes a step of the random walks and accumulate statistics
        """
        mu = np.random.uniform(-1.0, 1.0, self.xp.shape[1])
        phi = np.random.uniform(0, 2*pi, self.xp.shape[1])
        if self.type == "brownian":
            dR = np.ones_like(self.xp[0])
        else:
            dR = np.random.pareto(2/3, self.xp.shape[1])
        self.xp[0] += dR * np.cos(phi) * np.sqrt(1 - mu**2)
        self.xp[1] += dR * np.sin(phi) * np.sqrt(1 - mu**2)
        self.xp[2] += dR * mu 

        R2 = self.xp[0]**2 + self.xp[1]**2 + self.xp[2]**2
        self.R.append(np.median(np.sqrt(R2)))

if __name__ == '__main__':
    NWALKERS = 1000
    NSTEPS = 10000

    N = np.arange(1, NSTEPS+1)

    rwb = RandomWalk(NWALKERS, type="brownian")
    xp, yp, zp = [], [], []
    for i in range(NSTEPS):
        rwb.step()
        xp.append(rwb.xp[0,0])
        yp.append(rwb.xp[1,0])
        zp.append(rwb.xp[2,0])

    plt.figure()
    plt.title("Brownian Random Walk")
    plt.plot(xp, yp, 'b-')

    rwl = RandomWalk(NWALKERS, type="levy")
    xp, yp, zp = [], [], []
    for i in range(NSTEPS):
        rwl.step()
        xp.append(rwl.xp[0,0])
        yp.append(rwl.xp[1,0])
        zp.append(rwl.xp[2,0])

    plt.figure()
    plt.title("Lévy Flights")
    plt.plot(np.array(xp)/xp[0], np.array(yp)/yp[0], 'b-')

    plt.figure()
    plt.loglog(N, np.array(rwb.R)/rwb.R[0], "r", label="Brownian")
    plt.loglog(N, np.array(rwl.R)/rwl.R[0], "b", label="Levy")
    plt.loglog(N, N**(1/2), 'k--', label=r"$t^{1/2}$")
    plt.loglog(N, N**(3/2), 'k:', label=r"$t^{3/2}$")
    plt.xlabel(r"$t$")
    plt.ylabel(r"$\langle R \rangle$")
    plt.legend()
    plt.show()
