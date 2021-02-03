import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
# import generate_table

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools
NU_mean = __import__('1_untergrundrate').untergrundrate(ureg)

t, N = np.genfromtxt('Vanadium.dat', unpack=True)
N = unp.uarray(N, np.sqrt(N))
t *= ureg('s')
N /= ureg('30 s')

N -= NU_mean # Nulleffekt abziehen

def fit_fn(t, N0, λ):
    return N0 * np.exp(-λ*t)

def fit(t, N):
    (N0_fit, λ_fit) = tools.curve_fit(fit_fn, unp.nominal_values(t.to('s')), unp.nominal_values(N.to('1/s')), p0=param_guesses)
    λ_fit *= ureg('1/s')
    T_hw = np.log(2) / λ_fit # Halbwertszeit
    print(f"{N0_fit=}, {λ_fit=}, {T_hw=}")
    return N0_fit, λ_fit, T_hw

param_guesses = [N[0].n, (np.log((N[0]/N[-1]).n)/t[-1]).m]
N0_fit, λ_fit, T_hw = fit(t, N)

double_hw_index = next(i for i,t in enumerate(t) if t > T_hw)
N0_fit_2, λ_fit_2, T_hw_2 = fit(t[double_hw_index :], N[double_hw_index :])

t_linspace = np.linspace(0, t[-1])

plt.axvline(x=(T_hw.n), linewidth=0.5, linestyle="--", color='grey')
plt.axvline(x=(2*T_hw.n), linewidth=0.5, linestyle="--", color='grey')

plt.errorbar(t.to('s'), unp.nominal_values(N.to('1/s')), fmt='x', yerr=unp.std_devs(N), label='Messwerte')
plt.plot(t_linspace, fit_fn(unp.nominal_values(t_linspace), unp.nominal_values(N0_fit), unp.nominal_values(λ_fit)), label="Fit-Funktion")
plt.plot(t_linspace, fit_fn(unp.nominal_values(t_linspace), unp.nominal_values(N0_fit_2), unp.nominal_values(λ_fit_2)), label="Fit-Funktion 2")
plt.xlabel(r"$t \;/\; s$")
plt.ylabel(r"$N \;/\; \frac{1}{s}$")
plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot1_log.pdf')
# plt.show()

plt.yscale('linear')
plt.tight_layout()
plt.savefig('build/plot1_lin.pdf')
# plt.show()
