import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

from generate_table import generate_table

U_b_list = [200, 275, 350, 420, 500]
I_table = [np.genfromtxt(f'data/{U_b}V.dat', unpack=True)[1] for U_b in U_b_list]
D_list = [n for n in range(max(len(col) for col in I_table))] * ureg.inch / 4

generate_table(f'mess_1', list(zip(D_list.to('cm'), *I_table)), col_fmt=[{'d': 1}] + [{'d': 2}]*len(U_b_list), headers=['D/cm'] + list(map(str, U_b_list)))
