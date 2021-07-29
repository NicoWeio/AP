import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp
import tools


nr, a, b, c = np.genfromtxt('messwerte_schieblehre.dat', unpack=True)

nr, t_a, t_b, A_a, A_b = np.genfromtxt('messwerte_ultraschall.dat', unpack=True)

d_a = 2730*t_a/2000
d_b = 2730*t_b/2000

width = 150
height = 80

# Hier konnte ich nicht einfach einen Bar-Plot machen. Denn:
# Falls eine Ultraschall-Messung „über den Mittelpunkt hinaus falsch“ ist,
# stimmt der Plot sonst nicht!

fig = plt.figure()
ax = fig.gca()
plt.axhline(0, color='black')

for nr, a, b, d_a, d_b in zip(nr, a, b, d_a, d_b):
    radius = abs((b - height + a) / 2)
    h_center = b + radius

    ax.add_patch(matplotlib.patches.Rectangle((nr-0.9, -radius), 0.8, radius*2, color='tab:gray'))
    ax.add_patch(matplotlib.patches.Rectangle((nr-0.8, (d_b - h_center)), 0.6, height - d_a - d_b, color='tab:red'))

schieblehre_patch = matplotlib.patches.Patch(color='tab:gray', label='Schieblehre')
ultraschall_patch = matplotlib.patches.Patch(color='tab:red', label='Ultraschall')
plt.legend(handles=[schieblehre_patch, ultraschall_patch])

plt.xticks([])
# plt.xticks(list(range(len(nr)+1)))
plt.xlim(0, 11)
plt.ylim(-5, 5)
plt.ylabel(r'$\si{\milli\meter}$')
plt.grid()
plt.tight_layout()
plt.savefig('build/plt/visualization_bars.pdf')
# plt.show()
