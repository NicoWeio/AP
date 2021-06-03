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


def curve_fit(fit_fn, x, y, p0=None):
    params, pcov = sp.optimize.curve_fit(fit_fn, x, y, p0)
    param_errors = np.sqrt(np.diag(pcov))
    return tuple(ufloat(p, e) for p, e in zip(params, param_errors))


def pint_curve_fit(fit_fn, x, y, param_units, p0=None):
    #TODO: Abweichung mittels sigma-Parameter berücksichtigen
    if p0:
        assert len(param_units) == len(p0)
        for p0_single, pu in zip(p0, param_units):
            if p0_single.units != pu.units:
                raise Exception(f"Wrong unit in p0 – got '{p0_single.units}' instead of '{pu.units}'")
        p0 = tuple(p0_s.m for p0_s in p0)

    u_params = curve_fit(fit_fn, x.m, y.m, p0)
    pint_params = tuple(p * u for p, u in zip(u_params, param_units))

    try:
        pint_params_nominal = tuple(p.n * u for p, u in zip(u_params, param_units))
        test_val = fit_fn(x, *pint_params_nominal)
    except:
        raise Exception("Could not test fit_fn")
    if test_val.units != y.units:
        raise Exception(f"Wrong param_units – fit_fn(x[0], *fit_params_nominal) returns '{test_val.units}' instead of '{y.units}'")
    return pint_params


def pintify(list):
    assert len(list) > 0
    units = list[0].units
    assert all(e.units == units for e in list)
    return [e.m for e in list] * units

def nominal_values(list):
    assert isinstance(list, pint.Quantity)
    units = list.units
    return [e.m.n for e in list] * units

def nominal_value(v):
    units = v.units
    return v.m.n * units


def linspace(start, end, num=50):
    return np.linspace(start.m, end.to(start.units).m, num=num) * start.units


def ufloat_from_list(vals):
    return ufloat(np.mean(vals), np.std(vals))


def fmt_abs_err(o, r, precise=False, show_uncertainty=True):
    o_abs_err = o - r
    if isinstance(o_abs_err, UFloat) and not show_uncertainty:
        o_abs_err = o_abs_err.n
    return f'{o_abs_err:.2f}'


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
        f'- abs. Abweichung: {fmt_abs_err(my_o, my_r)}\n'
        f'- rel. Abweichung: {fmt_rel_err_percent(o, r)}'
    )


def pint_concat(*lists):
    units = lists[0].units
    out = []
    for l in lists:
        vals = l.to(units).m
        out.extend(vals)
    out *= units
    return out
    # return [*[l.to(units).m for l in lists]] * units


# Entfernt Wertepaare(/-tupel…), die NaNs enthalten
def remove_nans(*inputs):
    # return tuple(zip(*[input_tuple for input_tuple in zip(*inputs) if not any(np.isnan(v) for v in input_tuple)]))
    return (pintify(x) for x in zip(*[input_tuple for input_tuple in zip(*inputs) if not any(np.isnan(v) for v in input_tuple)]))


# Hilfreich, um z.B. eine Gerade zu plotten…
def bounds(vals):
    return pintify([min(vals), max(vals)])
