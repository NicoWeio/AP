import numpy as np
import pint

def pint_range(start, stop, step=1):
    assert start.dimensionality == stop.dimensionality
    if isinstance(step, int):
        print('stepShit')
        step *= start.units
    assert step.dimensionality == start.dimensionality

    num = start
    while num < stop:
        yield num
        num += step


def pint_max(x, y):
    current_index = x[0]
    current_max = y[0]
    for c_x, c_y in zip(x,y):
        # print("-", c_x,c_y)
        if c_y > current_max:
            current_index = c_x
            current_max = c_y
    return current_index, current_max

def pint_min(x, y):
    index, max = pint_max(x, -y)
    return index, -max

def pintify(list):
    assert len(list) > 0
    units = list[0].units
    assert all(e.units == units for e in list)
    return [e.m for e in list] * units
