import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.stats as sp_stats
import pint
ureg = pint.UnitRegistry()

NU = [129, 143, 144, 136, 139, 126, 158]
NU /= ureg('300 s') # Messintervall

# NU_mean = NU.mean()
# NU_mean = unp.uarray(NU.mean(), sp_stats.sem(NU.m))
NU_mean = ufloat(NU.mean().to('1/s').m, sp_stats.sem(NU.to('1/s').m)) * ureg('1/s')

def untergrundrate(ureg2):
    return NU_mean.m * ureg2('1/s')

if __name__ == '__main__':
    print(f"{NU_mean=}")
    print(f"{NU_mean*300=}")
