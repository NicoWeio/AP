import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

import tools

d = ureg('201.4 pm') # Gitterkonstante

E_K_alpha = ureg('8.1 keV')
E_K_beta = ureg('8.905 keV')

λ_alpha = ureg.h * ureg.c / E_K_alpha
λ_beta = ureg.h * ureg.c / E_K_beta

print(f"{λ_alpha.to('m')=}")
print(f"{λ_beta.to('m')=}")

# nach Bragg; n=1
θ_alpha = np.arcsin(λ_alpha / (2 * d))
θ_beta = np.arcsin(λ_beta / (2 * d))
print(f"{θ_alpha.to('°')=}")
print(f"{θ_beta.to('°')=}")

# deltaλ = λ_2 - λ_1
# deltaλ = ureg.h / (ureg.electron_mass * ureg.c) * (1 - np.cos(θ))

λ_C = 1 * ureg.h / (ureg.electron_mass * ureg.c)
print(f"{λ_C.to('m')=}")
