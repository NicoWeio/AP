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
L = ufloat(60.2, 0.4) * ureg.centimeters #cm
# ––– ist hier nicht eher der Abstand der Einspann-Vorrichtungen gemeint?
# mal probieren…
# L = ufloat(50,0) * ureg.centimeters #cm

# Masse bei x = 25cm
# = L/2

# –––––––––––––

x, D0, Dm = np.genfromtxt('beidseitig_rund.dat', unpack=True)
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

# Linearisierungsterme
def linR(x): # für x <= L/2
    return 3*(L**2)*x - 4*(x**3)

def linL(x): # für x >= L/2
    return 4*(x**3) - 12*L*(x**2) + 9*(L**2)*x - L**3

# –––––––––––––

x_rechts = x[:8] # die ersten 8 Werte (x <= L/2)
D_rechts = D[:8]
x_links = x[-8:] # die letzten 8 Werte (x >= L/2)
D_links = D[-8:]

# print('+++', x)
# print('+++', x_rechts)
# print('+++', x_links)

#TEST: rechts und links vertauschen → macht keinen Unterschied
# x_rechts = x[-8:]
# D_rechts = D[-8:]
# x_links = x[:8]
# D_links = D[:8]

# IMPROVE: deduplizieren, like so… ↓
# for x_i in [x_links, x_rechts…]:
#     linearized_x_i = linR(x_i) # length^3
#     print("linearized_x_i", linearized_x_i)
#     # pof_i = polyfit(unp.nominal_values(linearized_x_i), unp.nominal_values(D_i))
#     pof_i = polyfit(linearized_x_i, D_i)
#     print(f"polyfitParam a = {pof_i[0]}")
#     print(f"polyfitParam c = {pof_i[1]}")
#     pof_iVals = fit_fn(linearized_x_i, pof_i)


linearized_x_rechts = linR(x_rechts) # length^3
print("linearized_x_rechts", linearized_x_rechts)
# pof_rechts = polyfit(unp.nominal_values(linearized_x_rechts), unp.nominal_values(D_rechts))
pof_rechts = polyfit(linearized_x_rechts, D_rechts)
print(f"polyfitParams rechts = {pof_rechts[0]}  &  {pof_rechts[1].to('µm')}")
pof_rechtsVals = fit_fn(linearized_x_rechts, pof_rechts)

linearized_x_links = linL(x_links) # length^3 #CHANGED!
print("linearized_x_links", linearized_x_links)
# pof_links = polyfit(unp.nominal_values(linearized_x_links), unp.nominal_values(D_links))
pof_links = polyfit(linearized_x_links, D_links)
print(f"polyfitParams links = {pof_links[0]}  &  {pof_links[1].to('µm')}")
pof_linksVals = fit_fn(linearized_x_links, pof_links)


for (linearized_x_i, D_i, pofVals_i, xlabel, filename) in [
        (linearized_x_rechts, D_rechts, pof_rechtsVals, r"$Lx²-\frac{x³}{3} \;/\; 10^5 \cdot mm^3$",      'build/plot_beidseitig_rund_rechts.pdf'),
        (linearized_x_links,  D_links,  pof_linksVals,  r"$4x^3-12Lx^2+9L^2x-L^3 \;/\; 10^5 \cdot mm^3$", 'build/plot_beidseitig_rund_links.pdf')
    ]:
    plt.plot(unp.nominal_values(linearized_x_i.to('millimeters**3')*1e-5), D_i.to('millimeters'), 'x', label='Messwerte')
    plt.plot(unp.nominal_values(linearized_x_i.to('millimeters**3')*1e-5), unp.nominal_values(pofVals_i.to('millimeters')), label='Regression')
    plt.xlabel(xlabel)
    plt.ylabel(r"$D \;/\; mm$")
    plt.tight_layout()
    plt.legend()
    # plt.show()
    plt.savefig(filename)
    plt.clf()

d = ufloat(9.99, 0.020) * ureg.millimeters
R = d/2
I = (np.pi * R**4)/4
assert I.check('[length] ** 4')
print(f"I={(I.to('meters ** 4'))}")
# sollte in folgender Größenordnung liegen: I=(1.431+/-0.009)e-09 meter ** 4

g = 9.81 * ureg('meters / seconds**2')
E_rechts = (m*g)/(48*pof_rechts[0]*I) # N/m^2
print(f"E_rechts = {E_rechts.to('newton / millimeters**2')}")
E_links = (m*g)/(48*pof_links[0]*I)
print(f"E_links = {E_links.to('newton / millimeters**2')}")

E_avg = (E_links+E_rechts)/2
print(f"Mittelwert: E={E_avg.to('newton / millimeters**2')} = {E_avg.to('GPa')}")

E_zielwert = 100000 * ureg('newton / millimeters**2')
# print(f"Abweichung vom Zielwert: {(abs(E_zielwert-E_avg).magnitude/E_zielwert.magnitude)*100}%")
# print(f"abs. Abweichung vom Zielwert: {abs(E_zielwert-E_avg)}")
print(f"rel. Abweichung vom Zielwert: {(E_avg.to('newton / millimeters**2')/E_zielwert.to('newton / millimeters**2'))}")

# Zielwert: z.B. Messing: E = ~100GPa = 100*1000 N/mm² = 100000 N/mm² = 1e^5 N/mm²


print('***', x, linL(x))
