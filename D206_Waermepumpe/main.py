import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from generate_table import generate_table
import tools

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
T1 = unp.uarray(T1, np.full(len(T1), 0.1)) * ureg.celsius
T2 = unp.uarray(T2, np.full(len(T2), 0.1)) * ureg.celsius

# x-Werte für die Approximation
t_linspace = tools.linspace(*tools.bounds(t))


generate_table('table_messdaten',
    list(zip(
        t.to('minute').m,
        unp.nominal_values(T1.to('celsius').m),
        p1.to('bar').m,
        unp.nominal_values(T2.to('celsius').m),
        p2.to('bar').m,
        N.to('watt').m
        )),
    scientific=False)


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

fit_params_T1 = tools.pint_polyfit(t.to('second'), tools.nominal_values(T1.to('kelvin')), deg=2)
fit_params_T2 = tools.pint_polyfit(t.to('second'), tools.nominal_values(T2.to('kelvin')), deg=2)

print("T1:")
for param, i in zip(fit_params_T1, 'ABC'):
    print(f"{i} = {param}")
print("T2:")
for param, i in zip(fit_params_T2, 'ABC'):
    print(f"{i} = {param}")

generate_table('table_polyfit', [[T_index, A,B,C] for T_index, A,B,C in [list(["$T_1$"] + fit_params_T1), list(["$T_2$"] + fit_params_T2)]], scientific=True)

plt.figure()
with tools.plot_context(plt, 'minute', 'kelvin', 't', 'T') as plt2:
    plt2.plot(t_linspace, fit_fn(t_linspace, fit_params_T1), show_yerr=False, label="Approximation $T_1$")
    plt2.plot(t, T1, fmt='x', label="$T_1$")

    plt2.plot(t_linspace, fit_fn(t_linspace, fit_params_T2), show_yerr=False, label="Approximation $T_2$")
    plt2.plot(t, T2, fmt='x', label="$T_2$")

plt.legend()
plt.tight_layout()
plt.savefig('build/wärmepumpe_plot.pdf')
# plt.show()


print("\n## Aufgabe 5c:\n")

DERIV_INDICES = [7,14,21,28] # → äquidistant zwischen 0 und 35

all_derivs_T1 = fit_fn_derivate(t, fit_params_T1)
all_derivs_T2 = fit_fn_derivate(t, fit_params_T2)

# zum Ableich die ungefähren Formeln, nicht nur die Werte ausgeben
print(f"dT1/dt = {2 * fit_params_T1[0].to('K/min²').n:.3f} * t + {fit_params_T1[1].to('K/min').n:.3f} [kelvin / minute]")
print(f"dT2/dt = {2 * fit_params_T2[0].to('K/min²').n:.3f} * t + {fit_params_T2[1].to('K/min').n:.3f} [kelvin / minute]")

print("Ableitungen: t | dT1/dt | dT2/dt")
for i in DERIV_INDICES:
    print(f"t={i}min: {all_derivs_T1[i].to('kelvin / minute')} | {all_derivs_T2[i].to('kelvin / minute')}")

generate_table('table_ableitungen', [[i, all_derivs_T1[i].to('kelvin / minute'), all_derivs_T2[i].to('kelvin / minute')] for i in DERIV_INDICES])


print("\n## Aufgabe 5d:\n")

gueteziffer_ideal_table = [None] * (DERIV_INDICES[-1]+1)
for i in DERIV_INDICES:
    gueteziffer_ideal = T1[i].to('kelvin') / (T1[i] - T2[i])
    print(f"Ideale Güteziffer für Minute {i:>2}: {gueteziffer_ideal.to('dimensionless')}")
    gueteziffer_ideal_table[i] = gueteziffer_ideal
# ✓ Werte (für andere t!) stimmen überein mit Tahirbanane, unser Fehler ist aber größer

