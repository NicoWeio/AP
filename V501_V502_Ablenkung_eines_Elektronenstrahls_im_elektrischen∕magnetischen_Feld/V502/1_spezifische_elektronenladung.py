import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

from generate_table import generate_table
import tools

N = 20 # Windungszahl
R = ureg('0.282 m') # Spulenradius
L = ureg('0.175 m') # Der Weg L der Elektronen, auf dem das Magnetfeld wirksam ist, reicht etwa von der Beschleunigungselektrode bis zum Leuchtschirm. Er kann aus der Konstruktionszeichnung der Röhre entnommen werden (siehe V501; Abb.5).

e_div_m_theo = (1 * ureg.elementary_charge / ureg.electron_mass)

def analyze(I, U_b, i):
    B = (ureg.mu_0 * (8 / 125**.5) * (N / R) * I).to('µT')
    D = list(range(len(I))) # „Linien-Index“ auf dem Leuchtschirm
    D *= ureg.inch / 4      # …umgerechnet in die Ablenkung
    ding = D / (L**2 + D**2)
    a, b = tools.linregress(B, ding)
    print(f"a = {a.to('1/m/T'):.1f}")
    e_div_m = 8 * U_b * a**2
    print(tools.fmt_compare_to_ref(e_div_m, e_div_m_theo, unit='C/kg', name='e/m'))

    plt_vals, = plt.plot(B, ding.to('1/m'), 'x', color=f"C{i}")
    plt_regress, = plt.plot(B, (tools.nominal_value(a)*B + tools.nominal_value(b)).to('1/m'), '-', color=f"C{i}")
    return ((plt_vals, plt_regress), (U_b, a, e_div_m))

U_b_list = [250, 300, 350, 400, 420] * ureg.V

plt.figure()
actor_tuple_list = []
data_list = []
I_list = []

for i, U_b in enumerate(U_b_list):
    print(f"→ U_b = {U_b}")
    I = np.genfromtxt(f'V502/data/{U_b.m}V.dat', unpack=True) * ureg.A
    I_list.append(I)
    result = analyze(I, U_b, i)
    actor_tuple_list.append(result[0])
    data_list.append(result[1])
    print()

e_div_m_list = tools.pintify([d[2] for d in data_list])
e_div_m_mean = np.mean(e_div_m_list)
print(tools.fmt_compare_to_ref(e_div_m_mean, e_div_m_theo, unit='C/kg', name='e/m mean'))

plt.legend(actor_tuple_list, [f"$U_b = {U_b.m} V$" for U_b in U_b_list])
plt.xlabel(r"$B \mathbin{/} \si{\micro\tesla}$")
plt.ylabel(r"$\frac{D}{L²+D²} \mathbin{/} \si{\per\meter}$")
plt.grid()
# plt.show()
plt.tight_layout()
plt.savefig('build/plt/V502_1.pdf')

D_list = list(range(max([len(I) for I in I_list]))) # „Linien-Index“ auf dem Leuchtschirm
D_list *= ureg.inch / 4                             # …umgerechnet in die Ablenkung

# generate_table('tab/V502_tab_a', [(U_b, a.to('1/m/T'), e_div_m.to('C/kg') / 1e11) for U_b, a, e_div_m in data_list], col_fmt=[{'d': 0}, {'d': 1}, {'d': 2}], headers=['U_b', 'a', 'e/m / 1e11'])
generate_table('tab/V502_tab_b', list(zip(D_list.to('cm'), *I_list)), col_fmt=[{'d': 1}] + [{'d': 2}]*len(I_list), headers=['U_b'] + [f"{U_b.to('V').m}V" for U_b in U_b_list])
#TODO: generate_table umschreiben, dass die Pfade auch richtige Pfade sind und nicht build/ prependen…
