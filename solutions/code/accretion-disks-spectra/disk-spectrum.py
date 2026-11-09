import matplotlib.pyplot as plt
import numpy as np


def black_body(nu, T):
    """
    Returns a black body spectrum at a given temperature

    Input
    nu : array
         frequency (or frequencies) at which to evaluate the spectrum
    T : float
        blackbody temperature
    """
    return nu**3 / (np.exp(nu / T) - 1)


def plot_single_ring():
    # Frequency bins
    nu = 10.0 ** np.linspace(-2, 2.5, 100)
    # Radii to plot
    R = np.array([1.0, 2.0, 4.0, 8.0, 16.0])
    T = R ** (-3 / 4)

    plt.figure()
    ax = plt.axes()
    for i in range(R.shape[0]):
        F_nu = black_body(nu, T[i]) * R[i]
        ax.plot(nu, F_nu / F_nu.max(), label=f"$R/R_{{\\rm in}} = {R[i]:.2f}$")
    ax.set_xlim(1e-2, 300)
    ax.set_ylim(1e-4, 2)
    ax.set_xlabel("$h \\nu / k T$")
    ax.set_ylabel(r"Normalized flux")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    plt.savefig("disk-spectrum-fig1.png", bbox_inches="tight")


def plot_overall_spectrum():
    # Frequency bins
    nu = 10.0 ** np.linspace(-4, 4, 200)
    # Disk grid
    R = np.linspace(1.0, 200.0, 199)

    # Spectrum
    F_nu = np.zeros_like(nu)
    for i in range(R.shape[0]):
        F_nu += black_body(nu, R[i] ** (-3 / 4)) * R[i]
    F_nu = F_nu / np.max(F_nu)

    # Spectrum between the T_in and T_out
    F_nu_ex = nu ** (1 / 3)

    # Plot results
    plt.figure()
    ax = plt.axes()
    ax.loglog(nu, F_nu, "b-", label=r"$F_\nu$")
    ax.loglog(nu, F_nu_ex, "k--", label=r"$\nu^{1/3}$")
    ax.axvline(R[-1] ** (-3 / 4), color="r", linestyle="--", label=r"$T_{\rm out}$")
    ax.axvline(1.0, color="g", linestyle="--", label=r"$T_{\rm in}$")
    ax.legend()
    ax.set_xlim(1e-3, 100)
    ax.set_ylim(1e-4, 2)
    ax.set_xlabel("$h \\nu / k T$")
    ax.set_ylabel(r"Normalized flux")
    plt.savefig("disk-spectrum-fig2.png", bbox_inches="tight")


if __name__ == "__main__":
    plot_single_ring()
    plot_overall_spectrum()
