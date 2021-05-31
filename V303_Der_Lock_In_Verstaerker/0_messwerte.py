import numpy as np
from generate_table import generate_table

for name, unit in [('phasen', 'V'),('phasen_noise', 'mV')]:
    φ, U = np.genfromtxt(f'{name}.dat', unpack=True)
    # Die Datendateien sind nicht sortiert, sondern geben unsere Messreihenfolge wieder.
    φ, U = zip(*sorted(zip(φ, U)))
    generate_table(f'tab/{name}', [[*i] for i in zip(φ, U)], col_fmt=[{'d': 0},{'d': 1}])

d, U = np.genfromtxt('led.dat', unpack=True)
# Wir haben ohnehin nur DistanzUNTERSCHIEDE gemessen, daher können wir auch einfach bei 0 anfangen.
# d -= min(d)
generate_table('tab/led', [[*i] for i in zip(d, U)], col_fmt=[{'d': 1},{'d': 2}])
