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

t_linspace = np.linspace(0, t[-1])
t_unitless = unp.nominal_values(t)

slope, intercept = tools.linregress(t[15:], unp.nominal_values(ln_N)[15:])
# keine Einheiten für y-Achse – ist ja logarithmisch!

ln_N_lang_fit = slope*t_unitless+intercept
N_lang_fit = np.exp(unp.nominal_values(ln_N_lang_fit)) * ureg('1/s')
N_kurz = N - N_lang_fit
ln_N_kurz = np.log(unp.nominal_values(N_kurz))

slope2, intercept2 = tools.linregress(t[:15], unp.nominal_values(ln_N_kurz)[:15])

ln_N_kurz_fit = slope2*t_unitless+intercept2
N_kurz_fit = np.exp(unp.nominal_values(ln_N_kurz_fit)) * ureg('1/s')

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
plt.plot(t_unitless[15:], unp.nominal_values(ln_N_lang_fit[15:]), label="Fit-Funktion: langsamer Zerfall")
plt.plot(t, unp.nominal_values(ln_N_kurz), 'x', label="Messwerte abzgl. langsamer Zerfall (Fit)")
plt.plot(t_unitless[:15+1], unp.nominal_values(ln_N_kurz_fit[:15+1]), label="Fit-Funktion: schneller Zerfall")
ln_N_sum_fit = np.log(unp.nominal_values(N_lang_fit + N_kurz_fit))
plt.plot(t_unitless, unp.nominal_values(ln_N_sum_fit), label="Summe beider Fit-Funktionen")
plt.ylim(-1, None)

plt.xlabel(r"$t \;/\; s$")
plt.ylabel(r"$ln(N)$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2_log.pdf')
# plt.show()

plt.figure('lin')
plt.axvline(x=t_bounds_slowdecay[0], linewidth=0.5, linestyle="--", color='grey')
plt.errorbar(t, unp.nominal_values(N), fmt='x', yerr=unp.std_devs(N), label="Messwerte")
plt.plot(t_unitless, N_lang_fit, label="Fit-Funktion: langsamer Zerfall")
plt.errorbar(t, unp.nominal_values(N_kurz), fmt='x', yerr=unp.std_devs(N_kurz), label="Messwerte abzgl. langsamer Zerfall (Fit)")
plt.plot(t_unitless[:15+1], N_kurz_fit[:15+1], label="Fit-Funktion: schneller Zerfall")
plt.plot(t_unitless, N_lang_fit + N_kurz_fit, label="Summe beider Fit-Funktionen")
plt.xlabel(r"$t \;/\; s$")
plt.ylabel(r"$N \;/\; \frac{1}{s}$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2_lin.pdf')
# plt.show()
