import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
ureg.define('rydberg_energy = h * c * R_inf = R_y')
import scipy as sp
import uncertainties.unumpy as unp

from generate_table import generate_table
import tools

data = {
'Zink': {
    'E_lit': ureg('9.65 keV'),
    'Z': 30,
},
'Gallium': {
    'E_lit': ureg('10.37 keV'),
    'Z': 31,
},
'Brom': {
    'E_lit': ureg('13.47 keV'),
    'Z': 35,
},
'Rubidium': {
    'E_lit': ureg('15.20 keV'),
    'Z': 37,
},
'Strontium': {
    'E_lit': ureg('16.10 keV'),
    'Z': 38,
},
'Zirkonium': {
    'E_lit': ureg('17.99 keV'),
    'Z': 40,
},
}

def calc_σ_K(E, Z):
    return (Z - (E/ureg.R_y - (ureg.α**2 * Z**4 / 4))**.5).to('dimensionless')

d = ureg('201.4 pm') # Gitterebenenabstand

for name, s_data in data.items():
    print(f"→ {name}")

    ## Daten einlesen
    E_lit = s_data['E_lit']
    Z = s_data['Z']
    θ, N = np.genfromtxt(f'data/{name}.dat', unpack=True)
    θ *= ureg.deg
    # N ist in Imp/s gegeben

    ## Berechne Literaturwerte
    s_data['σ_K_lit'] = calc_σ_K(E_lit, Z).m
    s_data['θ_lit'] = np.arcsin(ureg.h * ureg.c / (2 * d * E_lit)).to('°')

    ## Berechnungen auf Basis der Messdaten
    def argmax(vals):
        return np.argwhere(vals == np.max(vals)).flatten().tolist()

    I_K_argmax = argmax(N)
    I_K_argmin = argmax(-N)

    I_K_max = np.max(N)
    I_K_min = np.min(N)
    I_K = (I_K_min + I_K_max) / 2 # „Mitte der Kante“
    print(f"I_K = {I_K}")

    lower = np.mean(θ[I_K_argmin])
    upper = np.mean(θ[I_K_argmax])
    θ_bounds = (lower, upper)


    # Bestimme θ_middle aus linearer Interpolation zwischen den an den Schnittpunkt angrenzenden Messwerten
    i_exact = np.argwhere(N == I_K).flatten().tolist()
    if i_exact: # z.B. Brom hat einen Messwert direkt auf I_K
        assert len(i_exact) == 1
        θ_middle = θ[i_exact[0]]
    else:
        for i in range(len(N)):
            if N[i] < I_K and N[i+1] > I_K:
                Δθ = θ[i+1] - θ[i]
                ΔN = N[i+1] - N[i]
                N_gerade = N[i] + ΔN * (θ - θ[i]) / Δθ
                θ_middle = (I_K - N[i]) * Δθ / ΔN + θ[i]
                break
    print(f"θ_middle = {θ_middle}")

    E = (ureg.h * ureg.c / (2 * d * np.sin(θ_middle.to('rad')))).to('keV')
    σ_K = calc_σ_K(E, Z)

    print(f"E = {E}")
    print(tools.fmt_compare_to_ref(σ_K, s_data['σ_K_lit'], name="σ_K"))

    ## Plots
    plt.figure()
    plt.plot(θ, N, 'x')
    plt.plot(θ[I_K_argmin], N[I_K_argmin], 'xr', label=('rel. Minima' if len(I_K_argmin) > 1 else 'rel. Minimum'))
    plt.plot(θ[I_K_argmax], N[I_K_argmax], 'xr', label=('rel. Maxima' if len(I_K_argmax) > 1 else 'rel. Maximum'))
    # plt.axvspan(*θ_bounds, alpha=0.25, label='Absorptionskante')
    if not i_exact:
        plt.plot(θ[i:i+2], N[i:i+2], color='gray')
    plt.axvline(θ_middle, linestyle='-', color='blue', label=r'gesuchtes $\theta$')
    plt.axhline(I_K, linestyle='-', color='green', label=r'$I_K$')
    plt.xlabel(r'$θ \mathbin{/} \si{\degree}$')
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
    s_data['θ_bounds'] = θ_bounds
    s_data['I_K'] = I_K
    s_data['I_K_bounds'] = (I_K_min, I_K_max)
    s_data['θ_bounds_flag_avg'] = (len(I_K_argmin) > 1, len(I_K_argmax) > 1)

    print('–'*10)

