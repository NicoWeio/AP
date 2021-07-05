import matplotlib.pyplot as plt
import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

α1, α2 = np.genfromtxt(f'data/Reflexionsgesetz.csv', comments='#', unpack=True, delimiter=',')
α1 *= ureg.deg # Einfallswinkel
α2 *= ureg.deg # Reflexionswinkel

Δα = abs(α1 - α2)
print(f"Δα = {Δα}")
print(f"Mittelwert Δα: {np.mean(Δα):.3f}")


a, b = tools.linregress(α1, α2)
print(f"{a, b=}")
print(tools.fmt_compare_to_ref(a, 1, name='Geradensteigung a'))
plt.plot(α1, α2, 'x', zorder=5, label='Messwerte')
plt.plot(α1, tools.nominal_values(a * α1 + b), label='Regressionsgerade')
plt.plot(α1, α1, color='black', label=r'$\alpha_1 = \alpha_2$')
plt.xlabel(r'$\alpha_1 \mathbin{/} \si{\degree}$')
plt.ylabel(r'$\alpha_2 \mathbin{/} \si{\degree}$')
plt.xticks(α1)
plt.yticks(α2)
plt.grid()
plt.legend()
# plt.gca().set_aspect('equal')
plt.tight_layout()
plt.savefig('build/plt/reflexionsgesetz.pdf')
# plt.show()
