import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

g = np.array([60,80,100,110,120,125])
b = np.array([285,142,117,85,86,82])

brennweite = 1/(1/g+1/b)
print("Brennweiten", brennweite)
print("Mittelwert", np.mean(brennweite))
print("Standardabweichung", np.std(brennweite))
print("Fehler des Mittelwertes", stats.sem(brennweite))

G = 1/g
B = 1/b

slope, intercept, r_value, p_value, std_err = stats.linregress(G,B)
print(f"slope ≈ {slope:.3f}")

y_vals = intercept + slope*G
print("ooo",y_vals/G)
print("fooo", 1/slope)

plt.title("Linsengleichung")
plt.plot(G,B, 'o', label="x²")
plt.plot(G, intercept + slope*G, 'r', label="Ausgleichsgerade (linregress)")
plt.legend()
plt.xlabel("1 / Gegenstandsweite g [mm]")
plt.ylabel("1 / Bildweite b [mm]")

plt.tight_layout()
plt.show()
# plt.savefig('Aufgabe_2.pdf')
