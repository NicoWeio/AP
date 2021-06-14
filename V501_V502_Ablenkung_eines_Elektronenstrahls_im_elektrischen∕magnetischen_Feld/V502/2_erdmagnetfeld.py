import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

import tools

N = 20 # Windungszahl
R = ureg('0.282 m') # Spulenradius
L = ureg('0.175 m') # Der Weg L der Elektronen, auf dem das Magnetfeld wirksam ist, reicht etwa von der Beschleunigungselektrode bis zum Leuchtschirm. Er kann aus der Konstruktionszeichnung der Röhre entnommen werden (siehe V501; Abb.5).
B_lit = ureg('49 µT')

def B(I):
    return (ureg.mu_0 * (8 / 125**.5) * (N / R) * I).to('µT')

I = tools.ufloat_from_list([0.49, 0.46, 0.45]) * ureg.A
print(f"{I=}")

print("ohne Inklinationswinkel:")
B_hor = B(I) # Horizontalkomponente des Erdmagnetfelds
print(f"{B_hor=}")

print("mit Inklinationswinkel:")
φ = ureg('54 °') # Inklinationswinkel
B_total = B_hor / np.sin(φ) # Totalintensität
print(tools.fmt_compare_to_ref(B_total, B_lit))

φ_opti = np.arcsin(tools.nominal_value(B_hor / B_lit)).to('°')
print(f"{φ_opti=}")
B_total_opti = B_hor / np.sin(φ_opti) # Totalintensität
print(tools.fmt_compare_to_ref(B_total_opti, B_lit))
