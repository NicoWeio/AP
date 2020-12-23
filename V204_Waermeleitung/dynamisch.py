import matplotlib.pyplot as plt
import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp
import scipy.optimize as sp_optimize
import scipy.stats as sp_stats
import pint
ureg = pint.UnitRegistry()
ureg.autoconvert_offset_to_baseunit = True
ureg.setup_matplotlib()
from generate_table import generate_table

# TODO: tight_layout überall!!!

from pint_tools import pint_range, pint_max, pint_min, pintify

def index_to_seconds(i, vals_per_second):
    return (i / vals_per_second).to('seconds')
def seconds_to_index(s, vals_per_second):
    return int((s * vals_per_second).to('dimensionless'))

def extrema(the_T, indices, periodendauer, vals_per_second):
    maxima = list()
    minima = list()
    for offset in pint_range(ureg('0 seconds'), indices[-1], periodendauer):
        start = seconds_to_index(offset, vals_per_second)
        end = seconds_to_index(offset + periodendauer, vals_per_second)
        t_vals = indices[start : end]
        T_vals = the_T[start : end]
        maxima.append(pint_max(t_vals, T_vals))
        minima.append(pint_min(t_vals, T_vals))
    return maxima, minima

def amplituden(maxima, minima):
    amplituden = list()
    for maximum, minimum in zip(maxima, minima):
        t_max, T_max = maximum
        t_min, T_min = minimum
        amplituden.append((T_max - T_min) / 2)
    return pintify(amplituden)

def phasendifferenzen(extrema1, extrema2):
    phasendifferenzen = list()
    for e1, e2 in zip(extrema1, extrema2):
        t_1, T_1 = e1
        t_2, T_2 = e2
        phasendifferenzen.append(t_2 - t_1)
    return pintify(phasendifferenzen)

def main(data):
    print(f"{data['displayName']}:")

    T_nah = data['T_nah']
    T_fern = data['T_fern']

    indices = index_to_seconds(data['raw_indices'], data['vals_per_second'])

    extrema_nah = extrema(T_nah, indices, data['periodendauer'], data['vals_per_second'])
    extrema_fern = extrema(T_fern, indices, data['periodendauer'], data['vals_per_second'])
    amplituden_nah = amplituden(*extrema_nah)
    amplituden_fern = amplituden(*extrema_fern)
    Δt = phasendifferenzen(extrema_nah[0], extrema_fern[0])

    t_bounds = (0 * ureg.seconds, (10+1) * data['periodendauer'])
    xticks = list(pint_range(*t_bounds, data['periodendauer']))

    def plt_extrema(extrema_i): # nimmt maxima ODER minima
        the_t, the_T = zip(*extrema_i)
        return pintify(the_t), pintify(the_T)

    plt.figure(data['name'])
    # Wir plotten nach Sekunden, nicht Indizes!
    plt.plot(indices.to('seconds'), T_nah, label=r'$T_\mathrm{nah}$')
    plt.plot(indices.to('seconds'), T_fern, label=r'$T_\mathrm{fern}$')
    # plt.plot(*plt_extrema(extrema_nah[0]), '.r') # Maxima
    # plt.plot(*plt_extrema(extrema_nah[1]), '.r') # Minima
    # plt.plot(*plt_extrema(extrema_fern[0]), '.r') # Maxima
    # plt.plot(*plt_extrema(extrema_fern[1]), '.r') # Minima
    plt.xticks(xticks)
    plt.xlabel('$t \;/\; s$')
    plt.ylabel('$T \;/\; °C$')
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"build/plot_dynamisch_{data['name']}.pdf")
    # plt.show()

    Δx = ureg('3 cm')
    A_verhältnis = amplituden_nah / amplituden_fern

    kappa = (data['ρ'] * data['c'] * Δx**2) / (2 * Δt * np.log(A_verhältnis))
    # TODO: Der letzte Wert ist Mist!
    # daher:
    kappaMean = kappa[:-1].mean()

    uKappaMean = ufloat(kappaMean.to('W/(m·K)').m, sp_stats.sem(kappa[:-1].to('W/(m·K)').m)) * ureg('W/(m·K)')
    print(f"κ={uKappaMean}")

    # Phasengeschwindigkeit
    f = 1 / data['periodendauer']
    ω = 2 * np.pi * f
    # pint, ufloat, und Wurzel vertragen sich nicht so richtig (egal ob np, unp, math…)
    v = unp.sqrt(((2 * uKappaMean * ω) / (data['ρ'] * data['c'])).to('cm²/s²').m) * ureg('cm/s')
    λ = v * data['periodendauer']
    assert λ.check('[length]')

    print(f"{λ=} | {v=}")

    # durch das Entfernen des letzten Elements von kappa entfällt die komplette letzte Zeile ✓
    generate_table(f"table_{data['name']}", [[a,b,c,d] for (a,b,c,d) in zip(amplituden_nah.to('delta_degC'), amplituden_fern.to('delta_degC'), Δt.to('seconds'), kappa[:-1].to('W/(m·K)'))])


indices_dynamisch1, T1, T2, T3, T4, T5, T6, T7, T8 = np.genfromtxt('Daten_dynamisch1.txt', unpack=True)

# aka Brass
messing_breit = {
    'name': 'messing_breit',
    'displayName': 'Messing (breit)',
    'ρ': ureg('8520 kg/m³'),
    'c': ureg('385 J/(kg·K)'),
    'raw_indices': indices_dynamisch1,
    'T_nah': T2 * ureg.degC,
    'T_fern': T1 * ureg.degC,
    'vals_per_second': ureg('5 / second'),
    # 40s HEAT + 40s COOL
    'periodendauer': 80 * ureg.seconds,
}
main(messing_breit)

messing_schmal = {
    'name': 'messing_schmal',
    'displayName': 'Messing (schmal)',
    'ρ': ureg('8520 kg/m³'),
    'c': ureg('385 J/(kg·K)'),
    'raw_indices': indices_dynamisch1,
    'T_nah': T3 * ureg.degC,
    'T_fern': T4 * ureg.degC,
    'vals_per_second': ureg('5 / second'),
    'periodendauer': 80 * ureg.seconds,
}
main(messing_schmal)

aluminium = {
    'name': 'aluminium',
    'displayName': 'Aluminium',
    'ρ': ureg('2800 kg/m³'),
    'c': ureg('830 J/(kg·K)'),
    'raw_indices': indices_dynamisch1,
    'T_nah': T6 * ureg.degC,
    'T_fern': T5 * ureg.degC,
    'vals_per_second': ureg('5 / second'),
    'periodendauer': 80 * ureg.seconds,
}
main(aluminium)

# OVERRIDES!
indices_dynamisch2, T1, T2, T3, T4, T5, T6, T7, T8 = np.genfromtxt('Daten_dynamisch2.txt', unpack=True)

edelstahl = {
    'name': 'edelstahl',
    'displayName': 'Edelstahl',
    'ρ': ureg('8000 kg/m³'),
    'c': ureg('400 J/(kg·K)'),
    'raw_indices': indices_dynamisch2,
    'T_nah': T7 * ureg.degC,
    'T_fern': T8 * ureg.degC,
    'vals_per_second': ureg('0.5 / second'),
    # 100s HEAT + 100s COOL
    'periodendauer': 200 * ureg.seconds,
}
main(edelstahl)
