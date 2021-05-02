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


def ufloat_from_list(vals):
    return ufloat(np.mean(vals), np.std(vals))


def fmt_abs_err(own, reference, precise=False):
    own_abs_err = own - reference
    return f'{(own_abs_err).n:.2f}'


def fmt_rel_err_percent(o, r, precise=False):
    o_rel_err = ((o - r)/r).to('dimensionless').m
    return f'{(o_rel_err * 100).n:.2f} %'


def fmt_err(o, r, precise=False):
    return f'{fmt_rel_err_percent(o, r, precise)} | {fmt_abs_err(o, r, precise)}'
