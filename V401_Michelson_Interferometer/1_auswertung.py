import numpy as np
import tools

import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

print('a) Bestimmung der Wellenlänge des Lasers\n')
Z_list = np.genfromtxt('data/wellenlaenge.dat', unpack=True)
# Wie viele „Perioden“ das Interferenzmuster durchläuft
Z = tools.ufloat_from_list(Z_list)
print(f"{Z=}")

# große Änderung der Mikrometerschraube → kleine Änderung des Spiegels
uebersetzung = 5.017 # auf der Apparatur angegeben

ΔSchraube = ureg('5 mm') # Wegänderung der Schraube
Δd = ΔSchraube / uebersetzung # Wegänderung des Spiegels
Δw = 2 * Δd # Änderung der optischen Weglänge (hin und zurück)

λ = Δw / Z

λ_angegeben = ureg('635 nm') # am Laser angegeben

print("- gemessen:", λ.to('nm'))
print("- angegeben:", λ_angegeben)
print("- Abweichung:", tools.fmt_err(λ, λ_angegeben, precise=True))

# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

print('\nb) Bestimmung des Brechungsindex von Luft\n')
# ACHTUNG: ÜBERSCHREIBE Z aus Part 1!
Z_list = np.genfromtxt('data/brechungsindex.dat', unpack=True)
Z_list = Z_list[::2] # berücksichtige nur die (kleineren) Werte für negative Druckänderungen
Z = tools.ufloat_from_list(Z_list)
print(f"{Z=}")

b = ureg('50 mm') # Länge der Messkammer
p_0 = ureg('1.01325 bar') # Normalbedingungen (→ Versuchsanleitung)
Δp = ureg('0.6 bar') # Druckdifferenz
Δn = (Z * λ_angegeben) / (2 * b)
Δn.ito('dimensionless')
T = ureg('293.15 K') # 20 °C
T_0 = ureg('273.15 K') # Normalbedingungen (→ Versuchsanleitung)

n = 1 + Δn * (T / T_0) * (p_0 / Δp)
n_lit = 1.000272 # → https://www.spektrum.de/lexikon/physik/brechzahl/1958
Δn_lit = (n_lit - 1) / ((T / T_0) * (p_0 / Δp))

print("n:")
print("- gemessen:", n)
print("- Literaturwert:", n_lit)
print("- Abweichung:", tools.fmt_err(n, n_lit, precise=True))
print("Δn:")
print("- gemessen: ", Δn)
print("- Literaturwert:", Δn_lit)
print("- Abweichung:", tools.fmt_err(Δn, Δn_lit, precise=True))
