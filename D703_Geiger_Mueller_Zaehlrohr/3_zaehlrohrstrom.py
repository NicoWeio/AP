import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import generate_table
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

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

generate_table.generate_table('table_zaehlrohrstrom', [*zip(U,N,I,(Z/1e10))], col_fmt=[{'d': 0},{'d': 1},{'d': (1,2)},{'d': (2,2)}])

slope, intercept = tools.linregress(U, tools.nominal_values(Z))

with tools.plot_context(plt, 'V', 'dimensionless', 'U', 'Z') as plt2:
    plt2.plot(U, Z, fmt='x', label='freigesetzte Ladungen pro eingefallenem Teilchen')
    plt2.plot(U, slope * U + intercept, show_yerr=False, label='Regressionsgerade')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot2.pdf')
# plt.show()
