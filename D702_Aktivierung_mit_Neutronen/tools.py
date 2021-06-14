import numpy as np
import scipy as sp
from uncertainties import ufloat

def curve_fit(fit_fn, x, y, **kwargs):
    params, pcov = sp.optimize.curve_fit(fit_fn, x, y, p0=kwargs.get('p0', None))
    param_errors = np.sqrt(np.diag(pcov))
    print(f"{params=}")
    print(f"{param_errors=}")
    u_params = tuple(ufloat(param, error) for param, error in zip(params, param_errors))
    print(f"{u_params=}")
    return u_params

# def pint_curve_fit(fit_fn, x, y, **kwargs):
    # Wie soll ich das machen :/ ?

def linregress(x, y):
    slope, intercept, r_value, p_value, std_err = sp.stats.linregress(x, y)
    return (ufloat(slope, std_err), intercept)