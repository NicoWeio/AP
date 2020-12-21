import matplotlib.pyplot as plt 
import numpy as np 

#TODO Die Werte sind sehr gequetscht. Vllt die Achsenskalierung ändern?

t, T1, T4, T5, T8, T2, T3, T6, T7 = np.genfromtxt('Messwerte_statisch.txt', unpack=True)

plt.plot(t, T5, 'o', label="T5: Aluminium")
plt.plot(t, T8, 'o', label="T8: Edelstahl")


plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig("Graph_T5T8.pdf")

plt.show()