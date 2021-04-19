import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.stats as sp_stats
import generate_table

from tools import *

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

# Speisespannung
U_Sp = ureg('4.5 V') # irgendwas von 4.5 steht in unseren Notizen…
# U_Sp = ureg('7.526 V') # der Wert, der Σabs(χU_rel_err) minimiert

F = ureg('86.6 mm²') # Spulenquerschnitt, lt. Versuchsanleitung
R31 = 998 * ureg('Ω') # Vorwiderstand, lt. dlmsr – bei uns auch vorhanden?

data = [
{
    'name': 'Dy2O3',
    'theoriewert': 0.0254, # eigener
    'R_0_raw': [514, 495, 497],
    'R_m_raw': [157, 168, 159],
    'U_0_raw': [2.41, 2.3, 2.35],
    'U_m_raw': [8.62, 7.8, 7.81],
    'm': ureg('14.38 g'),
    'l': ufloat_from_list([17.75, 17.8, 17.78]) * ureg('cm'),
    'ρ': ureg('7.8 g/cm³'),
},
{
    'name': 'Nd2O3',
    'theoriewert': 0.003, # eigener
    'R_0_raw': [489, 485, 495],
    'R_m_raw': [464, 465, 466],
    'U_0_raw': [2.25, 2.39, 2.39],
    'U_m_raw': [2.31, 2.39, 2.41],
    'm': ureg('9.0 g'),
    'l': ufloat_from_list([17.9, 17.9, 17.85]) * ureg('cm'),
    'ρ': ureg('7.24 g/cm³'),
},
]


def analyse(data):
    print(f"{data['name']} ↓")

    m = data['m']
    l = data['l']
    print(f"{l=}")
    ρ = data['ρ']

    Q_real = m / (ρ * l)
    Q_real.ito('cm²')
    print(f"{Q_real=}")

    # 1 auf dem Anzeigewerk des Potentiometers entspricht 5 [m!?]Ω.

    R_0 = np.array(data['R_0_raw']) * 5 * ureg('mΩ')
    R_m = np.array(data['R_m_raw']) * 5 * ureg('mΩ')
    U_0 = np.array(data['U_0_raw']) * ureg('mV')
    U_m = np.array(data['U_m_raw']) * ureg('mV')

    # Anscheinend haben wir R3 statt R4 oder umgekehrt gemessen.
    # Da diese aber über *ein* Potentiometer laufen,
    # lässt sich der jeweils andere Widerstand über das Komplement einfach berechnen.
    R_0 = ureg('1000 mΩ') * 5 - R_0
    R_m = ureg('1000 mΩ') * 5 - R_m

    ΔR_list = R_m - R_0
    ΔU_list = U_m - U_0

    generate_table.generate_table(f"table_{data['name']}_auswertung", [[*i] for i in zip(R_0.to('Ω'), R_m.to('Ω'), ΔR_list.to('Ω'), U_0, U_m, ΔU_list)], col_fmt=[{'d': 2}]*6)

    ΔR = pint_ufloat(ΔR_list, 'mΩ', ureg)
    ΔU = pint_ufloat(ΔU_list, 'mV', ureg)

    R_0_mittel = pint_ufloat(R_0, 'mΩ', ureg)
    χR = (2*ΔR*F)/((R_0_mittel+R31)*Q_real)
    χR.ito('dimensionless')

    χU = (4*F*ΔU)/(Q_real*U_Sp)
    # komplette Formel – sollte nach Versuchsanleitung nicht nötig sein…
    # χU = (U_Br/U_Sp) * ((4*l)/(ω*μ0*(n**2)*Q)) * sqrt((R**2) + (w**2) * (μ0*((n**2)/l)*F)**2)
    χU.ito('dimensionless')

    χT = data['theoriewert']

    χR_rel_err = ((χT - χR)/χT)
    χR_rel_err.ito('dimensionless')
    χU_rel_err = ((χT - χU)/χT)
    χU_rel_err.ito('dimensionless')

    print(f'{χR=}')
    print(f'{χU=}')
    print(f'{χT=}')

    print("Fehler χR:", f'{(χR_rel_err * 100).n:.2f} %')
    print("Fehler χU:", f'{(χU_rel_err * 100).n:.2f} %')

for d in data:
    analyse(d)
    print('–––')
