import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
import pint
ureg = pint.UnitRegistry()
import generate_table

t, T1, p1, T2, p2, N = np.genfromtxt('Daten.dat', unpack=True)

t *= ureg.minutes
N *= ureg.watt

# „Um die Drücke p1 und p2 zu erhalten, muss noch 1 bar auf die gemessenen Drücke p1* und p2* addiert werden.“
# Da die mit "*" versehenen Werte aus "Daten und Hinweise.pdf" mit denen ohne "*" aus "Daten.dat" übereinstimmen, liegt es tatsächlich an uns, 1 bar zu addieren.
p1 += 1
p2 += 1
p1 *= ureg.bar
p2 *= ureg.bar

# „Die Messunsicherheit des digitalen Thermometers kann als ∆T = 0.1 °C angenommen werden.“
# (0.1 °C = 0.1 K)
T1 = unp.uarray(T1, np.full(len(T1), 0.1)) * ureg.celsius
T2 = unp.uarray(T2, np.full(len(T2), 0.1)) * ureg.celsius

# x-Werte für die Approximation
t_linspace = np.linspace(t[0], t[-1])


generate_table.generateTable('table_messdaten',
    [[unp.nominal_values(y) for y in x] for x in zip(
        t.to('minute'),
        T1.to('celsius'),
        p1.to('bar'),
        T2.to('celsius'),
        p2.to('bar'),
        N.to('watt'))
    ], scientific=False)


print("## Aufgabe 5b: Approximation der Temperaturverläufe\n")

def fit_fn(x, params):
    A, B, C = params
    return A*x**2 + B*x + C

# --- Für Aufgabe 5c:
def fit_fn_derivate(x, params):
    A, B, C = params
    result = 2*A*x + B
    assert result.check('kelvin / seconds')
    return result

def polyfit(T):
    the_t = unp.nominal_values(t.to('seconds'))
    the_T = unp.nominal_values(T.to('kelvin'))
    params, covariance_matrix = np.polyfit(the_t, the_T, deg=2, cov=True)
    errors = np.sqrt(np.diag(covariance_matrix))
    return [ufloat(param, error) * ureg(unit) for param, error, unit in zip(params, errors, ['kelvin / seconds**2', 'kelvin / seconds', 'kelvin'])]
    # return [ufloat(*x) for x in zip(params, errors)]

fit_params_T1 = polyfit(T1)
fit_params_T2 = polyfit(T2)

print("T1:")
for param, i in zip(fit_params_T1, ["A","B","C"]):
    print(f"{i} = {param}")
print("T2:")
for param, i in zip(fit_params_T2, ["A","B","C"]):
    print(f"{i} = {param}")

generate_table.generateTable('table_polyfit', [[T_index, A,B,C] for T_index, A,B,C in [list(["$T_1$"] + fit_params_T1), list(["$T_2$"] + fit_params_T2)]], scientific=True)


plt.plot(unp.nominal_values(t_linspace), unp.nominal_values(fit_fn(t_linspace, fit_params_T1).to('kelvin')), label=r"Approximation $T_1$")
plt.errorbar(unp.nominal_values(t), unp.nominal_values(T1.to('kelvin')), fmt='x', yerr=unp.std_devs(T1), label=r'$T_1$')

plt.plot(unp.nominal_values(t_linspace), unp.nominal_values(fit_fn(t_linspace, fit_params_T2).to('kelvin')), label=r"Approximation $T_2$")
plt.errorbar(unp.nominal_values(t), unp.nominal_values(T2.to('kelvin')), fmt='x', yerr=unp.std_devs(T2), label=r'$T_2$')

plt.figure(1)
plt.xlabel(r'$t \; / \; \mathrm{s}$')
plt.xlim(unp.nominal_values(t).min(), unp.nominal_values(t).max()) #TODO
plt.ylabel(r'$T \; / \; K$')
plt.legend()
plt.tight_layout()
plt.savefig('build/wärmepumpe_plot.pdf')


print("\n## Aufgabe 5c:\n")

DERIV_INDICES = [7,14,21,28] # → equal spacing between 0-35

# derivs_T1 = [fit_fn_derivate(t[i], fit_params_T1) for i in DERIV_INDICES]
# derivs_T2 = [fit_fn_derivate(t[i], fit_params_T2) for i in DERIV_INDICES]
all_derivs_T1 = fit_fn_derivate(t, fit_params_T1)
all_derivs_T2 = fit_fn_derivate(t, fit_params_T2)

# zum Ableich die ungefähren Formeln, nicht nur die Werte ausgeben
print(f"dT1/dt = {2 * fit_params_T1[0].to('K/min²').n:.3f} * t + {fit_params_T1[1].to('K/min').n:.3f} [kelvin / minute]")
print(f"dT2/dt = {2 * fit_params_T2[0].to('K/min²').n:.3f} * t + {fit_params_T2[1].to('K/min').n:.3f} [kelvin / minute]")

print("Derivs: t | dT1/dt | dT2/dt")
for i in DERIV_INDICES:
    print(f"t={i}min: {all_derivs_T1[i].to('kelvin / minute')} | {all_derivs_T2[i].to('kelvin / minute')}")

generate_table.generateTable('table_ableitungen', [[i, all_derivs_T1[i].to('kelvin / minute'), all_derivs_T2[i].to('kelvin / minute')] for i in DERIV_INDICES])

print("\n## Aufgabe 5d:\n")

