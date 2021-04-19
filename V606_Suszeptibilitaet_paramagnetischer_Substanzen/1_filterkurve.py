import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.stats as sp_stats

import tools

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

ν, U_A = np.genfromtxt('Filterkurve.dat', unpack=True)
ν *= ureg('kHz')
U_A *= ureg('mV')

def lorentzkurve(ν, ν_0, a, γ):
    return a / ((ν**2 - ν_0**2)**2 + γ**2 * ν_0**2)

def fit():
    (ν_0_fit, a_fit, γ_fit) = tools.curve_fit(lorentzkurve, ν.to('kHz').m, U_A.to('mV').m)
    ν_0_fit *= ureg('kHz')
    a_fit *= ureg('kHz⁴ · mV')
    γ_fit *= ureg('kHz')
    print(f"{ν_0_fit=}", f"{a_fit=}", f"{γ_fit=}", sep='\n')
    return (ν_0_fit, a_fit, γ_fit)

def analyse1(the_max, ν_0, a, γ):
    y = the_max / np.sqrt(2)
    ν1 = (ν_0**2 - ( (a/y) - (γ**2) * (ν_0**2) )**.5)**.5
    ν2 = (ν_0**2 + ( (a/y) - (γ**2) * (ν_0**2) )**.5)**.5
    return ν1, ν2

fit_params = fit()

# GEMESSENER Peak
# peak = max(U_A)

ν_linspace = np.linspace(20, 40, 500) * ureg('kHz')
U_A_fit = lorentzkurve(ν_linspace, *fit_params)

peak_fit = max(U_A_fit) # oder f(ν_0)

intersects = analyse1(peak_fit, *fit_params)
print(f"{intersects=}")
guete = fit_params[0] / (intersects[1] - intersects[0])
print(f"{guete=}")

plt.plot(ν, U_A, 'xr', label="Messwerte")
plt.plot(ν_linspace, unp.nominal_values(U_A_fit.m), label="Ausgleichskurve")
# plt.plot([ν.m.nominal_value for ν in analyse1(peak_fit, *fit_params)], 2*[peak_fit.m.nominal_value / np.sqrt(2)], 'go', label="Schnittpunkte")
plt.axhline(peak_fit.n / np.sqrt(2), color='g', label=r"$\frac{1}{\sqrt{2}} \cdot U_{A, max}$")
plt.xlabel(r"$\nu \;/\; kHz$")
plt.ylabel(r"$U_A \;/\; mV$")
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('build/plot_filterkurve.pdf')
# plt.show()
