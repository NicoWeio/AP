import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import argrelextrema, find_peaks
from uncertainties import ufloat
import pandas as pd
import tools
from generate_table import generate_table

# T = np.array([296.15, 427.15, 456.15, 458.15, 461.15])
T_orig = ureg.Quantity([23.7, 148, 166.6, 183.8], ureg.degC)
T = T_orig.to(ureg.K).m
print(f"{T=}")
p_Sät = 5.5e7 * np.exp(-6876 / T)

w = (0.0029 / p_Sät) * ureg('cm')

a = ureg('1 cm') # lt. Versuchsanleitung
# a = ureg('2 cm') # → Mampfzwerg
w_soll_min = 1000 # „Hierbei ist zu beachten, dass w etwa um den Faktor 1 000 bis 4000 kleiner als a sein muss, damit eine ausreichende Stoßwahrscheinlichkeit gegeben ist.“

df = pd.DataFrame({'T [°C]': T_orig, 'T [K]': T, 'p_Sät [mbar]': p_Sät, 'w [mm]': w.to('mm'), 'a/w': a/w})
print(df.to_string(index=False))

# generate_table(f'tab/freie_weglaenge', list(zip(T_orig, T, p_Sät, w, a/w)), col_fmt=[{'d': 1}]*2 + [{'d': 5}]*2 + [{'d': 2}])
generate_table(f'tab/freie_weglaenge', list(zip(T_orig, T, p_Sät, w, a/w)), col_fmt=[{'d': n} for n in [1,1,5,6,2]])
