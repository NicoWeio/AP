import numpy as np

from generate_table import generate_table

names = ['Bragg', 'Emissionsspektrum'] + ['Zink', 'Gallium', 'Brom', 'Rubidium', 'Strontium', 'Zirkonium']

data = {}

for i, name in enumerate(names):
    θ, N = np.genfromtxt(f'data/{name}.dat', unpack=True)
    generate_table(f'table_mess_{name.lower()}', [[*i] for i in zip(θ, N)], col_fmt=[{'d': 1}, {'d': 0}])
