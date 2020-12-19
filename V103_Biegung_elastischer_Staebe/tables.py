import numpy as np
import generate_table

for type in ['einseitig_eckig', 'einseitig_rund', 'beidseitig_rund']:
    x, D0, Dm = np.genfromtxt(type+'.dat', unpack=True)
    D = D0 - Dm
    generate_table.generateTable('table_'+type, [[*i] for i in zip(x, D0, Dm, D)])
