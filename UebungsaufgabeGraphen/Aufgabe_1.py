import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

m = np.array([2,3,4,5,6])
x = np.array([1.6,2.7,3.2,3.5,4.0])

slope, intercept, r_value, p_value, std_err = stats.linregress(m,x)
print(f"k≈{slope:.3f}")

plt.title("Hooksches Gesetz")
plt.plot(m,x, 'o', label="x²")
plt.plot(m, intercept + slope*m, 'r', label="Ausgleichsgerade")
plt.legend()
plt.xlabel("m [g]")
plt.ylabel("x [cm]")

plt.tight_layout()
plt.show()
# plt.savefig('Aufgabe_1.pdf')
