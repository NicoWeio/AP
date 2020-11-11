import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
#TODO
import sys

import generate_table

t, T1, p1, T2, p2, N = np.genfromtxt('Daten.dat', unpack=True)

# Minuten → Sekunden
t *= 60
# °C → Kelvin
T1 += 273.15
T2 += 273.15
# „Um die Drücke p1 und p2 zu erhalten, muss noch 1 bar auf die gemessenen Drücke p1* und p2* addiert werden.“
# Da die mit "*" versehenen Werte aus "Daten und Hinweise.pdf" mit denen ohne "*" aus "Daten.dat" übereinstimmen, liegt es tatsächlich an uns, 1 bar zu addieren.
p1 += 1
p2 += 1

# „Die Messunsicherheit des digitalen Thermometers kann als ∆T = 0.1 °C angenommen werden.“
# (0.1 °C = 0.1 K)
T1 = unp.uarray(T1, np.full(len(T1), 0.1))
T2 = unp.uarray(T2, np.full(len(T2), 0.1))

# x-Werte für die Approximation
t_linspace = np.linspace(t[0], t[-1])

## Aufgabe 5b: Approximation der Temperaturverläufe
print("## Aufgabe 5b: Approximation der Temperaturverläufe\n")

# T(t) = A*x**2 + B*x + C → brauchbar :)
# T(t) = A / (1 + B*t) → doof
# T(t) = A / (1 + B*t**2) → doof
# T(t) = (A*t) / (1 + B*t) + C → doof
# T(t) = (A*t**2) / (1 + B*t**2) + C → doof

def fit_fn(x, params):
    A, B, C = params
    return A*x**2 + B*x + C

# --- Für Aufgabe 5c:
def fit_fn_derivate(x, params):
    A, B, C = params
    return ufloat(
        2*A.n*x + B.n,
        np.sqrt((2*x*A.s)**2 + (B.s)**2)
    )
# def fit_fn_derivate_error(x, paramErrors):
#     A_err, B_err, C_err = paramErrors
#     return np.sqrt((2*x*A_err)**2 + (B_err)**2)
# ---

def polyfit(T):
    params, covariance_matrix = np.polyfit(t, T, deg=2, cov=True)
    errors = np.sqrt(np.diag(covariance_matrix))
    return [ufloat(*x) for x in zip(params, errors)]

# def fit_fn_2(t, A, B):
#     alpha = 1
#     return A / (1 + B*t**alpha)
#
# def fit_fn_3(t, A, B, C):
#     alpha = 2
#     return (A*t**alpha) / (1 + B*t**alpha) + C
#
# def curve_fit(T):
#     popt, pcov = sp_optimize.curve_fit(fit_fn_3, t, T)
#     return popt

fit_params_T1 = polyfit(unp.nominal_values(T1))
fit_params_T2 = polyfit(unp.nominal_values(T2))

print("T1:")
for param, i in zip(fit_params_T1, ["A","B","C"]):
    print(f"{i} = {param.n:.5} ± {param.s:.5}")
print("T2:")
for param, i in zip(fit_params_T2, ["A","B","C"]):
    print(f"{i} = {param.n:.5} ± {param.s:.5}")

generate_table.generateTable('table_polyfit', [[T_index, A,B,C] for T_index, A,B,C in [list(["$T_1$"] + fit_params_T1), list(["$T_2$"] + fit_params_T2)]], scientific=True)

# generate_table.generateTable('table_polyfit_T1', [[i, param] for param, i in zip(fit_params_T1, ["A","B","C"])])


plt.plot(t_linspace, unp.nominal_values(fit_fn(t_linspace, fit_params_T1)), label=r"Approximation $T_1$")
plt.errorbar(t, unp.nominal_values(T1), fmt='x', yerr=unp.std_devs(T1), label=r'$T_1$')

plt.plot(t_linspace, unp.nominal_values(fit_fn(t_linspace, fit_params_T2)), label=r"Approximation $T_2$")
plt.errorbar(t, unp.nominal_values(T2), fmt='x', yerr=unp.std_devs(T2), label=r'$T_2$')

plt.figure(1)
plt.xlabel(r'$t \; / \; \mathrm{min}$')
plt.xlim(t.min(), t.max())
plt.ylabel(r'$T \; / \; K$')
plt.legend()
plt.tight_layout()
plt.savefig('build/wärmepumpe_plot.pdf')


## Aufgabe 5c:
print("\n## Aufgabe 5c:\n")

DERIV_INDICES = [7,14,21,28] # 7-14-21-28 → equal spacing between 0-35
# DERIV_INDICES = [8,16,24,32] # → Tahirbanane

def fit_fn_derivate_error(x, paramErrors):
    A_err, B_err, C_err = paramErrors
    return np.sqrt((2*x*A_err)**2 + (B_err)**2)

derivs_T1 = [fit_fn_derivate(t[i], fit_params_T1) for i in DERIV_INDICES]
derivs_T2 = [fit_fn_derivate(t[i], fit_params_T2) for i in DERIV_INDICES]

print("Derivs: t | dT1/dt | dT2/dt")
for deriv_T1, deriv_T2, i in zip(derivs_T1, derivs_T2, DERIV_INDICES):
    print(f"{i}: {deriv_T1:.3e} {deriv_T2:.3e}")


