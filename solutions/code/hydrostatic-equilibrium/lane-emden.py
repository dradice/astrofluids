import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def lane_emden(n, Rmax=10):
    """Solves the Lane-Emden equations using `solve_ivp`"""

    def rhs(t, y):
        if t > 0:
            return [y[1], -2 * y[1] / t - np.abs(y[0]) ** n]
        else:
            # limit xi -> 0: theta ~ 1 - xi^2/6, so 2 phi / xi -> -2/3 and phi' -> -theta^n / 3
            return [y[1], -np.abs(y[0]) ** n / 3]

    def surface(t, y):
        return y[0]

    surface.terminal = True
    surface.direction = -1
    return solve_ivp(
        rhs, [0, Rmax], [1.0, 0.0], events=surface, dense_output=True, rtol=1e-10, atol=1e-12
    )


# Analytic solutions to Lane-Emden equations for special values of n
analytic = {
    0.0: lambda x: 1.0 - 1.0 / 6.0 * x**2,
    1.0: lambda x: np.sin(x + 1e-15) / (x + 1e-15),
    5.0: lambda x: 1.0 / np.sqrt(1 + 1.0 / 3.0 * x**2),
}


for n in [0.0, 1.0, 1.5, 5.0]:
    sol = lane_emden(n)
    try:
        R = float(sol.t_events[0][0])
        print(f"n = {n}", f"R = {R}")
    except:
        R = sol.t[-1]
        print(f"n = {n}", f"R = oo")
    xi = np.linspace(0, R, 100)
    theta = sol.sol(xi)[0]

    plt.figure()
    plt.title(f"Lane-Emden n = {n}")
    plt.xlabel(r"$\xi$")
    plt.ylabel(r"$\theta$")
    plt.plot(xi, theta, linewidth=2, label="Numerical Solution")
    if n in analytic:
        plt.plot(xi, analytic[n](xi), linewidth=1.0, label="Analytical Solution")
    plt.legend()

plt.show()
