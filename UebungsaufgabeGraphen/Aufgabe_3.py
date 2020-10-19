import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

d = np.array([0.1,0.2,0.3,0.4,0.5,1.0,1.2,1.5,2.0,3.0,4.0,5.0])
N = np.array([7565,6907,6214,5531,4942,2652,2166,1466,970,333,127,48])

# slope, intercept, r_value, p_value, std_err = stats.linregress(m,x)
# print(f"k≈{slope:.3f}")

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle("Absorptionsgesetz")

# ax1.plot(d,N, 'o')
ax1.errorbar(d,N, yerr=np.sqrt(N))
# plt.plot(m, intercept + slope*m, 'r', label="Ausgleichsgerade")
# ax1.legend()
ax1.set_xlabel("d [cm]")
ax1.set_ylabel("N [1/60s]")

# ax2.plot(d,N, 'o')
ax2.errorbar(d,N, yerr=np.sqrt(N))
# plt.plot(m, intercept + slope*m, 'r', label="Ausgleichsgerade")
# ax2.legend()
ax2.set_xlabel("d [cm]")
ax2.set_ylabel("N [1/60s]")
ax2.set_yscale('log') #!

plt.tight_layout()
plt.show()
# plt.savefig('Aufgabe_3.pdf')
