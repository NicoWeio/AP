import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat, unumpy as unp
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

f, a, b = np.genfromtxt('mess_3.dat', unpack=True)
f *= ureg('Hz')
a *= ureg('ms')
b *= ureg('ms')

b_aus_f = (1 / f).to('ms')

φ = (a / b_aus_f) * 2 * np.pi * ureg('rad')

def fn(f, RC): # mit Einheiten für den internen Gebrauch…
    assert f.units == ureg.hertz
    assert RC.units == ureg('ms')
    return np.arctan((f * RC).to('dimensionless')).to('rad')

def fit_fn(f, RC): # einheitenlos für den Fit
    f *= ureg('Hz')
    RC *= ureg('ms')
    return fn(f.to('Hz'), RC.to('ms')).to('rad').m


RC_fit, = tools.curve_fit(fit_fn, f.m, φ.m)
RC_fit *= ureg('ms')
assert RC_fit.units == ureg('ms')

print(f'RC = {RC_fit}')
RC_fit_nominal = RC_fit.n * ureg('ms')
f_linspace = np.linspace(f[0].m, f[-1].m, 10000) * ureg('Hz')
plt.plot(f, φ, 'x', label='Messwerte')
plt.plot(f_linspace, fn(f_linspace, RC_fit_nominal), label='Fit-Funktion')
plt.fill_between(f_linspace, fn(f_linspace, ureg('2.03 ms')), fn(f_linspace, ureg('2.103 ms')), color='tab:green', label='Erwartung')
# plt.xscale('log')
plt.xlabel(r'$\omega \;/\; Hz$')
plt.ylabel(r'$\varphi \;/\; rad$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/3_rc_via_phi.pdf')
# plt.show()

# –––––

RC = RC_fit_nominal

def A_rel(ω):
    # das U_0 im Nenner fliegt raus…
    return (1 / (1 + (ω*RC)**2))**.5

A_rel_calc = A_rel(f_linspace)
φ_calc = np.arcsin(f_linspace * RC * A_rel_calc)

plt.figure()
plt.polar(φ, A_rel(f), '.', label='gemessene Relativamplitude')
plt.plot(φ_calc, A_rel_calc, label='berechnete Relativamplitude')

plt.xlabel('')
plt.ylabel('')
ax = plt.gca()
ax.set_thetamin(0)
ax.set_thetamax(100)
plt.tight_layout()
plt.legend()
plt.savefig('build/plt/3_polar.pdf')
# plt.show()
