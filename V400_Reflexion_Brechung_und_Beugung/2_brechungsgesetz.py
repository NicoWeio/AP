import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

α, β = np.genfromtxt(f'data/Brechungsgesetz.csv', comments='#', delimiter=',', unpack=True)
α *= ureg.deg # Einfallswinkel
β *= ureg.deg # Brechungswinkel

n = np.sin(α) / np.sin(β)
# n1 = 1.000292 # Brechungsindex Luft
# n2 = n1 * np.sin(α) / np.sin(β)
n_avg = tools.ufloat_from_list(n.m)
# print(f"Mittelwert n: {n_avg:.3f}")

n_lit = 1.489 * ureg.dimensionless
print(tools.fmt_compare_to_ref(n_avg, n_lit), 'Brechungsindex')

v = (ureg.c / n_avg).to('m/s')
# v = (ureg.c * np.sin(β) / np.sin(α)).to('m/s')
print(f"Lichtgeschwindigkeit in Plexiglas: {v}")
