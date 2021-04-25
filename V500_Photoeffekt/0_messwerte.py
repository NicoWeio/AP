import numpy as np
import uncertainties.unumpy as unp
from generate_table import generate_table

for color in ['gelb', 'gruen', 'violett', 'ultraviolett']:
    U, I = np.genfromtxt(f'{color}.dat', unpack=True)
    # Die Datendateien sind nicht sortiert, sondern geben unsere Messreihenfolge wieder. Das würde sonst stören.
    U, I = zip(*sorted(zip(U, I)))
    generate_table(f'table_{color}', [[*i] for i in zip(U, I)], col_fmt=[{'d': 2},{'d': 3}])
