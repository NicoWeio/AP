import numpy as np
import uncertainties.unumpy as unp
import generate_table

U, N = np.genfromtxt('Kennlinie.dat', unpack=True)

N = [int(n) for n in N]
N = unp.uarray(N, unp.sqrt(N))

U2, I = np.genfromtxt('Zaehlrohrstrom.dat', unpack=True)
# Die Ablesegenauigkeit am Amperemeter beträgt ∆I = 0.05μA.

data = [{'U': U, 'N': N} for U,N in zip(U,N)]

for d in data:
    d.update(('I', i) for u2, i in zip(U2, I) if d['U'] == u2)

table_data = list([[int(d['U']), d['N'], d.get('I', '-')] for d in data])

print(table_data)

generate_table.generate_table('table_messwerte', table_data, col_fmt=[{'d': 0},{'d': (0,0)},{'d': 1}])
