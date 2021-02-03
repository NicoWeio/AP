import numpy as np
import uncertainties.unumpy as unp
import generate_table

for stoff in ['Rhodium', 'Vanadium']:
    t, N = np.genfromtxt(f'{stoff}.dat', unpack=True)
    N = unp.uarray(N, unp.sqrt(N))
    generate_table.generate_table(f'table_{stoff.lower()}', [*zip(t, N)], col_fmt=[{'d': 0}, {'d': (0,1)}])
