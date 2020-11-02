import matplotlib.pyplot as plt
import numpy as np

t, T1, p1, T2, p2, N = np.genfromtxt('Daten.dat', unpack=True)

# plt.plot(t, T1, p1, T2, p2, N)

#t = np.linspace(0,3)

#sigma_t = np.std(t)
#sigma_T1 = np.std(T1)
#sigma_p1 = np.std(p1)
#sigma_T2 = np.std(T2)
#sigma_p2 = np.std(p2)
#sigma_N = np.std(N)

T1 += 273.15
T2 += 273.15

plt.errorbar(t, T1,  fmt='x', label='T1')
#plt.errorbar(t, p1, yerr = p1 * 0.68, fmt='o', label='p1')

plt.errorbar(t, T2,  fmt='x', label='T2')
#plt.errorbar(t, p2, yerr = p2 * 0.68, fmt='o', label='p2')

#plt.errorbar(t, N, fmt='x', label='N')

plt.xlabel(r'$t/s$')
plt.xlim(0, 36)


plt.legend()

plt.tight_layout()
plt.savefig('build/wärmepumpe_plot.pdf')

# plt.show()
