import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat, unumpy as unp
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

def fit_fn(t, U_0, RC):
    return U_0 * np.exp(-t / RC)

t, U = np.genfromtxt('mess_1.dat', unpack=True)
t *= ureg('ms')
U *= ureg('V')

U -= U[-1] # Das Minimum von U soll 0 sein.
# Das macht aber Probleme beim Logarithmieren,
# weshalb im Folgenden häufig mit `[:-1]` das letzte Wertepaar ignoriert wird.
# Besser misst man U_0 vernünftig, um stets Werte >0 für U zu bekommen.

ln_U = np.log(U.m[:-1])
a, b = tools.linregress(t[:-1], ln_U * ureg('dimensionless'))

# Das Logarithmieren macht meine Pint-Zaubereien wertlos… :/
# Diese Einheiten müssen manuell überprüft werden.
RC = (-1/a).m * ureg('ms')
print(f"{a=}, {b=}")
print(f"{RC=}")

plt.plot(t, U, 'x', label='Messwerte')
plt.plot(t[:-1], np.exp(unp.nominal_values(a*t[:-1]+b)), label='Regressionsgerade')
plt.yscale('log')
plt.xlabel(r'$t \;/\; ms$')
plt.ylabel(r'$\ln(U)$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/1_rc_via_t.pdf')
# plt.show()
