import numpy as np
import pint
import scipy as sp
import scipy.stats
from uncertainties import ufloat, UFloat

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


def fmt_rel_err_percent(o, r, precise=False, show_uncertainty=True):
    o_rel_err = ((o - r)/r).to('dimensionless').m
    if isinstance(o_rel_err, UFloat) and not show_uncertainty:
        o_rel_err = o_rel_err.n
    return f'{o_rel_err:.2%}'


def fmt_err(o, r, precise=False):
    return f'{fmt_rel_err_percent(o, r, precise)} | {fmt_abs_err(o, r, precise)}'

def fmt_compare_to_ref(o, r, name=None, unit=None):
    my_o = o.to(unit) if unit else o
    my_r = r.to(unit) if unit else r
    my_name = f'{name}:\n' if name else ''
    return my_name + (
        f'- ist: {my_o:.2f}\n'
        f'- soll: {my_r:.2f}\n'
        f'- rel. Abweichung: {fmt_rel_err_percent(o, r)}'
    )
