import numpy as np
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
import tools

def get_T(i, name):
    # Schwingungsdauern, jeweils von uns beiden gemessen
    T_a, T_b = np.genfromtxt(f'data/{i}_{name}.dat', unpack=True)
    return np.concatenate([T_a, T_b])

for i, l in [('1', 50), ('2', 100)]:
    l *= ureg.cm
    print(f"→ Pendellänge: {l}")
    print("\n→ Gleichsinnige Schwingung")
    T_plus_links = get_T(i, 'gleichsinnig_links') / 5 # 5 Perioden gemessen… Unschön…
    T_plus_rechts = get_T(i, 'gleichsinnig_rechts') / 5 # 5 Perioden gemessen… Unschön…
    T_plus = np.concatenate([T_plus_links, T_plus_rechts])
    T_plus_avg = tools.ufloat_from_list(T_plus) * ureg('s')
    print(f"{T_plus_avg=}")
    print(f"- T_plus_links={tools.ufloat_from_list(T_plus_links)}")
    # print(f"- T_std_links={np.std(T_plus_links)}")
    print(f"- T_plus_rechts={tools.ufloat_from_list(T_plus_rechts)}")
    # print(f"- T_std_rechts={np.std(T_plus_rechts)}")

    T_diff_lr = abs(tools.ufloat_from_list(T_plus_links) - tools.ufloat_from_list(T_plus_rechts))
    T_diff_lr_tolerance = min(np.std(T_plus_links), np.std(T_plus_rechts))
    print(f"Differenz der Schwingungsdauern links/rechts: {T_diff_lr}")
    # „Überprüfen Sie, daß die Schwingungsdauern T₁ und T₂ im Rahmen der Meßgenauigkeit übereinstimmen.“
    print(f"Toleranzgrenze dieser Differenz: {T_diff_lr_tolerance} (→ {'PASS' if T_diff_lr < T_diff_lr_tolerance else 'FAIL'})")

    ω_plus_theo = ((ureg.gravity / l)**.5).to('rad/s')
    ω_plus_avg = (2 * np.pi * ureg.rad) / T_plus_avg
    print(tools.fmt_compare_to_ref(ω_plus_avg, ω_plus_theo, name='ω_plus'))


    print("\n→ Gegensinnige Schwingung")
    T_minus = get_T(i, 'gegensinnig') / 5 # 5 Perioden gemessen… Unschön…
    T_minus_avg = tools.ufloat_from_list(T_minus) * ureg('s')
    print(f"{T_minus_avg=}")

    # Kopplungskonstante
    K = (T_plus_avg**2 - T_minus_avg**2) / (T_plus_avg**2 + T_minus_avg**2)
    K *= ureg('m/s²') # !?
    print(f"{K=}")

    ω_minus_theo = ((ureg.gravity / l + 2*K/l)**.5).to('rad/s')
    ω_minus_avg = (2 * np.pi * ureg.rad) / T_minus_avg
    print(tools.fmt_compare_to_ref(ω_minus_avg, ω_minus_theo, name='ω_minus'))


    print("\n→ Gekoppelte Schwingung")
    # nur für die Tabelle:
    T = get_T(i, 'gekoppelt_periode') / 5 # 5 Perioden gemessen… Unschön…
    T_avg = tools.ufloat_from_list(T)
    print(f"{T_avg=}")

    T_S = get_T(i, 'gekoppelt_schwebung') # *eine* Schwebungsdauer gemessen
    T_S_avg = tools.ufloat_from_list(T_S) * ureg('s')
    print(f"{T_S_avg=}")
    T_S_formel = (T_plus_avg * T_minus_avg) / (T_plus_avg - T_minus_avg)
    print(f"{T_S_formel=}")
    print(tools.fmt_compare_to_ref(T_S_avg, T_S_formel, name='T_S'))

    # Ich habe keine Ahnung, was hier passiert… ¯\_(ツ)_/¯
    ω_S_avg = (2 * np.pi * ureg.rad) / T_S_avg
    ω_S_formel = abs(ω_plus_avg - ω_minus_avg) # :/
    ω_S_theo = abs(ω_plus_theo - ω_minus_theo) # :/

    print(f"{ω_S_avg=}")
    print(f"{ω_S_formel=}")
    print(f"{ω_S_theo=}")

    print(tools.fmt_compare_to_ref(ω_S_avg, ω_S_formel, name='ω_S_avg vs. ω_S_formel'))

    print('\n' + '–'*10 + '\n')
