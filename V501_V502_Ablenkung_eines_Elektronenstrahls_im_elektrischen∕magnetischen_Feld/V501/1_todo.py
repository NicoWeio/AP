import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

from generate_table import generate_table
import tools

## Linearer Zusammenhang zwischen der Leuchtpunktverschiebung und Ablenkspannung

plt.figure()
a_list = []
actor_tuple_list = []
U_B_list = [200, 275, 350, 420, 500] * ureg.V

for i, U_B in enumerate(U_B_list):
    D, U_d = np.genfromtxt(f'V501/data/{U_B.m}V.dat', unpack=True)
    U_d *= ureg.V
    D *= ureg.inch / 4

    D, U_d = tools.remove_nans(D, U_d)

    a, b = tools.linregress(U_d, D)
    a_list.append(a.to('mm/V'))
    print(f"{a.to('mm/V')=}")

    plt_vals, = plt.plot(U_d, D.to('cm'), 'x', label='Messwerte', color=f"C{i}")
    plt_regress, = plt.plot(U_d, tools.nominal_value(a)*U_d+tools.nominal_value(b), '-', label='Regressionsgerade', color=f"C{i}")
    actor_tuple_list.append((plt_vals, plt_regress))
a_list = tools.pintify(a_list)

plt.grid()
plt.xlabel(r'$U_d \mathbin{/} \si{\volt}$')
plt.ylabel(r'$D \mathbin{/} \si{\centi\meter}$')
plt.yticks(list(range(0, 9)) * ureg.inch / 4)
plt.legend(actor_tuple_list, [r'$U_\text{B} = \SI{' f'{U_B.m}' r'}{\volt}$' for U_B in U_B_list])
plt.tight_layout()
plt.savefig('build/plt/V501_1.pdf')

# generate_table('c_dings', list(zip(U_B_list.m, tools.pintify(a_list))))


print("\n\nApparaturkonstante:")
a_list_nominal = tools.nominal_values(tools.pintify(a_list))
m, n = tools.linregress(1 / U_B_list, a_list_nominal)

d = ureg('0.38 cm') # Abstand der Y-Ablenkplatten zueinander
p = ureg('1.9 cm') # Länge der Y-Ablenkplatten
L = ureg('1.03 cm') + ureg('14.3 cm') # Abstand *Beginn* der Y-Ablenkplatten → Leuchtschirm
m_theo = (p*L)/(2*d)

print(tools.fmt_compare_to_ref(m, m_theo, unit='mm', name='Apparaturkonstante'))

plt.figure()
plt.plot(1 / U_B_list.to('kV'), a_list_nominal, 'x', label='Werte') #label-Name lol
plt.plot(1 / U_B_list.to('kV'), tools.nominal_value(m)*(1 / U_B_list)+tools.nominal_value(n), '-', label='Regressionsgerade')
plt.grid()
plt.xlabel(r'$\sfrac{1}{U_\text{b}} \mathbin{/} \si{\per\kilo\volt}$')
plt.ylabel(r'$\sfrac{D}{U_\text{d}} \mathbin{/} \si{\centi\meter\per\volt}$')
# plt.legend() # hier vllt. wirklich keine Legende…
plt.tight_layout()
plt.savefig('build/plt/V501_2.pdf')

print("\n\nAmplitude:")
a = a_list[np.argwhere(U_B_list == ureg('420 V'))[0][0]]
print(f"{a=}")
D = 1/2 * ureg('1/4 inch') # Amplitude: eine halbe Skaleneinheit
U_A = D / a
print(f"{U_A=}")
