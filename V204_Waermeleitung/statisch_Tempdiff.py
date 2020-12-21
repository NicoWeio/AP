import matplotlib.pyplot as plt 
import numpy as np 

t, T1, T4, T5, T8, T2, T3, T6, T7 = np.genfromtxt('Messwerte_statisch.txt', unpack=True)

DeltaT_St = T7 - T8
print(DeltaT_St)

T_St = T2- T1

plt.plot(t, DeltaT_St, 'o', label="T7 - T8")
plt.plot(t, T_St, 'o', label="T2 - T1")

plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig("Graph_Tempdiff.pdf")

plt.show()