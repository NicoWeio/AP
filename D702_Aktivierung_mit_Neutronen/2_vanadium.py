import matplotlib.pyplot as plt
import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import uncertainties.unumpy as unp
import tools

NU_mean = __import__('1_untergrundrate').untergrundrate(ureg)

t, N = np.genfromtxt('Vanadium.dat', unpack=True)
N = unp.uarray(N, np.sqrt(N))
t *= ureg('s')
N /= ureg('30 s')

N -= NU_mean # Nulleffekt abziehen

def fit_fn(t, N0, λ):
    return N0 * np.exp(-λ*t)

def fit(t, N):
    (N0_fit, λ_fit) = tools.curve_fit(fit_fn, unp.nominal_values(t.to('s').m), unp.nominal_values(N.to('1/s').m), p0=param_guesses)
    λ_fit *= ureg('1/s')
    T_hw = np.log(2) / λ_fit # Halbwertszeit
    print(f"{N0_fit=}, {λ_fit=}, {T_hw=}")
    return N0_fit, λ_fit, T_hw

param_guesses = [N[0].n, (np.log((N[0]/N[-1]).n)/t[-1]).m]
N0_fit, λ_fit, T_hw = fit(t, N)

double_hw_index = np.argmax(t > T_hw) # finde den ersten Index, an dem t > T_hw ist
N0_fit_2, λ_fit_2, T_hw_2 = fit(t[double_hw_index:], N[double_hw_index:])

t_linspace = np.linspace(0, t[-1])

for yscale in ['log', 'linear']:
    plt.figure(yscale)
    tools.errorbar(plt, t.to('s'), N.to('1/s'), fmt='x', zorder=5, label='Messwerte')
    plt.plot(t_linspace, tools.nominal_values(fit_fn(t_linspace, N0_fit, tools.nominal_value(λ_fit))).m, label="Fit-Funktion")
    plt.plot(t_linspace, tools.nominal_values(fit_fn(t_linspace, N0_fit_2, tools.nominal_value(λ_fit_2))).m, label="Fit-Funktion 2")
    plt.axvline(x=(T_hw.n), linewidth=0.5, linestyle="--", color='grey')
    plt.axvline(x=(2*T_hw.n), linewidth=0.5, linestyle="--", color='grey')
    plt.xlabel(r"$t \mathbin{/} \si{\second}$")
    plt.ylabel(r"$N \mathbin{/} \si{\per\second}$")
    plt.yscale(yscale)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'build/plot1_{yscale[:3]}.pdf')
    # plt.show()
