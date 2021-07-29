import numpy as np
import matplotlib.pyplot as plt
import uncertainties as unc
import uncertainties.unumpy as unp
from uncertainties import ufloat
from scipy.optimize import curve_fit
import scipy.constants as const
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import generate_table
import tools



# Daten einlesen
U, I = np.genfromtxt(f"gelb.dat", unpack=True)
# Die Datendateien sind nicht sortiert, sondern geben unsere Messreihenfolge wieder. Das würde sonst stören.
U, I = zip(*sorted(zip(U, I)))
U = list(U) * ureg('V')
I = list(I) * ureg('nA')

fig, ax = plt.subplots()
ax.plot(U.m, I.m, "x", label='Messwerte Gelb', color='orange')
ax.grid() # ?
axin2 = ax.inset_axes([5, 1, 15, 3], transform = ax.transData)
axin2.plot(U.m, I.m, "x", color='orange')
# axin2.set_xlim(-2, 3)
# axin2.set_ylim(-0.25, 1.2)
axin2.set_xlim(-0.25, 1.2)
axin2.set_ylim(-0.025, 0.4)
axin2.grid()

plt.gca().indicate_inset_zoom(axin2, edgecolor="black")

plt.xlabel(r'$U \mathbin{/} \si{\volt}$')
plt.ylabel(r'$I \mathbin{/} \si{\nano\ampere}$')
plt.legend()
plt.tight_layout()
plt.savefig("build/plot_gelb_full.pdf")
# plt.show()
