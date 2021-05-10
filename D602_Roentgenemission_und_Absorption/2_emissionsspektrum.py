import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

import tools

θ, N = np.genfromtxt('data/Emissionsspektrum.dat', unpack=True)
θ *= ureg.deg

peak_indices, _ = find_peaks(N, height=1000)
assert len(peak_indices) == 2

peaks = θ[peak_indices]

print(tools.fmt_compare_to_ref(peaks[1], ureg('22.323 °'), name="θ_Kα"))
print(tools.fmt_compare_to_ref(peaks[0], ureg('20.217 °'), name="θ_Kβ"))
results_half = peak_widths(N, peak_indices, rel_height=0.5)

w_h, l, r = results_half[1:]
# TODO hard-coden ist doof :/
l = (l/10 + 8) * ureg.deg
r = (r/10 + 8) * ureg.deg

print(f"Halbwertsbreiten: {(r-l):.3f}°")

def energie(θ):
    d = ureg('201.4 pm') # Gitterebenenabstand
    return (ureg.h * ureg.c / (2 * d * np.sin(θ.to('rad')))).to('keV')

E = energie(peaks)
ΔE = energie(l)-energie(r)
print(f"Energien für die Peaks: {E:.2f}")
print(f"Energiedifferenzen über die Halbwertsbreiten: {ΔE:.3f}")

print(f"Auflösungsvermögen: {E/ΔE:.2f}")

Z = 29 # für Kupfer
σ_K = (Z - (E/(1*ureg.h * ureg.c * ureg.R_inf) - (((1*ureg.α)**2 * Z**4) / 4))**.5).to('dimensionless')

E_abs = ufloat(8987.96, 15) * ureg('eV') # → NIST
E_α = E[1]
E_β  = E[0]
assert E_α < E_β

R_y = ureg.h * ureg.c * ureg.R_inf # Rydberg-Energie

# etwas lesbarer so, finde ich
def sqrt(x):
    return x**.5
    # return np.sqrt(x)

# nach Formeln von YanickKi
σ_1 = Z - sqrt(E_abs / R_y)
σ_2 = Z - 2 * sqrt((Z - σ_1)**2 - (E_α / R_y))
σ_3 = Z - 3 * sqrt((Z - σ_1)**2 - (E_β  / R_y))

print(f"{σ_1=}")
print(f"{σ_2=}")
print(f"{σ_3=}")


plt.hlines(w_h, l, r, color="red", label='Halbwertsbreiten')
plt.axvline(peaks[0], color='tab:orange', label=r'$K_\beta \;$-Kante')
plt.axvline(peaks[1], color='tab:green', label=r'$K_\alpha \;$-Kante')
# plt.yticks(list(w_h))
# plt.yticks(list(plt.yticks()[0]) + list(w_h))
plt.plot(θ, N, '-')
plt.grid()
plt.xlabel(r'$θ \;/\; °$')
plt.ylabel(r'$N$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot_emissionsspektrum.pdf')
# plt.show()
