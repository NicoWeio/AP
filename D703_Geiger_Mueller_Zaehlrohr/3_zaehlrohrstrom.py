import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
import generate_table

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

U, I = np.genfromtxt('Zaehlrohrstrom.dat', unpack=True)
U *= ureg('V')
I = unp.uarray(I, 0.05) * ureg('µA')
# "Die Ablesegenauigkeit am Amperemeter beträgt ∆I = 0.05μA."

print(f"{I=}")

U2, N = np.genfromtxt('Kennlinie.dat', unpack=True)
N = [N for U2, N in zip(U2, N) if U2*ureg('V') in U]

t = ureg('60 s')
N /= t

# "Aus dem mittleren Zählrohrstrom I" !(?)
e0 = ureg.elementary_charge
Z = I/(e0*N)
Z.ito('dimensionless')

print(f"<Z>={np.mean(Z)}")
# print(f"Z={Z.to('dimensionless')}")

generate_table.generate_table('table_zaehlrohrstrom', [*zip(U,N,I,(Z/1e10))], col_fmt=[{'d': 0},{'d': 1},{'d': (1,2)},{'d': (2,2)}])

slope, intercept, r_value, p_value, std_err = sp_stats.linregress(U.m, unp.nominal_values(Z))
slope *= ureg('1/V')

plt.errorbar(U.to('V'), unp.nominal_values(Z), fmt='x', yerr=unp.std_devs(Z), label='freigesetzte Ladungen pro eingefallenem Teilchen')
plt.plot(U, slope * U + intercept, label='Regressionsgerade')
plt.xlabel(r"$U \;/\; V$")
plt.ylabel(r"$Z$")
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2.pdf')
# plt.show()
