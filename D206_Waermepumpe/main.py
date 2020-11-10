import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats

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

# x-Werte für die Approximation
t_linspace = np.linspace(t[0], t[-1])

## Aufgabe 5b: Approximation der Temperaturverläufe

# T(t) = A*x**2 + B*x + C → brauchbar :)
# T(t) = A / (1 + B*t) → doof
# T(t) = A / (1 + B*t**2) → doof
# T(t) = (A*t) / (1 + B*t) + C → doof
# T(t) = (A*t**2) / (1 + B*t**2) + C → doof

def fit_fn(x, params):
    A, B, C = params
    return A*x**2 + B*x + C

# Für Aufgabe 5c:
def fit_fn_derivate(x, params):
    A, B, C = params
    return 2*A*x + B

def polyfit(T):
    params, covariance_matrix = np.polyfit(t, T, deg=2, cov=True)
    errors = np.sqrt(np.diag(covariance_matrix))
    return params

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

fit_params_T1 = polyfit(T1)
fit_params_T2 = polyfit(T2)

print("fit_params:", fit_params_T1, fit_params_T2)

plt.plot(t_linspace, fit_fn(t_linspace, fit_params_T1), label=r"Approximation $T_1$")
# plt.plot(t_linspace, fit_fn_2(t_linspace, *curve_fit(T1)), label=r"Approximation $T_1$")
# plt.plot(t_linspace, fit_fn_3(t_linspace, *curve_fit(T1)), label=r"Approximation $T_1$")
plt.errorbar(t, T1,  fmt='x', label=r'$T_1$')
#plt.errorbar(t, p1, yerr = p1 * 0.68, fmt='o', label='p1')

plt.plot(t_linspace, fit_fn(t_linspace, fit_params_T2), label=r"Approximation $T_2$")
# plt.plot(t_linspace, fit_fn_2(t_linspace, *curve_fit(T2)), label=r"Approximation $T_2$")
# plt.plot(t_linspace, fit_fn_3(t_linspace, *curve_fit(T2)), label=r"Approximation $T_2$")
plt.errorbar(t, T2,  fmt='x', label=r'$T_2$')
#plt.errorbar(t, p2, yerr = p2 * 0.68, fmt='o', label='p2')

#plt.errorbar(t, N, fmt='x', label='N')

# TODO: Einheiten passen nicht…
plt.figure(1)
plt.xlabel(r'$t / s$')
plt.xlim(t.min(), t.max())
plt.ylabel(r'$T / K$')
plt.legend()
plt.tight_layout()
# plt.savefig('build/wärmepumpe_plot.pdf')
# plt.show()


## Aufgabe 5c:
# TODO Fehlerrechnung!

# 7-14-21-28 → equal spacing between 0-35
derivs_T1 = [fit_fn_derivate(x, fit_params_T1) for x in [t[7], t[14], t[21], t[28]]]
derivs_T2 = [fit_fn_derivate(x, fit_params_T2) for x in [t[7], t[14], t[21], t[28]]]
print("5c) derivs", derivs_T1, derivs_T2)

## Aufgabe 5d:
gueteziffern_ideal = T1 / (T1 - T2)
print("gueteziffern_ideal", gueteziffern_ideal)
# ✓ stimmt überein mit Tahirbanane

mkck = 750 #J/K
m1cw = 13293 # → Mampfzwerg

gueteziffern_real = ((m1cw + mkck) * fit_fn_derivate(t, fit_params_T1)) / N
print("gueteziffern_real", gueteziffern_real)
# ~ grobe Übereinstimmung mit Mampfzwerg, Tahirbanane

## Aufgabe 5e:

def Lregress(x,y):
    slope, intercept, r_value, p_value, std_err = sp_stats.linregress(x,y)
    return slope, intercept
def LregressFun(params, x):
    slope, intercept = params
    print(slope, intercept)
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
T2_kehrwert = 1 / T2
ln_p2 = np.log(p2)

regressParams = Lregress(T2_kehrwert, ln_p2)
print("slope, intercept", regressParams)


plt.figure(2)
plt.plot(T2_kehrwert, ln_p2, 'x', label="Werte")
plt.plot(T2_kehrwert, LregressFun(regressParams, T2_kehrwert), label="Regression")
plt.xlabel(r"$\frac{1}{T_2}$ in $\frac{1}{K}$") #TODO
# plt.ylabel(r"$\mathrm{ln}(p_2)$") #TODO
plt.legend()
# plt.show()

massendurchsatz = -0.00152 # → Tahirbanane
# Ich will ihn aber positiv für 5f…
# massendurchsatz = 0.00152 # → Tahirbanane

## Aufgabe 5f:

# pa, pb = p1, p2
pa = p1
pb = p2
k = 1.14 # gegeben
rho = 23.63 # → Mampfzwerg

N_mech = (1 / (k - 1)) * (pb * np.power(pa/pb, 1/k) - pa) * (1/rho) * massendurchsatz
print("N_mech", N_mech)
