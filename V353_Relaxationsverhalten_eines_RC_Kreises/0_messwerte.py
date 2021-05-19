import numpy as np
import uncertainties.unumpy as unp
import generate_table

t, U = np.genfromtxt('mess_1.dat', unpack=True)
U -= U[-1] # das Minimum von U soll 0 sein
generate_table.generate_table('tab/mess_1', [[*x] for x in zip(t, U)], col_fmt=[{'d': 1},{'d': 1}])


f, U = np.genfromtxt('mess_2.dat', unpack=True)
U -= U[-1] # das Minimum von U soll 0 sein
generate_table.generate_table('tab/mess_2', [[*x] for x in zip(f, U)], col_fmt=[{'d': 0},{'d': 1}])
