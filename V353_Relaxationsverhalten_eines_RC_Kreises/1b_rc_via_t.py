# Dies ist vor allem ein Proof-of-concept für mein `tools.pint_curve_fit`;
# die Analyse für das Protokoll soll anders erfolgen…

import matplotlib.pyplot as plt
import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

def fit_fn(t, U_0, RC):
    return U_0 * np.exp(-t / RC)

t, U = np.genfromtxt('mess_1.dat', unpack=True)
t *= ureg('ms')
U *= ureg('V')

U -= U[-1] # das Minimum von U soll 0 sein

U_0_fit, RC_fit = tools.pint_curve_fit(fit_fn, t, U, (ureg('V'), ureg('Ω·F')), p0=(U[0], ureg('1 Ω·F')))
print(f"{U_0_fit=}, {RC_fit=}")

t_linspace = np.linspace(0, 8)

plt.plot(t_linspace, fit_fn(t_linspace, U_0_fit.n, RC_fit.n))
plt.plot(t, U, 'x')
plt.show()
