import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats

import pint
ureg = pint.UnitRegistry()

# –––––––––––––

mAll = np.array([1005.9, 1005.9, 1006.0, 1006.0, 1006.1])
m = ufloat(np.mean(mAll), np.std(mAll)) * ureg.grams
print(f"{m=}")

# # siehe abmessungen.py
L = ufloat(60.308, 0.016) * ureg.centimeters #cm
# ––– ist hier nicht eher der Abstand der Einspann-Vorrichtungen gemeint?
# mal probieren…
# L = ufloat(50,0) * ureg.centimeters #cm

# Masse bei x = 25cm
# = L/2

# –––––––––––––

x, D0, Dm = np.genfromtxt('einseitig_eckig.dat', unpack=True)
x  *= ureg.centimeters
D0 *= ureg.micrometers
Dm *= ureg.micrometers
D = Dm - D0
# mache D positiv… (?)
D *= -1

# –––––––––––––

def polyfit(t, T):
    t = unp.nominal_values(t.to('meters**3'))
    T = unp.nominal_values(T.to('meters'))

    # T = a*t+c
    # = 1/m^2 * m^3 + m
    # → m

    params, covariance_matrix = np.polyfit(t, T, deg=1, cov=True)
    errors = np.sqrt(np.diag(covariance_matrix))
    uParams = [ufloat(*x) for x in zip(params, errors)]
    #TODO: Fehlerquelle!!!
    return [uParams[0] * ureg('meters ** -2'), uParams[1] * ureg('meters')]

def fit_fn(x, params):
    assert x.check('[length] ** 3') # zeichnet ja die Linearisierungsfunktion…
    A, B = params
    return A*x + B

# –––––––––––––

# Linearisierungsterm
def linR(x):
    return L*(x**2) - (x**3)/3

# –––––––––––––

linearized_x = linR(x) # length^3
# print("linearized_x", linearized_x)
# pof = polyfit(unp.nominal_values(linearized_x), unp.nominal_values(D))
pof = polyfit(linearized_x, D)
# pof_a = pof[0]*(1000**2)
print(f"polyfitParam a = {pof[0]}")
print(f"polyfitParam c = {pof[1].to('millimeters')}")
pofVals = fit_fn(linearized_x, pof)

#
plt.plot(unp.nominal_values(linearized_x.to('millimeters**3')*1e-5), D.to('millimeters'), 'x', label='Messwerte')
plt.plot(unp.nominal_values(linearized_x.to('millimeters**3')*1e-5), unp.nominal_values(pofVals.to('millimeters')), label='Regression')
#TODO: Nur für eine Seite ↓
plt.xlabel(r"$Lx²-\frac{x³}{3} \;/\; 10^5 \cdot mm^3$")

plt.ylabel(r"$D \;/\; mm$")
plt.tight_layout()
plt.legend()
# plt.show()
plt.savefig('build/plot_einseitig_eckig.pdf')

a = ufloat(11.990, 0.020) * ureg.millimeters
b = ufloat(9.96, 0.04) * ureg.millimeters
#FALSCH: I = (a*(b**3))/12
I = ((a**3)*b)/12
assert I.check('[length] ** 4')
print(f"I={(I.to('meters ** 4'))}")

g = 9.81 * ureg('meters / seconds**2')
E = (m*g)/(48*pof[0]*I) # N/m^2
print(f"E={E.to('newton / millimeters**2')}")
print(f"E={E.to('GPa')}")

E_zielwert = 100000 * ureg('newton / millimeters**2')
print(f"Abweichung vom Zielwert: {(abs(E_zielwert-E).magnitude/E_zielwert.magnitude)*100}%")

# Zielwert: z.B. Messing: E = ~100GPa = 100*1000 N/mm² = 100000 N/mm² = 1e^5 N/mm²
