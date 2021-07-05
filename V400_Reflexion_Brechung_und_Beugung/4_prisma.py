import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools
from generate_table import generate_table

α1, α2_grün, α2_rot = np.genfromtxt(f'data/Prisma.csv', comments='#', delimiter=',', unpack=True)
α1 *= ureg.deg # Einfallswinkel
α2_grün *= ureg.deg # Austrittswinkel
α2_rot *= ureg.deg # Austrittswinkel

# assert all(α1 >= 10 & α1 <= 60)…

def analyze(α2):
    γ = ureg('60 °') # brechender Winkel; lt. Versuchsanleitung
    n_lit = 1.510 * ureg.dimensionless # Brechungsindex für Kronglas; aus der Vorbereitungsaufgabe
    δ = (α1 + α2) - γ # Ablenkung
    print(f"{δ=}")
    assert all(δ < ureg('120 °')) # sanity check – siehe Abbildung. Größere Werte ergeben keinen Sinn.
    return δ

print('grün:')
δ_grün = analyze(α2_grün)
print('\n' 'rot:')
δ_rot = analyze(α2_rot)
print('\n' f'{δ_grün - δ_rot=}')

generate_table('tab/prisma', list(zip(α1, α2_grün, δ_grün, α2_rot, δ_rot, (δ_grün - δ_rot))), col_fmt=[{'d': 0}]+[{'d': 2}]*5)