C_Kupferspirale = ureg('750 J/K')
# Wärmekapazität fürs Wasser in Reservoir 1
V_Wasser = ureg('4 liter')
c_Wasser = ureg('4.1851 kJ/(kg·K)')
ρ_Wasser = ureg('0.998207 gram / milliliter')
C_Wasser = (ρ_Wasser * V_Wasser) * c_Wasser
# Wärmekapazität des Eimers war nicht explizit angegeben
C_ges = C_Kupferspirale + C_Wasser
print(f"C_Wasser={C_Wasser.to('kJ/K'):.3f}, C_ges={C_ges.to('kJ/K'):.3f}")

gueteziffern_real = (C_ges * all_derivs_T1) / N

for i in DERIV_INDICES:
    print(f"Reale Güteziffer für Minute {i}: {gueteziffern_real[i].to('dimensionless')}")
# ✓ Übereinstimmung von Wert/Unsicherheit mit Tahirbanane (für andere t!)

generate_table('table_gueteziffern', [
    [
        i,
        gueteziffer_ideal_table[i].to('dimensionless'),
        gueteziffern_real[i].to('dimensionless')
    ] for i in DERIV_INDICES], scientific=False)


print("\n## Aufgabe 5e:\n")

T2_kehrwert_nominal = tools.nominal_values(1 / T2.to('kelvin'))
ln_p2 = np.log(p2.m) * ureg('dimensionless')

slope, intercept = tools.linregress(T2_kehrwert_nominal, ln_p2)

print(f"{slope=}, {intercept=}")

plt.figure()
plt.plot(T2_kehrwert_nominal.m, ln_p2.m, 'x', label="Messwerte")
plt.plot(T2_kehrwert_nominal.m, tools.nominal_values(slope * T2_kehrwert_nominal + intercept).m, label="Ausgleichsgerade")
plt.xlabel(r"$\frac{1}{T_2} \mathbin{/} \si{\per\kelvin}$")
plt.ylabel(r"$\ln(p_2 \mathbin{/} \si{\bar})$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot_massendurchsatz.pdf')
# plt.show()

L_reg = -slope * ureg.R  # R ist die molare Gaskonstante
molar_mass = ureg('120.913 gram / mole')
L = L_reg / molar_mass
print(f"{L_reg.to('joule / mole')=}, {L.to('joule / gram')=}")

massendurchsatz = (C_ges * abs(fit_fn_derivate(t, fit_params_T2))) / L
# massendurchsatz(0-10) → ähnlich Mampfzwerg, aber mit - statt +

for i in DERIV_INDICES:
    print(f"Massendurchsatz für Minute {i}: {massendurchsatz[i].to('gram / second'):.3f} | deriv: {fit_fn_derivate(t[i], fit_params_T2).to('kelvin / minute'):.3f}")

generate_table('table_massendurchsatz', [[i, fit_fn_derivate(t[i], fit_params_T2).to('kelvin / minute').m, massendurchsatz[i].to('gram / second').m] for i in DERIV_INDICES], scientific=False)


print("\n## Aufgabe 5f:\n")

ρ_0 = ureg('5.51 gram / liter')
T_0 = ureg.Quantity(0, ureg.degC).to(ureg.kelvin)
p_0 = ureg('1 bar')
κ = 1.14


ρ = (p2 * ρ_0 * T_0) / (p_0 * T2.to('kelvin'))
# (p_0 * ρ_0 * T2_i) / (p2 * T_0) # → meine Variante…?
# ρ = 23.63 * ureg('kg/(m**3)') # → Mampfzwerg

N_mech = (1 / (κ - 1)) * (p1 * np.power(p2/p1, 1/κ) - p2) * (1/ρ) * massendurchsatz

N_mech_table = list()
for i in DERIV_INDICES:
    print(f"N_mech={N_mech[i].to('watt'):2.3f} | ρ={ρ[i]:2.3f}")
    N_mech_table.append([i, ρ[i], N_mech[i].to('watt')])

generate_table('table_kompressorleistung', N_mech_table)
