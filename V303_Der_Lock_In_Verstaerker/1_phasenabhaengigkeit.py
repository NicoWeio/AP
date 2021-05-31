import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import scipy.stats as sp_stats
import uncertainties.unumpy as unp

import tools

def fit_fn(φ_x, U_0):
    return abs(2 / np.pi * U_0 * np.cos(φ_x))

def analyze(φ, U, name):
    print(f'→ {name}')
    # expected_sign = np.sign(np.cos(φ))
    # U *= expected_sign

    U_0_fit, = tools.pint_curve_fit(fit_fn, φ, U, [ureg('V')])
    print(f"{U_0_fit=}")

    φ_linspace = np.linspace(0, 360, 2*360) * ureg('°')

    plt.figure()
    plt.plot(φ, abs(U), '+', ms=10, mew=1.5, label='Messwerte')
    plt.plot(φ_linspace, fit_fn(φ_linspace, tools.nominal_value(U_0_fit)), label='Fit')
    # plt.yscale('log')
    plt.xlabel(r'$\phi \;/\; °$')
    plt.ylabel(r'$|U_A| \;/\; V$')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'build/plt/{name}.pdf')
    # plt.show()

for name, unit in [('phasen', 'V'),('phasen_noise', 'mV')]:
    φ, U = np.genfromtxt(f'{name}.dat', unpack=True)
    φ *= ureg('°')
    U *= ureg(unit)
    U.ito('V') # sonst nervt der Fit, und ich habe keine Lust mehr…
    analyze(φ, U, name)
