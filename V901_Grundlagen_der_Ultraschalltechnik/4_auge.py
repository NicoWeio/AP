import numpy as np
import pandas as pd # nur für eine schöne Tabelle
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

import tools

# gegeben in der Versuchsanleitung:
c_L = ureg('2500 m/s') # Linse
c_GK = ureg('1410 m/s') # Glaskörperflüssigkeit
# recherchierter Literaturwert:
c_K = ureg('1492 m/s') # vordere/hintere Augenkammer → genähert als Wasser

names = ['Hornhaut-Linse', 'Innerhalb der Linse', 'Linse-Retina']
t = [11.7, 16.2, 22.8] # unsere
# t = [11.4, 16.3, 23.2] # dormail
c_list = tools.pintify([c_GK, c_L, c_GK])

t.insert(0, 0) # Füge eine Null am Anfang hinzu, damit np.diff den ersten Wert unverändert ausgibt.
Δt = np.diff(t)
Δt *= ureg('µs')

Δd = (Δt * c_list / 2).to('mm')
d = np.cumsum(Δd)

df = pd.DataFrame(list(zip(Δt.m, c_list.m, Δd.m, d.m)), columns=['Δt', 'c_list', 'Δd', 'd'])
print(df.head(len(Δt)))
