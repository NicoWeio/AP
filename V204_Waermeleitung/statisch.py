import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
import pint
ureg = pint.UnitRegistry()
ureg.autoconvert_offset_to_baseunit = True
ureg.setup_matplotlib()
from generate_table import generate_table

from pint_tools import pint_range, pint_max, pint_min, pintify

def index_to_seconds(i, vals_per_second):
    return (i / vals_per_second).to('seconds')
def seconds_to_index(s, vals_per_second):
    return int((s * vals_per_second).to('dimensionless'))

vals_per_second = 1/5 * ureg('1 / second')

indices_statisch, T1, T4, T5, T8, T2, T3, T6, T7 = np.genfromtxt('Daten_statisch.txt', unpack=True)
indices_statisch = index_to_seconds(indices_statisch, vals_per_second)

# TODO irgendwie schöner machen…
T1 *= ureg.celsius
T2 *= ureg.celsius
T3 *= ureg.celsius
T4 *= ureg.celsius
T5 *= ureg.celsius
T6 *= ureg.celsius
T7 *= ureg.celsius
T8 *= ureg.celsius

print("max_t", indices_statisch[-1])

def plot_common(plt):
    plt.xlabel(r'$t \mathbin{/} \si{\second}$')
    plt.ylabel(r'$T \mathbin{/} \si{\celsius}$')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.axvline(x=(700 * ureg.seconds), linewidth=0.5, linestyle="--", color='grey')

plt.figure("T1, T4, T5, T8")
plt.plot(indices_statisch, T1, label='Messing (breit)')
plt.plot(indices_statisch, T4, label='Messing (schmal)')
plt.plot(indices_statisch, T5, label='Aluminium')
plt.plot(indices_statisch, T8, label='Edelstahl')
plot_common(plt)
plt.savefig('build/plot_statisch_alle.pdf')
# plt.show()

#################

the_index = seconds_to_index(ureg('700 seconds'), vals_per_second)

temps_at_700 = [the_T[the_index] for the_T in [T1, T4, T5, T8]]
print(f"{temps_at_700=}")

#################

def waermestrom(kappa, A, dT_dx):
    # print(f"{dT_dx=}")
    wärmestrom = - kappa * A * dT_dx
    # soll immer positiv sein
    wärmestrom = abs(wärmestrom)
    return wärmestrom.to('watt')

waermestrom_messing_breit = waermestrom(
    ureg('120 W/(m·K)'),
    ureg('1.2 cm') * ureg('0.4 cm'),
    (T2 - T1) / ureg('3 centimeters'))

waermestrom_messing_schmal = waermestrom(
    ureg('120 W/(m·K)'),
    ureg('0.7 cm') * ureg('0.4 cm'),
    (T3 - T4) / ureg('3 centimeters'))

waermestrom_aluminium = waermestrom(
    ureg('237 W/(m·K)'),
    ureg('1.2 cm') * ureg('0.4 cm'),
    (T6 - T5) / ureg('3 centimeters'))

waermestrom_edelstahl = waermestrom(
    ureg('15 W/(m·K)'),
    ureg('1.2 cm') * ureg('0.4 cm'),
    (T7 - T8) / ureg('3 centimeters'))

the_table = [[int(x[0].to('seconds').m), *(x[1:])] for x in zip(indices_statisch, waermestrom_messing_breit, waermestrom_messing_schmal, waermestrom_aluminium, waermestrom_edelstahl) if (x[0] in ([30,60,120,240,480] * ureg.seconds))]

generate_table('table_waermestroeme', the_table)

# plt.figure("Wärmestrom")
# plt.plot(indices_statisch, waermestrom_messing_breit)
# plt.show()


#################

plt.figure("T2 - T1 & T7 - T8")
plt.plot(indices_statisch, T2 - T1, label='T2 - T1 (Messing, breit)')
plt.plot(indices_statisch, T7 - T8, label='T7 - T8 (Edelstahl)')
plot_common(plt)
plt.ylabel("$\Delta T \mathbin{/} \si{\celsius}$")
plt.savefig('build/plot_statisch_tdiff.pdf')
# plt.show()
