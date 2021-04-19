import numpy as np
import uncertainties.unumpy as unp
import generate_table

ν, U_A = np.genfromtxt('Filterkurve.dat', unpack=True)

generate_table.generate_table('table_filterkurve', [[*i] for i in zip(ν, U_A)], col_fmt=[{'d': 2},{'d': 1}])