## Aufgabe 5d:
print("\n## Aufgabe 5d:\n")

for i in DERIV_INDICES:
    gueteziffer_ideal = T1[i] / (T1[i] - T2[i])
    print(f"Ideale Güteziffer für Minute {i} / t={t[i]:.0f}: {gueteziffer_ideal}")
# ✓ Werte (für andere t!) stimmen überein mit Tahirbanane, unser Fehler ist aber größer

C_Kupferspirale = 750 #J/K

# Wärmekapazität fürs Wasser in Reservoir 1
V_Wasser = 4 # L
c_Wasser = 4.1851 * 1000 # J/(kg·K)
ρ_Wasser = 0.998207
C_Wasser = (ρ_Wasser * V_Wasser) * c_Wasser
# Wärmekapazität des Eimers war nicht explizit angegeben
C_ges = C_Kupferspirale + C_Wasser
print(f"{C_Wasser=}, {C_ges=}")

for i in DERIV_INDICES:
    myDeriv = fit_fn_derivate(t[i], fit_params_T1)
    gueteziffer_real = (C_ges * myDeriv) / N[i]
    print(f"Reale Güteziffer für Minute {i} / t={t[i]:.0f}: {gueteziffer_real}")
# ✓ Übereinstimmung von Wert/Unsicherheit mit Tahirbanane (für andere t!)

## Aufgabe 5e:
print("\n## Aufgabe 5e:\n")

def Lregress(x,y):
    slope, intercept, r_value, p_value, std_err = sp_stats.linregress(x,y)
    return slope, intercept
def LregressFun(params, x):
    slope, intercept = params
    return slope*x + intercept

# plt.figure(5)
# plt.yscale('log')
# plt.plot(1/T1, p1, label=f"$Todo_1$")
# plt.plot(1/T2, p2, label=f"$Todo_2$")
# plt.plot(1/T1, LregressFun(Lregress(1/T1, p1), 1/T1), label=f"$Foo$")
# plt.plot(1/T2, LregressFun(Lregress(1/T2, p2), 1/T2), label=f"$Foo$")
# #TODO wohl doch besser linear scale und ln auf die Werte anwenden…
# plt.legend()
# plt.show()
# –––––
T2_kehrwert_nominal = unp.nominal_values(1 / T2)
ln_p2 = np.log(p2)

regressParams = Lregress(T2_kehrwert_nominal, ln_p2)
#TODO Fehler!
print("slope, intercept =", regressParams)
# ✓ Identisch zu Tahirbanane's Werten

plt.figure(2)
plt.plot(T2_kehrwert_nominal, ln_p2, 'x', label="Messdaten")
plt.plot(T2_kehrwert_nominal, LregressFun(regressParams, T2_kehrwert_nominal), label="Ausgleichsgerade")
plt.xlabel(r"$\frac{1}{T_2}$ in $\frac{1}{K}$") #TODO
# plt.ylabel(r"$\mathrm{ln}(p_2)$") #TODO
plt.legend()
# plt.show()

a = regressParams[0]
R = 8.31446261815324 # J/mol*K
L_reg = -a*R
molar_mass = 120.913 # g/mol
L = L_reg / molar_mass

print(f"{a=}, {R=}, {L_reg=}, {L=}, ")

def massendurchsatz(i):
    return (C_ges * fit_fn_derivate(t[i], fit_params_T2)) / L

# for i in range(0,35):
for i in DERIV_INDICES:
    print(f"Massendurchsatz für Minute {i}: {massendurchsatz(i):.3f} [g/s] | deriv: {fit_fn_derivate(t[i], fit_params_T2):.3f}")

generate_table.generateTable('table_massendurchsatz', [[t[i], fit_fn_derivate(int(t[i]), fit_params_T2)*(10**3), massendurchsatz(i)] for i in DERIV_INDICES], scientific=False)

# L_reg → ähnlich Mampfzwerg
# L → ähnlich Mampfzwerg
# massendurchsatz(0-10) → ähnlich Mampfzwerg, aber mit - statt +

# sys.exit()

## Aufgabe 5f:
print("\n## Aufgabe 5f:\n")

ρ_0 = 5.52 # g/L
T_0 = 273.15 # K
p = 1 # bar
κ = 1.14

N_mech_table = list()
for i in DERIV_INDICES:
    rho = 23.63 # → Mampfzwerg #TODO
    pb = p1 #!
    pa = p2 #!
    N_mech = (1 / (κ - 1)) * (pb[i] * np.power(pa[i]/pb[i], 1/κ) - pa[i]) * (1/rho) * massendurchsatz(i)
    print("N_mech", N_mech)
    N_mech_table.append([t[i], N_mech])

generate_table.generateTable('table_kompressorleistung', N_mech_table, scientific=False)

# # pa, pb = p1, p2
# # hier hatte ich die beiden vertauscht… :/
# pa = p2
# pb = p1
# k = 1.14 # gegeben
# rho = 23.63 # → Mampfzwerg
#
# N_mech = (1 / (k - 1)) * (pb * np.power(pa/pb, 1/k) - pa) * (1/rho) * massendurchsatz
# print("N_mech", N_mech)
