import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import scipy as sp
import uncertainties.unumpy as unp

from generate_table import generate_table
import tools

def get_T(i, name):
    # Schwingungsdauern, jeweils von uns beiden gemessen
    T1, T2 = np.genfromtxt(f'data/{i}_{name}.dat', unpack=True)
    T = np.concatenate([T1, T2])
    return T

T_1_plus_links = get_T(1, 'gleichsinnig_links') / 5
T_1_plus_rechts = get_T(1, 'gleichsinnig_rechts') / 5
T_2_plus_links = get_T(2, 'gleichsinnig_links') / 5
T_2_plus_rechts = get_T(2, 'gleichsinnig_rechts') / 5
generate_table(f'tab/gleichsinnig', [[*x] for x in zip(T_1_plus_links, T_1_plus_rechts, T_2_plus_links, T_2_plus_rechts)], col_fmt=[{'d': 2}]*4)


T_1_minus = get_T(1, 'gegensinnig') / 5
T_2_minus = get_T(2, 'gegensinnig') / 5
generate_table(f'tab/gegensinnig', [[*x] for x in zip(T_1_minus, T_2_minus)], col_fmt=[{'d': 2}]*2)

T_1_gekoppelt_periode = get_T(1, 'gekoppelt_periode') / 5
T_1_gekoppelt_schwebung = get_T(1, 'gekoppelt_schwebung')
T_2_gekoppelt_periode = get_T(2, 'gekoppelt_periode') / 5
T_2_gekoppelt_schwebung = get_T(2, 'gekoppelt_schwebung')
generate_table(f'tab/gekoppelt', [[*x] for x in zip(T_1_gekoppelt_periode, T_1_gekoppelt_schwebung, T_2_gekoppelt_periode, T_2_gekoppelt_schwebung)], col_fmt=[{'d': 2}]*4)
