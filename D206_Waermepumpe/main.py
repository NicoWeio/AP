import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as sp_optimize

t, T1, p1, T2, p2, N = np.genfromtxt('Daten.dat', unpack=True)

# °C → Kelvin
T1 += 273.15
T2 += 273.15

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

plt.xlabel(r'$t / s$')
plt.xlim(0, 36)
plt.ylabel(r'$T / K$')
plt.legend()
plt.tight_layout()
# plt.savefig('build/wärmepumpe_plot.pdf')
plt.show()