def fmt_single(name, d):
    return '\n'.join((
        r'\clearpage',
        r'\subsubsection{' + name + '}',
        r'\begin{figure}[H]',
        r'\centering',
        r'\includegraphics[width=\textwidth]{build/plot_' + name.lower() + '.pdf}',
        r'\caption{Absorptionsspektrum von ' + name + '.}',
        r'\label{fig:' + name.lower() + '}',
        r'\end{figure}',
        r'Die Intensität wird ' + ('im Mittel ' if d['θ_bounds_flag_avg'][0] else '') + r'für $\SI{' + f"{d['θ_bounds'][0].m:.1f}" + r'}{\degree}$ minimal ($N = \num{' + f"{d['I_K_bounds'][0]:.0f}" + '} $)',
        r'und ' + ('im Mittel ' if d['θ_bounds_flag_avg'][1] else '') + r'für $\SI{' + f"{d['θ_bounds'][1].m:.1f}" + r'}{\degree}$ maximal ($N = \num{' + f"{d['I_K_bounds'][1]:.0f}" + '} $).',
        r'Also ist $I_K = \num{' + f"{d['I_K']:.1f}" + '}$',
        r'und die Mitte der abgelesenen Absorptionskante liegt bei $\SI{' + f"{d['θ_middle'].m:.2f}" + r'}{\degree}$.',
        r'Die Absorptionsenergie beträgt demnach $E_\text{' + name + r'} = \SI{' + f"{d['E'].m:.2f}" + r'}{\kilo\electronvolt}$',
        r'und die Abschirmkonstante ist $\sigma_{K, \text{' + name + r'}} = \num{' + f"{d['σ_K'].m:.2f}" + '}$.',
        ))

with open('build/auswertung_absorptionsspektren.tex', 'w') as f:
    f.write('\n\n'.join([fmt_single(name, d) for name, d in data.items()]))

## Bestimmung der Rydbergenergie ↓

E_list = tools.pintify([s['E'] for s in data.values()])
σ_K_list = tools.pintify([s['σ_K'] for s in data.values()])
σ_K_lit_list = np.array([s['σ_K_lit'] for s in data.values()])
z = np.array([s['Z'] for s in data.values()]) * ureg('dimensionless')

sqrt_E_list = (E_list**.5).to('eV**0.5')
a, b = tools.linregress(z, sqrt_E_list)

plt.figure()
plt.plot(z, sqrt_E_list, 'x', label='Daten')
plt.plot(z, tools.nominal_values(a*z + b), label='Regressionsgerade')
plt.grid()
plt.xlabel(r'$Z$')
plt.ylabel(r'$\sqrt{E_K} \mathbin{/} \si{\sqrt{\electronvolt}}$')

print(f'Regressionsparameter a = {a}')
print(f'Regressionsparameter b = {b}')

R_energie = a**2
R = R_energie / ureg.h

print(tools.fmt_compare_to_ref(R_energie, 1 * ureg.R_y, unit='eV', name="Rydbergenergie"))
print(tools.fmt_compare_to_ref(R, 1 * ureg.c * ureg.R_inf, unit='PHz', name="Rydbergfrequenz"))
plt.legend()
plt.tight_layout()
plt.savefig('build/plot_moseley.pdf')
# plt.show()

generate_table('table_absorptionsspektren', [[name, d['θ_middle'], d['E'], d['σ_K'], d['σ_K_lit'], d['σ_K_rel_err']] for name, d in data.items()], col_fmt=[None,{'d': 2},{'d': 2},{'d': 2},{'d': 2},None])

# tabellarische Darstellung der Ergebnisse im Terminal
import pandas as pd
df = pd.DataFrame.from_dict(data, orient='index')
print(df.head(len(data)))
