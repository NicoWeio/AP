import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

nr, a, b, c = np.genfromtxt('messwerte_schieblehre.dat', unpack=True)
a *= ureg('mm')
b *= ureg('mm')
c *= ureg('mm')

nr, t_a, t_b, A_a, A_b = np.genfromtxt('messwerte_ultraschall.dat', unpack=True)
t_a *= ureg('µs')
t_b *= ureg('µs')
A_a *= ureg('V')
A_b *= ureg('V')

d = tools.pint_concat(a, b) * 2 # hin und zurück
t = tools.pint_concat(t_a, t_b)
d, t = tools.remove_nans(d, t)

speed, achse = tools.linregress(t, d)
print(f"{speed=}")
print(f"{achse=}")

print(tools.fmt_compare_to_ref(speed, ureg('2730 m/s'), 'Schallgeschwindigkeit in Acryl', unit=ureg('m/s')))

t_bounds = tools.bounds(t)
plt.plot(t, d, '+', label='Messwerte')
plt.plot(t_bounds, (achse.nominal_value * ureg('mm') + speed.nominal_value * ureg('mm/µs') * t_bounds).to('mm'), label='Fit')
#TODO Theoriewert dazu plotten

plt.xlabel(r'$t \mathbin{/} \si{\micro\second}$')
plt.ylabel(r'$d \mathbin{/} \si{\milli\meter}$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/schallgeschwindigkeit.pdf')
# plt.show()
