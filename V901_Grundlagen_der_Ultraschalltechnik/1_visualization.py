import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import scipy.stats as sp_stats

import tools

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

nr, a, b, c = np.genfromtxt('messwerte_schieblehre.dat', unpack=True)

nr, t_a, t_b, A_a, A_b = np.genfromtxt('messwerte_ultraschall.dat', unpack=True)

d_a = 2730*t_a/2000
d_b = 2730*t_b/2000

width = 150
height = 80

fig = plt.figure()
ax = fig.gca()
ax.set_aspect('equal') # die Kreise sollen schließlich wie Kreise aussehen

for a, b, c, d_a, d_b in zip(a, b, c, d_a, d_b):
    radius = abs((b - height + a) / 2)
    h_center = b + radius
    w_center = c + radius
    plt.plot(w_center, b, '_', color='green', label='Schieblehre')
    plt.plot(w_center, height-a, '_', color='green', label='Schieblehre')
    plt.plot(c, h_center, '|', color='green', label='Schieblehre')
    circle = matplotlib.patches.Circle((w_center, h_center), radius=radius, color='black')
    ax.add_patch(circle)

    plt.plot(w_center, d_b, '_', markeredgewidth=1.25, markersize=15, color='red')
    plt.plot(w_center, height - d_a, '_', markeredgewidth=1.25, markersize=15, color='red')

schieblehre_patch = matplotlib.patches.Patch(color='green', label='Schieblehre')
ultraschall_patch = matplotlib.patches.Patch(color='red', label='Ultraschall')
plt.legend(handles=[schieblehre_patch, ultraschall_patch])

plt.xlim([0, width])
plt.ylim([0, height])
plt.xlabel(r'$\si{\milli\meter}$')
plt.ylabel(r'$\si{\milli\meter}$')
plt.tight_layout()
plt.savefig('build/plt/visualization.pdf')
# plt.show()
