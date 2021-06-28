import tools
from uncertainties import ufloat
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()


def analyze(T, manual_max_indices):
    print(f"→ {T=}")
    U_B, I_A = np.genfromtxt(f'build/dat/franck_hertz_{str(T).replace(".", "_")}.csv', comments='#', unpack=True, delimiter=',')
    U_B *= ureg.V # Beschleunigungsspannung
    I_A *= ureg.nA

    # Achtung: distance/width werden in *samples* angegeben!
    # Damit ist keine weitere Generalisierung möglich.
    max_indices = find_peaks(I_A.m, height=1.5, width=1)[0]
    # max_indices = find_peaks(I_A.m, height=1.5, distance=15)[0]

    if manual_max_indices:
        max_indices = np.sort(np.unique(np.concatenate([max_indices, manual_max_indices])))

    print(f'{max_indices=}')
    print(f'Peaks: \n-U_B: {U_B[max_indices]:.3f}\n-I_A: {I_A[max_indices]:.3f}')

    # Abstand der relativen Maxima
    dif = np.diff(U_B[max_indices].to('V').m) * ureg.V
    dif_avg = tools.ufloat_from_list(dif.m) * ureg.V
    print(f'Abstände: {dif:.3f}', )
    print('mittlerer Abstand:', dif_avg)
    print(tools.fmt_compare_to_ref(dif_avg * ureg.e, ureg('4.9 eV'), unit='eV', name='→ Anregungsenergie'))
    λ = ureg.c * ureg.h / (dif_avg * ureg.e)
    print('λ =', λ.to('nm'))

    # Ohne Berücksichtigung des Kontaktpotentials würde man erwarten,
    # dass der mittlere Abstand gleich dem Abstand des ersten Maximums von der 0 ist –
    # schließlich müssten die Elektronen bei dif_avg gerade zum ersten Mal
    # eine ausreichende Beschleunigung erfahren haben, um ein Hg-Atom zu ionisieren.
    # Das tatsächliche Beschleunigungspotential (und somit die Energie des Elektrons)
    # ist wegen des Kontaktpotentials aber geringer.
    # Das verschiebt die Franck-Hertz-Kurve nach rechts,
    # was wir uns folgendermaßen zu Nutze machen können:
    print('1. Maximum: ', U_B[max_indices[0]])
    print('Kontaktpotential: ', U_B[max_indices[0]] - dif_avg)
    print('Kontaktpotential (Modulo): ', U_B[max_indices[0]] % dif_avg) # sinnvoll, wenn das wirklich erste Maximum (bei 4.9 V) nicht bestimmt werden konnte

    plt.figure(f'{T=}')
    plt.plot(U_B, I_A, 'x-', label='Messwerte')
    plt.plot(U_B[max_indices], I_A[max_indices], 'xr', label='Maxima')

    for i in max_indices:
        plt.axvline(U_B[i], color='grey', linestyle='--', alpha=0.5)
    for k in range(len(max_indices) - 1):
        i1 = max_indices[k]
        i2 = max_indices[k + 1]
        plt.arrow(*(U_B[i1], I_A[i2]), *(U_B[i2] - U_B[i1], 0))
        plt.annotate(f'{(U_B[i2] - U_B[i1]).to("V").m:.1f} V', (U_B[i1], I_A[i2] + ureg('0.15 nA')))

    # plt.grid()
    plt.xlabel(r'$U_\text{A} \mathbin{/} \si{\volt}$')
    plt.ylabel(r'$I_\text{A}$')
    plt.yticks([])
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'build/plt/franck_hertz_{str(T).replace(".", "_")}.pdf')
    # plt.show()


# for T, manual_max_indices in [(166.6, []), (183.8, [7])]:
for T, manual_max_indices in [(166.6, []), (183.8, [])]:
    analyze(T, manual_max_indices)
    print('\n')
