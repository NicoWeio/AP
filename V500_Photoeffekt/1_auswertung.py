import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import uncertainties.unumpy as unp
from uncertainties import ufloat
from scipy.optimize import curve_fit
import scipy.constants as const
import generate_table
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

data = [
{
'color': 'gelb',
'colorName': 'Gelb',
'plotColor': 'orange',
'range': (9, -8),
'λ': ureg('578 nm'),
},
{
'color': 'gruen',
'colorName': 'Grün',
'plotColor': 'green',
'range': (8, -1),
'λ': ureg('546 nm'),
},
{
'color': 'violett',
'colorName': 'Violett',
'plotColor': 'violet',
'range': (9, -1),
'λ': ureg('435 nm'),
},
{
'color': 'ultraviolett',
'colorName': 'Ultraviolett',
'plotColor': 'blue',
'range': (8, -1),
'λ': ureg('365.5 nm'),
},
]



for d in data:
    print(f"→ {d['colorName']} ({d['λ']})")

    range = d['range']

    # Daten einlesen
    U, I = np.genfromtxt(f"{d['color']}.dat", unpack=True)
    # Die Datendateien sind nicht sortiert, sondern geben unsere Messreihenfolge wieder. Das würde sonst stören.
    U, I = zip(*sorted(zip(U, I)))
    U = list(U) * ureg('V')
    I = list(I) * ureg('nA')

    # Wir betrachten nur den linearen Abschnitt. Und aus negativen Zahlen mag Python keine Wurzel ziehen.
    U_ranged = U[range[0] : range[1]]
    sqrt_I_ranged = I[range[0] : range[1]] ** .5

    a, b = tools.linregress(U_ranged, sqrt_I_ranged)
    print(f"a={a}"); print(f"b={b}")
    d['a'] = a; d['b'] = b

    #Grenzspannungen
    U_g = (-b/a).to('V')
    print("Nullstelle", U_g)
    d['U_g'] = U_g

    # Die Ausgleichgerade bzw. der Plot soll die Nullstelle immer einschließen
    # U_fit_point_upper = U_ranged[-1] if U_ranged[-1] > U_g else U_g
    U_fit_point_upper = max(U_g, U_ranged[-1])
    U_fit_points = np.array([U_ranged[0].to('V').m, U_fit_point_upper.to('V').m]) * ureg('V')
    I_fit_points = a*U_fit_points + b

    # Diesmal besonders pedantisch: Plotte Messwerte *über* der Ausgleichgeraden, ohne die Reihenfolge in der Legende zu ändern.
    plt.figure()
    plt.axhline(0, color='grey')
    plt.plot(unp.nominal_values(U_fit_points.m), unp.nominal_values(I_fit_points.m), "-", label=f"Ausgleichsgerade {d['colorName']}", color=d['plotColor'])
    plt.plot(U_ranged.to('V').m, sqrt_I_ranged.to('nA**0.5').m, "x", label=f"Messwerte {d['colorName']}", color='black')
    plt.xlabel("$U \;/\; \mathrm{V}$")
    plt.ylabel("$\sqrt{I \;/\; \mathrm{nA}}$")
    handles, labels = plt.gca().get_legend_handles_labels()
    labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0], reverse=True))
    plt.legend(handles, labels)
    plt.tight_layout()
    plt.savefig(f"build/plot_sqrt_{d['color']}.pdf")
    # plt.show()

table_data = [(d['colorName'], d['λ'].m, d['a'], d['b'], d['U_g']) for d in data]
generate_table.generate_table('table_fitdata', [[*i] for i in table_data], col_fmt=[None, {'d': 1}, {'d': (3,3)}, {'d': (3,3)}, {'d': (3,3)}])

##b)
print("\n––– b)\n")
U_g = np.array([d['U_g'].n for d in data]) * ureg('V')
λ = tools.pintify([d['λ'] for d in data])
print(f"{λ=}")

e = 1 * ureg.elementary_charge
c = 1 * ureg.speed_of_light

ν = (c/λ).to('THz')
print(f"{ν=}")

α, β = tools.linregress(ν, U_g)

# Verhältnis h/e
print(f"α=h/e{α.to('V·s')}")
# (3.6±0.3)·10^-15 eV → mwindau
# (3.82±0.13)·10^-15 eV·s → aknierim
# (4.3±0.2)·10^-15 J·s/C (=V·s) → rkallo
# (4.486±0.655)·10^-15 V·s → Jean1995
# αT = (1*ureg.h)/(1*ureg.e)
αT = 1 * (ureg.h / ureg.e)
print(f"→ Theoriewert: {αT.to('V·s')}")
α_rel_err = ((αT - α)/αT).to('dimensionless')
print("→ Fehler:", f'{(α_rel_err * 100):.2f} %')

print(f"β={β.to('V')}")

# Austrittsarbeit
A_K = - β * e
print(f"{A_K=}")
# 0.264 eV → Mampfzwerg
# (1.4±0.3) eV → mwindau
# (1.46±0.08) eV → aknierim
# (1.71±0.15) eV → rkallo
# (-2.0±0.4) eV → Jean1995

## Plot
ν_linspace = np.array([min(ν).to('THz').m, max(ν).to('THz').m]) * ureg('THz')
print(f"{ν_linspace=}")

plt.figure()
plt.plot(ν_linspace, unp.nominal_values((ν_linspace * α + β).to('V').m), color='grey', label="Ausgleichgerade")
for ν, U_g, d in zip(ν, U_g, data):
    plt.plot(ν, U_g, "x", label=d['colorName'], color=d['plotColor'])

plt.xlabel(r'$\nu \;/\; \mathrm{THz}$')
plt.ylabel(r'$U_g \;/\; \mathrm{V}$')
plt.legend()
plt.tight_layout()
plt.savefig("build/plot_nu_ug.pdf")
# plt.show()
