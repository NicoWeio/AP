import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.stats as sp_stats

import tools

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

nr, a, b, c = np.genfromtxt('messwerte_schieblehre.dat', unpack=True)
a *= ureg('mm')
b *= ureg('mm')
c *= ureg('mm')

nr, t_a, t_b, A_a, A_b = np.genfromtxt('messwerte_ultraschall.dat', unpack=True)
t_a *= ureg('µs')
t_b *= ureg('µs')
A_a *= ureg('V')
A_b *= ureg('V')

d_a = (t_a * ureg('2730 m/s')).to('mm')
d_b = (t_b * ureg('2730 m/s')).to('mm')

def fit_fn(d, U_0, α):
    return U_0 * np.exp(-d * α)

# Weil eine verdeckte Auslassung nicht gemessen werden konnte
# (und NaNs hier Probleme bereiten),
# muss sie aus den Daten entfernt werden.
d_merged = tools.pint_concat(a, b) * 2 # hin und zurück
A_merged = tools.pint_concat(A_a, A_b)
d_merged, A_merged = tools.remove_nans(d_merged, A_merged)

# Damit curve_fit nicht auf dumme Gedanken kommt
# (und "RuntimeWarning: overflow encountered in exp" produziert),
# geben wir Startwerte vor.
U_0_guess = max(max(A_a), max(A_b))
print("Erwarte U_0 ≥", U_0_guess)
U_0_fit, α_fit = tools.pint_curve_fit(fit_fn, d_merged, A_merged, (ureg('V'), ureg('1/mm')), p0=(U_0_guess, ureg('20 1/m').to('1/mm')))
print(f"U_0_fit = {U_0_fit}")
print(f"α_fit = {α_fit.to('1/m')}")

d_linspace = np.linspace(min(d_a).m, max(d_a).m) * ureg('mm')
# plt.plot(d_a, A_a, '+', label='Messwerte a')
# plt.plot(d_b, A_b, '+', label='Messwerte b')
plt.plot(d_merged, A_merged, '+', label='Messwerte')
plt.plot(d_linspace, fit_fn(d_linspace.m, U_0_fit.nominal_value, α_fit.nominal_value), label='Fit')
# plt.plot(d_linspace, fit_fn(d_linspace.m, U_0_fit.nominal_value, ureg('21/m').to('1/mm').m), label='Altprotokoll (21/m)')
plt.yscale('log')
plt.xlabel(r'$d \mathbin{/} \si{\milli\meter}$')
plt.ylabel(r'$U_A \mathbin{/} \si{\volt}$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/absorptionskurve.pdf')
# plt.show()
