import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import uncertainties.unumpy as unp

from generate_table import generate_table
import tools

data = {
'Zink': {
    'θ_bounds': (ureg('18.5 °'), ureg('18.9 °')),
    'σ_K_lit': 3.566,
    'Z': 30,
},
'Gallium': {
    'θ_bounds': (ureg('17.1 °'), ureg('17.6 °')),
    'σ_K_lit': 3.677,
    'Z': 31,
},
'Brom': {
    'θ_bounds': (ureg('13.0 °'), ureg('13.5 °')),
    'σ_K_lit': 3.848,
    'Z': 35,
},
'Rubidium': {
    'θ_bounds': (ureg('11.4 °'), ureg('12.1 °')),
    'σ_K_lit': 3.944,
    'Z': 37,
},
'Strontium': {
    'θ_bounds': (ureg('10.8 °'), ureg('11.4 °')),
    'σ_K_lit': 3.999,
    'Z': 38,
},
'Zirkonium': {
    'θ_bounds': (ureg('9.7 °'), ureg('10.2 °')),
    'σ_K_lit': 4.101,
    'Z': 40,
},
}

d = ureg('201.4 pm') # Gitterebenenabstand

for name, s_data in data.items():
    print(f"→ {name}")
    ## Daten einlesen
    θ_bounds = s_data['θ_bounds']
    Z = s_data['Z']
    θ, N = np.genfromtxt(f'data/{name}.dat', unpack=True)
    θ *= ureg.deg
    # N ist in Imp/s gegeben

    ## Berechnungen
    θ_middle = (θ_bounds[0] + θ_bounds[1])/2

    E = (ureg.h * ureg.c / (2 * d * np.sin(θ_middle.to('rad')))).to('keV')
    R_y = 1 * ureg.h * ureg.c * ureg.R_inf # Rydberg-Energie
    σ_K = (Z - (E/R_y - (((1*ureg.α)**2 * Z**4) / 4))**.5).to('dimensionless')

    print(f"θ_middle = {θ_middle:.2f}")
    print(f"E = {E}")
    print(tools.fmt_compare_to_ref(σ_K, s_data['σ_K_lit'], name="σ_K"))

    ## Plots
    plt.figure()
    plt.axvline(θ_middle, linestyle='-', color='blue', label='Mitte der Absorptionskante')
    plt.plot(θ, N, 'x')
    plt.axvspan(*θ_bounds, alpha=0.25, label='Absorptionskante')
    plt.xlabel(r'$θ \;/\; °$')
    plt.ylabel(r'$N$')
    plt.grid()
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(f'build/plot_{name.lower()}.pdf')
    # plt.show()

    s_data['E'] = E
    s_data['σ_K'] = σ_K
    s_data['σ_K_rel_err'] = tools.fmt_rel_err_percent(σ_K, s_data['σ_K_lit'])
    s_data['θ_middle'] = θ_middle

    print('–'*10)


E_list = tools.pintify([s['E'] for s in data.values()])
σ_K_list = tools.pintify([s['σ_K'] for s in data.values()])
σ_K_lit_list = np.array([s['σ_K_lit'] for s in data.values()])
z = np.array([s['Z'] for s in data.values()]) * ureg('dimensionless')

sqrt_E_list = (E_list**.5).to('eV**0.5')
params = tools.linregress(z, sqrt_E_list)

plt.figure()
plt.plot(z, sqrt_E_list, 'x', label='Daten')
plt.plot(z, unp.nominal_values(params[0] * z + params[1]), label='Regressionsgerade')
plt.grid()
plt.xlabel(r'$Z$')
plt.ylabel(r'$\sqrt{E_K} \;/\; \sqrt{eV}$')

print(f'Regressionsparameter m = {params[0]}')
print(f'Regressionsparameter b = {params[1]}')

R_energie = params[0]**2
R = R_energie / ureg.h

print(tools.fmt_compare_to_ref(R_energie, 1 * ureg.h * ureg.c * ureg.R_inf, unit='eV', name="Rydbergenergie"))
print(tools.fmt_compare_to_ref(R, 1 * ureg.c * ureg.R_inf, unit='PHz', name="Rydbergfrequenz"))
plt.legend()
plt.tight_layout()
plt.savefig('build/plot_moseley.pdf')
# plt.show()

# generate_table('table_absorptionsspektren', [[name, d['σ_K'], d['σ_K_lit'], d['σ_K_rel_err']] for name, d in data.items()], col_fmt=[None,{'d': 2},{'d': 2},None])
