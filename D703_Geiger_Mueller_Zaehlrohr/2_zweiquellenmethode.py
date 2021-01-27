import numpy as np
from uncertainties import ufloat
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

N1 = ufloat(96041, np.sqrt(96041)) * ureg('1/(120s)')
N12 = ufloat(158479, np.sqrt(158479)) * ureg('1/(120s)')
N2 = ufloat(76518, np.sqrt(76518)) * ureg('1/(120s)')

T = (N1 + N2 - N12)/(2*N1*N2)

print(f"T={T.to('µs')}")
