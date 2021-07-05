import tools
from generate_table import generate_table
import numpy as np
from uncertainties import ufloat
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

# Für diesen Aufgabenteil haben wir keine Messungen durchgeführt.

# TODO: schöner aus Aufg. 2 übernehmen!
n = 1.45
d = ureg('5.85 cm')  # lt. Versuchsanleitung


def calc_s(α):
    β = np.arcsin(np.sin(α) / n)  # Brechungswinkel aus dem umgeformten Brechungsgesetz
    s = d * np.sin(α - β) / np.cos(β)
    return s


α_table = tools.linspace(*([0, 90] * ureg('°')), 10)
generate_table(f'tab/strahlversatz', list(zip(α_table, calc_s(α_table))), col_fmt=[{'d': 0}, {'d': 2}])

α_plot = tools.linspace(*([-90, 90] * ureg('°')), 180)
plt.plot(α_plot, calc_s(α_plot))
plt.xlabel(r'$\alpha \mathbin{/} \si{\degree}$')
plt.ylabel(r'$s \mathbin{/} \si{\centi\meter}$')
plt.grid()
plt.tight_layout()
plt.savefig('build/plt/strahlversatz.pdf')
# plt.show()
