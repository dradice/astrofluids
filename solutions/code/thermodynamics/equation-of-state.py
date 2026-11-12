import matplotlib.pyplot as plt
import numpy as np


class StellarMatter:
    def __init__(self, X_H=0.7, X_He=0.3):
        from astropy.constants import k_B, c, sigma_sb, m_p, u

        self.X_H = X_H
        self.X_He = X_He
        # SI units: rho in kg m^-3, T in K, p in Pa
        self.k_B = k_B.si.value
        self.a_rad = (4 * sigma_sb / c).si.value
        self.m_H = m_p.si.value
        self.m_He = 4 * u.si.value

    def get_densities(self, rho, temp):
        n_H = rho * (self.X_H / self.m_H)
        n_He = rho * (self.X_He / self.m_He)
        n_e = n_H + 2 * n_He
        print(rho, n_e)
        return n_H, n_He, n_e

    def get_pressures(self, rho, temp):
        n_H, n_He, n_e = self.get_densities(rho, temp)
        p_ions = (n_H + n_He) * self.k_B * temp
        p_e = n_e * self.k_B * temp
        p_rad = (1.0 / 3.0) * self.a_rad * temp**4
        return p_ions, p_e, p_rad

if __name__ == "__main__":
    eos = StellarMatter()

    rho = 150e3  # 150 g cm^-3
    temp = 10.0**np.linspace(1, 10, 100)
    p_ions, p_e, p_rad = eos.get_pressures(rho, temp)
    plt.figure()
    plt.title(r"$\rho = 150\ {\rm g}\ {\rm cm}^{-3}$")
    plt.loglog(temp, p_ions, label=r"$p_{\rm ions}$")
    plt.loglog(temp, p_e, label=r"$p_{\rm e}$")
    plt.loglog(temp, p_rad, label=r"$p_{\rm rad}$")
    plt.xlabel(r"$T\ [{\rm K}]$")
    plt.ylabel(r"$p\ [{\rm Pa}]$")
    plt.legend()

    rho = 1e-21  # 1e-24 g cm^-3
    temp = 10.0**np.linspace(-3, 3, 100)
    p_ions, p_e, p_rad = eos.get_pressures(rho, temp)
    plt.figure()
    plt.title(r"$\rho = 10^{-24}\ {\rm g}\ {\rm cm}^{-3}$")
    plt.loglog(temp, p_ions, label=r"$p_{\rm ions}$")
    plt.loglog(temp, p_e, label=r"$p_{\rm e}$")
    plt.loglog(temp, p_rad, label=r"$p_{\rm rad}$")
    plt.xlabel(r"$T\ [{\rm K}]$")
    plt.ylabel(r"$p\ [{\rm Pa}]$")
    plt.legend()

    plt.show()
