import matplotlib.pyplot as plt 
import numpy as np 

#TODO Die Werte sind sehr gequetscht. Vllt die Achsenskalierung ändern?

t, T1, T4, T5, T8, T2, T3, T6, T7 = np.genfromtxt('Messwerte_statisch.txt', unpack=True)

plt.plot(t, T1, 'o', label="T1: Messing (breit)")
plt.plot(t, T4, 'o', label="T4: Messing (schmal)")

plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig("Graph_T1T4.pdf")

plt.show()

