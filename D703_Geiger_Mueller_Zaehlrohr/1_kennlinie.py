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

U, N = np.genfromtxt('Kennlinie.dat', unpack=True)
U *= ureg('V')

t = ureg('60s') # Integrationszeit pro Zählrohrspannung
deltaI = ureg('0.05 µA') # Ablesegenauigkeit am Amperemeter
deltaN = np.sqrt(N)

N_per_t = N/t
N_per_t_err = np.sqrt(N/t)

plateau_bound_indices = (5, 32)
plateau_bounds = tuple(U[i] for i in plateau_bound_indices)

U_b = U[plateau_bound_indices[0] : plateau_bound_indices[1]+1]
N_per_t_b = N_per_t[plateau_bound_indices[0] : plateau_bound_indices[1]+1]

slope, intercept, r_value, p_value, std_err = sp_stats.linregress(U_b.m, N_per_t_b)
slope *= ureg('(1/s)/V')
std_err *= ureg('(1/s)/V')
intercept *= ureg('1/s')

U_linspace = np.array([U[0].m, U[-1].m]) * ureg('V') # kein richtiger „linspace“ nötig…
N_regress = slope * U_linspace + intercept
# N_regress_u = ufloat(slope.m, std_err)* ureg('(1/s)/V') * U_linspace + intercept

print(f"Plateau-Start/Ende: {plateau_bounds}")
print(f"Plateaulänge: {U_b[-1] - U_b[0]}")
print(f"Plateauanstieg: {slope.to('(1/s)/V')} ± {std_err.to('(1/s)/V')}")
print(f"Plateauanstieg: {slope.to('(1/s)/kV')} ± {std_err.to('(1/s)/kV')}")

plt.axvline(x=plateau_bounds[0], linewidth=0.5, linestyle="--", color='grey')
plt.axvline(x=plateau_bounds[1], linewidth=0.5, linestyle="--", color='grey')

plt.errorbar(U.to('V'), N_per_t.to('1/s').m, fmt='x', yerr=N_per_t_err.m, label='Messwerte')
plt.plot(U_linspace.to('V'), N_regress.to('1/s'), label="Ausgleichsgerade")
plt.xlabel(r"$U \mathbin{/} \si{\volt}$")
plt.ylabel(r"$N \mathbin{/} \si{\per\second}$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('build/plot1.pdf')
# plt.show()
