import numpy as np
import uncertainties.unumpy as unp
from generate_table import generate_table

nr, a, b, c = np.genfromtxt('messwerte_schieblehre.dat', unpack=True)
generate_table('tab/mess_schieblehre', [[*i] for i in zip(nr, a, b, c)], col_fmt=[{'d': 0}] + [{'d': 1}]*3)
