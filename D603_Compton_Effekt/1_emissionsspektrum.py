# Übernommen aus D602 – die gegebenen Daten sind 1:1 dieselben.

import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

import tools

θ, N = np.genfromtxt('data/EmissionCu.dat', unpack=True)
θ *= ureg.deg

peak_indices = find_peaks(N, height=1000)[0]
assert len(peak_indices) == 2

θ_Kβ, θ_Kα = θ[peak_indices]

θ_Kα_lit = ureg('22.323 °')
θ_Kβ_lit = ureg('20.217 °')

print(tools.fmt_compare_to_ref(θ_Kα, θ_Kα_lit, name='θ_Kα'))
print(tools.fmt_compare_to_ref(θ_Kβ, θ_Kβ_lit, name='θ_Kβ'))

def energie(θ):
    d = ureg('201.4 pm') # Gitterebenenabstand
    return (ureg.h * ureg.c / (2 * d * np.sin(θ))).to('keV')

E_Kα, E_Kβ = energie(θ_Kα), energie(θ_Kβ)
assert E_Kα < E_Kβ

print(tools.fmt_compare_to_ref(E_Kα, energie(θ_Kα_lit), name='E_Kα'))
print(tools.fmt_compare_to_ref(E_Kβ, energie(θ_Kβ_lit), name='E_Kβ'))

plt.plot(θ, N, '-o', zorder=5, label='Messwerte')
plt.axvline(θ_Kβ, color='tab:orange', label=r'$K_\beta$-Kante')
plt.axvline(θ_Kα, color='tab:green', label=r'$K_\alpha$-Kante')
plt.grid()
plt.xlabel(r'$θ \mathbin{/} \si{\degree}$')
plt.ylabel(r'$N$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/emissionsspektrum.pdf')
# plt.show()