gueteziffer_ideal_table = [None] * (DERIV_INDICES[-1]+1)
for i in DERIV_INDICES:
    gueteziffer_ideal = T1[i].to('kelvin') / (T1[i] - T2[i])
    print(f"Ideale Güteziffer für Minute {i}: {gueteziffer_ideal}")
    gueteziffer_ideal_table[i] = gueteziffer_ideal
# ✓ Werte (für andere t!) stimmen überein mit Tahirbanane, unser Fehler ist aber größer

C_Kupferspirale = 750 * ureg('J/K')
# Wärmekapazität fürs Wasser in Reservoir 1
V_Wasser = 4 * ureg('liter')
c_Wasser = 4.1851 * ureg('kJ/(kg·K)')
ρ_Wasser = 0.998207 * ureg('gram / milliliter')
C_Wasser = (ρ_Wasser * V_Wasser) * c_Wasser
# Wärmekapazität des Eimers war nicht explizit angegeben
C_ges = C_Kupferspirale + C_Wasser
print(f"C_Wasser={C_Wasser.to_compact()}, C_ges={C_ges.to_compact()}")

gueteziffern_real = (C_ges * all_derivs_T1) / N
gueteziffern_real.ito_reduced_units()

for i in DERIV_INDICES:
    print(f"Reale Güteziffer für Minute {i}: {gueteziffern_real[i]}")
# ✓ Übereinstimmung von Wert/Unsicherheit mit Tahirbanane (für andere t!)

generate_table.generateTable('table_gueteziffern', [[i, gueteziffer_ideal_table[i], gueteziffern_real[i]] for i in DERIV_INDICES], scientific=False)

print("\n## Aufgabe 5e:\n")

def Lregress(x, y):
    params, covariance_matrix = np.polyfit(x, y, deg=1, cov=True)
    errors = np.sqrt(np.diag(covariance_matrix))
    return [ufloat(*i) for i in zip(params, errors)]
def LregressFun(params, x):
    slope, intercept = params
    return slope*x + intercept

T2_kehrwert_nominal = unp.nominal_values(1 / T2.to('kelvin'))
ln_p2 = np.log(p2.m)

regressParams = Lregress(T2_kehrwert_nominal, ln_p2)
print("slope, intercept =", regressParams)
# ✓ Identisch zu Tahirbanane's Werten

plt.figure(2)
plt.plot(T2_kehrwert_nominal, ln_p2, 'x', label="Messdaten")
plt.plot(T2_kehrwert_nominal, unp.nominal_values(LregressFun(regressParams, T2_kehrwert_nominal)), label="Ausgleichsgerade")
plt.xlabel(r"$\frac{1}{T_2} \;/\; \frac{1}{\mathrm{K}}$")
plt.ylabel(r"$\mathrm{ln}(p_2 \;/\; \mathrm{bar})$")
plt.legend()
plt.savefig('build/plot_massendurchsatz.pdf')
# plt.show()

a = regressParams[0] * ureg('kelvin')
R = 8.31446261815324 * ureg('J/(mol*K)')
L_reg = -a*R
molar_mass = 120.913 * ureg('gram / mol')
L = L_reg / molar_mass

print(f"{a=}, {R=}, {L_reg=}, {L=}, ")

def massendurchsatz(i):
    assert L.check('[energy] / [mass]')
    result = (C_ges * abs(fit_fn_derivate(t[i], fit_params_T2))) / L
    assert result.check('[mass] / [time]')
    return result

# for i in range(0,35):
for i in DERIV_INDICES:
    print(f"Massendurchsatz für Minute {i}: {massendurchsatz(i).to('gram / second'):.3f} | deriv: {fit_fn_derivate(t[i], fit_params_T2).to('kelvin / minute'):.3f}")

generate_table.generateTable('table_massendurchsatz', [[i, fit_fn_derivate(t[i], fit_params_T2).to('kelvin / minute').m, massendurchsatz(i).to('gram / second').m] for i in DERIV_INDICES], scientific=False)

# L_reg → ähnlich Mampfzwerg
# L → ähnlich Mampfzwerg
# massendurchsatz(0-10) → ähnlich Mampfzwerg, aber mit - statt +

# sys.exit()

print("\n## Aufgabe 5f:\n")

ρ_0 = ureg('5.51 grams/liter')
T_0 = ureg.Quantity(0, ureg.degC).to(ureg.kelvin)
p_0 = ureg('1 bar')
κ = 1.14

def ρ(i):
    T2_i = T2[i].to('kelvin')
    result = (p2[i] * ρ_0 * T_0) / (p_0 * T2_i) # → Mampfzwerg
    assert result.check('[mass] / [volume]')
    return result
    # return (p_0 * ρ_0 * T2_i) / (p2[i] * T_0) # → meine Variante…?

N_mech_table = list()
for i in DERIV_INDICES:
    # ρ = 23.63 * ureg('kg/(m**3)') # → Mampfzwerg
    pa, pb = p2, p1 #!
    N_mech = (1 / (κ - 1)) * (pb[i] * np.power(pa[i]/pb[i], 1/κ) - pa[i]) * (1/ρ(i)) * massendurchsatz(i)
    print(f"N_mech={N_mech.to('watt')} | ρ={ρ(i)}")
    N_mech_table.append([i, ρ(i), N_mech.to('watt')])

generate_table.generateTable('table_kompressorleistung', N_mech_table)
