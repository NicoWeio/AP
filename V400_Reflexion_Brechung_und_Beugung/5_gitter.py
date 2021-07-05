import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

d_list = [100, 300, 600] * ureg('mm') # Gitterkonstante
λ_all = {'red': [], 'green': []}
color_names = {'green': 'gruen', 'red': 'rot'}

fig, axs = plt.subplots(len(d_list), sharex=True)

for d, ax in zip(d_list, axs):
    ax.title.set_text('$d = \SI{' f'{d.to("mm").m:.0f}' '}{\milli\meter}$')
    for color in ['red', 'green']:
        k, φ = np.genfromtxt(f'data/Beugung_{int(d.m)}_{color_names[color]}.csv', comments='#', unpack=True)
        φ *= ureg.deg # Ablenkwinkel

        # Rote und grüne Striche können sich verdecken; daher wird nicht mit vollem alpha gearbeitet.
        ax.eventplot(φ, color=color, lineoffsets=0, linewidths=2, alpha=0.75)
        ax.set_ylim([-0.5,0.5])

        # Für k=0 lässt sich keine Wellenlänge berechnen, daher `[k!=0]`.
        λ = d * np.sin(φ[k!=0]) / k[k!=0]
        λ_all[color] += list(λ)

        λ_mean = tools.ufloat_from_list(λ)

    ax.axvline(0, color='grey', zorder=0)
    ax.set_xlabel(r'$\varphi \mathbin{/} \si{\degree}$')
    ax.set_yticks([])
    # krasser One-Liner, um 0° im Plot zu zentrieren :P
    ax.set_xlim(*(np.array([-1,1]) * abs(max(ax.get_xlim(), key=abs))))

plt.tight_layout()
plt.savefig(f'build/plt/beugung.pdf')
# plt.show()


λ_lit = {'red': ureg('635 nm'), 'green': ureg('532 nm')} # siehe Versuchsanleitung und Versuchsaufbau

for color, λ in λ_all.items():
    λ = tools.pintify(λ)
    λ_all_mean = tools.ufloat_from_list(λ).to('nm')
    print(f"{color}:", tools.fmt_compare_to_ref(λ_all_mean, λ_lit[color]), '', sep='\n')
