import numpy as np
from generate_table import generate_table

θ, N = np.genfromtxt('data/EmissionCu.dat', unpack=True)
generate_table(f'tab/mess_emissionsspektrum', list(zip(θ, N)), col_fmt=[{'d': 1},{'d': 0}])

# –––

θ_Al, N_Al = np.genfromtxt('data/ComptonAl.dat', unpack=True)
θ_0, N_0 = np.genfromtxt('data/ComptonOhne.dat', unpack=True)
assert np.array_equal(θ_Al, θ_0) # sonst müssten die Daten hier zusammengeführt werden
θ = θ_Al

generate_table(f'tab/mess_transmission', list(zip(θ, N_0, N_Al)), col_fmt=[{'d': 1}]*3)
