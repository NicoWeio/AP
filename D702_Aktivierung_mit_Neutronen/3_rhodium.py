import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
# import generate_table
import tools
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

NU_mean = __import__('1_untergrundrate').untergrundrate(ureg)

t, N = np.genfromtxt('Rhodium.dat', unpack=True)
N = unp.uarray(N, np.sqrt(N))
t *= ureg('s')
N /= ureg('15 s')

N -= NU_mean # Nulleffekt abziehen

ln_N = unp.log(N.to('1/s').m)

def fit_fn(t, N0, λ):
    return N0 * np.exp(-λ*t)


t_end_fastdecay = ureg('240 s')
t_bounds_slowdecay = (t_end_fastdecay, t[-1])

slope, intercept = tools.linregress(t[15:], unp.nominal_values(ln_N)[15:] * ureg.dimensionless)
# keine Einheiten für y-Achse – ist ja logarithmisch!

ln_N_lang_fit = slope*t+intercept
N_lang_fit = np.exp(tools.nominal_values(ln_N_lang_fit)) * ureg('1/s')
N_kurz = N - N_lang_fit
ln_N_kurz = np.log(tools.nominal_values(N_kurz).m) # TODO: Hier sollte sich – wie oben – mit unp der Fehler mitnehmen lassen


slope2, intercept2 = tools.linregress(t[:15], unp.nominal_values(ln_N_kurz)[:15] * ureg.dimensionless)

ln_N_kurz_fit = slope2*t+intercept2
N_kurz_fit = np.exp(tools.nominal_values(ln_N_kurz_fit)) * ureg('1/s')

λ1 = (-slope*ureg('1/s'))
λ2 = (-slope2*ureg('1/s'))
T_hw1 = np.log(2) / λ1
T_hw2 = np.log(2) / λ2

print(f"{slope=}, {intercept=}")
print(f"{λ1=}, {T_hw1=}")
print(f"{slope2=}, {intercept2=}")
print(f"{λ2=}, {T_hw2=}")

plt.figure('log')
plt.axvline(x=t_bounds_slowdecay[0], linewidth=0.5, linestyle="--", color='grey')
# plt.errorbar(t.to('s'), unp.nominal_values(N.to('1/s')), fmt='x', yerr=unp.std_devs(N), label='Messwerte')
plt.plot(t, unp.nominal_values(ln_N), 'x', label="Messwerte")
plt.plot(t[15:], tools.nominal_values(ln_N_lang_fit[15:]), label="Fit-Funktion: langsamer Zerfall")
plt.plot(t, unp.nominal_values(ln_N_kurz), 'x', label="Messwerte abzgl. langsamer Zerfall (Fit)")
plt.plot(t[:15+1], tools.nominal_values(ln_N_kurz_fit[:15+1]), label="Fit-Funktion: schneller Zerfall")
plt.plot(t, np.log((N_lang_fit + N_kurz_fit).m), label="Summe beider Fit-Funktionen")
plt.ylim(-1, None)
plt.xlabel(r"$t \mathbin{/} \si{\second}$")
plt.ylabel(r"$ln(N \mathbin{/} \si{\per\second})$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2_log.pdf')
# plt.show()

plt.figure('lin')
plt.axvline(x=t_bounds_slowdecay[0], linewidth=0.5, linestyle="--", color='grey')
tools.errorbar(plt, t, N, fmt='x', label="Messwerte")
plt.plot(t, N_lang_fit, label="Fit-Funktion: langsamer Zerfall")
tools.errorbar(plt, t, N_kurz, fmt='x', label="Messwerte abzgl. langsamer Zerfall (Fit)")
plt.plot(t[:15+1], N_kurz_fit[:15+1], label="Fit-Funktion: schneller Zerfall")
plt.plot(t, N_lang_fit + N_kurz_fit, label="Summe beider Fit-Funktionen")
plt.xlabel(r"$t \mathbin{/} \si{\second}$")
plt.ylabel(r"$N \mathbin{/} \si{\per\second}$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2_lin.pdf')
# plt.show()
