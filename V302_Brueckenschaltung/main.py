import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
#TODO
import sys

# import generate_table

nu, UBr = np.genfromtxt('Daten_e.dat', unpack=True)
# Ubr = np.array([b/1000 if u == "mV" else b for (b,u) in zip(UBr, unit) ])
US = 10 #TODO: gemogelt

quot = UBr / US

# ν0 ist diejenige Frequenz, bei der die Brückenspannung minimal wird
#TODO: programmatisch finden
nu0 = 226

omega = nu / nu0

# ––––––––

def quotTheorie(w):
    return np.sqrt((1/9)*((w**2-1)**2)/((1-w**2)**2 + 9*w**2))

omegaLin = np.linspace(omega.min(), omega.max(), 1000)

# ––––––––

plt.plot(omega, quot, '.', label="Messwerte")
plt.plot(omegaLin, quotTheorie(omegaLin), label="Theorie")
plt.xlabel(r"$\Omega = \nu / \nu_0$")
plt.ylabel(r"$U_{Br} / U_{S}$")
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot1.pdf')
# plt.show()

plt.clf()

omegaSection = omega[3:-10]
quotSection = quot[3:-10]
plt.plot(omegaSection, quotSection, '.', label="Messwerte")
omegaLin2 = np.linspace(omegaSection.min(), omegaSection.max(), 1000)
plt.plot(omegaLin2, quotTheorie(omegaLin2), label="Theorie")
plt.xlabel(r"$\Omega = \nu / \nu_0$")
plt.ylabel(r"$U_{Br} / U_{S}$")
plt.xscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2.pdf')
# plt.show()
