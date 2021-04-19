# sehr WIP – ich sollte wahrscheinlich einfach anfangen, zu schreiben, statt dieses Programm zu Pint umzubauen…

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import sem
import scipy.constants as const
from scipy import optimize
from scipy.optimize import curve_fit

from uncertainties import ufloat
import uncertainties.unumpy as unp

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

# Konstanten:
avo = ureg.avogadro_constant
μ_B = 9.274 * 1e-24 * ureg('J/T') # Bohrsches Magneton, nicht in Pint
μ_0 = ureg.mu_0
k_b  = ureg.boltzmann_constant
T = ureg('293.15 K') # Raumtemperatur ≙ 20 °C

data = [
{
    'name': "Dy2O3",
    'S': 2.5,
    'L': 5,
    'J': 7.5,
    'ρ': ureg('7800 kg/m³'),
    'M': ureg('373 g/mol'),
},
{
    'name': "Nd2O3",
    'S': 1.5,
    'L': 6,
    'J': 4.5,
    'ρ': ureg('7240 kg/m³'),
    'M': ureg('336 g/mol'),
},
]

def analyse(data):
    print(f"{data['name']} ↓")
    L = data['L']
    S = data['S']
    J = data['J']
    M = data['M']
    ρ = data['ρ']

    g_J = (3*J*(J+1) + S*(S+1) - L*(L+1)) / (2*J*(J+1))
    print(f"g_J: {g_J:.4f}") #✓

    N = (2*avo*ρ)/M # Faktor 2 siehe Mampfzwerg, aknierim – nur so stimmen die Werte
    N.ito('1/m³')
    print(f"{N=}")

    χT = (μ_0 * μ_B**2 * g_J**2 * N * J * (J+1)) / (3 * k_b * T)
    χT.ito('dimensionless')
    print(f"χT: {χT.magnitude:.4f}")

for d in data:
    analyse(d)
    print('–––')
