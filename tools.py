import numpy as np
import pint
import scipy as sp
import scipy.stats
from uncertainties import ufloat

def linregress(x, y):
    r = sp.stats.linregress(x.m, y.m)
    return (
        ufloat(r.slope, r.stderr) * (y.units / x.units),
        ufloat(r.intercept, r.intercept_stderr) * y.units
    )

def pintify(list):
    assert len(list) > 0
    units = list[0].units
    assert all(e.units == units for e in list)
    return [e.m for e in list] * units
