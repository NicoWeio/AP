import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks
import tools

def import_data(T):
    U_A, I_A = np.genfromtxt(f'build/dat/energieverteilung_{str(T).replace(".", "_")}.csv', comments='#', unpack=True, delimiter=',')
    U_A *= ureg.V # Bremsspannung
    I_A *= ureg.nA
    return U_A, I_A

data = {T: import_data(T) for T in [23.7, 148]}

plt.figure('Integrale Energieverteilung')
for T, (U_A, I_A) in data.items():
    plt.plot(U_A, I_A, 'x-', label='\SI{' f'{T}' '}{\celsius}')
plt.xlabel(r'$U_\text{A} \mathbin{/} \si{\volt}$')
plt.ylabel(r'$I_\text{A}$')
plt.yticks([])
plt.grid()
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('build/plt/energieverteilung_int.pdf')


plt.figure('Differenzielle Energieverteilung')
for T, (U_A, I_A) in data.items():
    print(f"{T=}")
    def differentiate(U_A, I_A):
        U_A_middle = (U_A[1:] + U_A[:-1]) / 2 # Wir nehmen die x-Mitte der jeweils betrachteten zwei Datenpunke.
        U_A_diff = np.diff(U_A)
        I_A_diff = np.diff(I_A)
        steigung = I_A_diff / U_A_diff
        return U_A_middle, steigung

    # weniger Werte = besser?
    select_every = 3
    U_A_selection, I_A_selection = U_A[::select_every], I_A[::select_every]
    if T == 148:
        select_start = 5 # da war der XY-Schreiber ausgerutscht…
        U_A_selection, I_A_selection = U_A[select_start::select_every], I_A[select_start::select_every]

    # def min_xy(x, y):
    #     argmin = np.argmin(y)
    #     return x[argmin], y[argmin]
    # print(f"absolute Minimum (selection): {min_xy(diff_U_A_selection, diff_I_A_selection)}")

    diff_U_A_selection, diff_I_A_selection = differentiate(U_A_selection, I_A_selection)
    argmindex = find_peaks(-diff_I_A_selection.m, width=3)[0]
    print(f"relatives Minimum (selection): {diff_U_A_selection[argmindex], diff_I_A_selection[argmindex]}")
    assert len(argmindex) == 1

    U_B = ureg('11 V') # Beschleunigungsspannung; sollte für diesen Versuchsteil konstant so eingestellt sein
    K = U_B - diff_U_A_selection[argmindex]
    print(f"{K=}")

    plt.plot(diff_U_A_selection, diff_I_A_selection, 'x-', label='\SI{' f'{T}' '}{\celsius}')
    # if T == 148:
    #     plt.plot(*differentiate(U_A, I_A), 'x', color='grey', label=f"{T} °C – alle Werte")
    # plt.plot(diff_U_A_selection[argmindex], diff_I_A_selection[argmindex], 'x', color='red', label=f"Maxima")
plt.xlabel(r'$U_\text{A}\mathbin{/} \si{\volt}$')
plt.ylabel(r"${I_\text{A}}'$")
plt.yticks([])
plt.grid()
plt.legend(loc='lower left')
plt.tight_layout()
plt.savefig('build/plt/energieverteilung_diff.pdf')
# plt.show()
