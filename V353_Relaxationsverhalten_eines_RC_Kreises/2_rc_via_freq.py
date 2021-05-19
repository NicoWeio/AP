import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

def fit_fn(f, U_0, RC):
    return U_0 / np.sqrt(1 + (2*np.pi*f*RC)**2)

f, U = np.genfromtxt('mess_2.dat', unpack=True)
f *= ureg('Hz')
U *= ureg('V')

f_linspace = np.geomspace(10, f[-1].m, 100_000) * ureg('Hz')

# U_0 sollte eigentlich gemessen und nicht aus dem Fit bestimmt werden.
# So funktioniert's aber auch. :P

U_0_fit, RC_fit = tools.pint_curve_fit(fit_fn, f, U, (ureg('V'), ureg('Ω·F')))

# Ohne Bounds vorzugeben, führt das Quadrieren in der Fit-Funktion dazu,
# dass der Parameter mit Minus zurückgegeben werden kann.
RC_fit = abs(RC_fit)

print(f"{U_0_fit=}")
print(f"{RC_fit.to('ms')=}")

plt.plot(f, U, 'x', label='Messwerte')
plt.plot(f_linspace, fit_fn(f_linspace.m, U_0_fit.m.n, RC_fit.m.n), label='Fit-Funktion')
plt.yscale('log')
plt.xlabel(r'$f \;/\; Hz$')
plt.ylabel(r'$U \;/\; V$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/2_rc_via_freq.pdf')
# plt.show()
