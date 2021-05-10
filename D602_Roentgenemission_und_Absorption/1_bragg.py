import numpy as np
import matplotlib.pyplot as plt

θ, N = np.genfromtxt('data/Bragg.dat', unpack=True)

θ_theorie = 28
θ_peak = θ[np.argmax(N)]
print(f"Maximum: {θ_peak}° / {np.max(N)}")
print(f"Abweichung: {abs(θ_peak - θ_theorie):.2f}°")

plt.plot(θ, N, '-')
plt.axvline(θ_peak, linestyle='-', color='red', label=r'$\theta_{B, exp}$')
plt.axvline(θ_theorie, linestyle='--', color='gray', label=r'$\theta_{B, theo}$')

plt.xlabel(r'$θ_{GM} \;/\; °$')
plt.ylabel(r'$N$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plot_bragg.pdf')
# plt.show()
