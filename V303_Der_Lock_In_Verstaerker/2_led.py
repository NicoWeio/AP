import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

d, U = np.genfromtxt('led.dat', unpack=True)
d *= ureg('cm')
U *= ureg('V')

# Wir haben ohnehin nur DistanzUNTERSCHIEDE gemessen, daher können wir auch einfach bei 0 anfangen.
d -= min(d)

def fit_fn(d, U_0, d_0):
    return U_0 / (d + d_0)

def fit_fn_square(d, U_0, d_0):
    return U_0 / (d + d_0)**2

U_0_fit, d_0_fit = tools.pint_curve_fit(fit_fn, d, U, (ureg('V·cm'), ureg('cm')))
U_0_fit2, d_0_fit2 = tools.pint_curve_fit(fit_fn_square, d, U, (ureg('V·cm²'), ureg('cm')), p0=(tools.nominal_value(U_0_fit)*ureg('cm'), tools.nominal_value(d_0_fit)))
print(f"{U_0_fit, d_0_fit=}")
print(f"{U_0_fit2, d_0_fit2=}")

d_linspace = tools.linspace(min(d), max(d), 100)
plt.plot(d, U, '+', zorder=5, label='Messwerte')
with tools.plot_context(plt, 'cm', 'V', 'd', 'U_A') as plt2:
    plt2.plot(d_linspace, fit_fn(d_linspace, U_0_fit, d_0_fit), show_yerr=False, label='1/d-Fit')
    plt2.plot(d_linspace, fit_fn_square(d_linspace, U_0_fit2, d_0_fit2), show_yerr=False, label='1/d²-Fit')
# plt.yscale('log')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/led.pdf')
# plt.show()
