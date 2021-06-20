import numpy as np
import matplotlib.pyplot as plt
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()
from scipy.signal import find_peaks, peak_widths
from uncertainties import ufloat
import uncertainties.unumpy as unp

import tools

# Für eine schönere Notation im Folgenden. Tut sonst nichts.
ureg.define('impulse = 1 = Imp')

# For reference:
# I beschreibt Impulse (Imp),
# N beschreibt Impulse pro Zeit (Imp/s)
# …wie in „DatenHinweiseCompton.pdf“

τ = ureg('90 µs') # Totzeit; laut Versuchsanleitung

print('### Bestimmung der Transmission als Funktion der Wellenlänge' '\n')

θ_Al, N_Al = np.genfromtxt('data/ComptonAl.dat', unpack=True)
θ_0, N_0 = np.genfromtxt('data/ComptonOhne.dat', unpack=True)
assert np.array_equal(θ_Al, θ_0) # sonst müssten die Daten hier zusammengeführt werden

θ = θ_Al * ureg.deg # = θ_0 * ureg.deg, siehe oben
N_0 *= ureg('Imp/s')
N_Al *= ureg('Imp/s')


def u_N(N): # Berechnung der fehlerbehafteten Zählraten
    t = ureg('200 s') # Integrationszeit
    I = N * t # umrechnen in Gesamt-Impulse
    # Hier ist die Unsicherheit einfach √N
    I_err = np.sqrt(I) * ureg('Imp^.5') # die Unsicherheit soll natürlich dieselbe Einheit wie der Nennwert haben
    N_err = I_err / t # zurück umrechnen in Zählraten
    return tools.uarray(N, N_err)
    # oder kurz: N_err = np.sqrt(N * t) * ureg('Imp^.5') / t

N_0 = u_N(N_0)
N_Al = u_N(N_Al)

def I_totzeitkorrektur(N):
    return N / (1 - τ * N) # Gl. 4 in der Versuchsanleitung

def calc_λ(θ):
    d = ureg('201.4 pm') # Gitterkonstante; laut Versuchsanleitung
    return 2 * d * np.sin(θ) # nach Bragg; n=1

λ = calc_λ(θ)
I_0 = I_totzeitkorrektur(N_0)
I_Al = I_totzeitkorrektur(N_Al)
transmission = I_Al / I_0
transmission_no_TZK = N_Al / N_0

a, b = tools.linregress(λ, tools.nominal_values(transmission))
print(f"{a, b=}")

tools.errorbar(plt, λ, transmission, fmt='.', zorder=5, label='Messwerte')
# tools.errorbar(plt, λ, transmission_no_TZK, fmt='.', zorder=5, label='Messwerte ohne Totzeitkorrektur')
plt.plot(λ, tools.nominal_values(a*λ+b), label='Regressionsgerade')

plt.xlabel('$\lambda \mathbin{/} \si{\pico\meter}$')
plt.ylabel('$T$')
plt.legend()
plt.tight_layout()
plt.savefig('build/plt/transmission.pdf')
# plt.show()


print('\n'*2 + '### Bestimmung der Compton-Wellenlänge' '\n')
# Keine eigene Datei, weil wir gleich die Steigung der zuvor bestimmten Regerssionsgeraden nutzen werden
# und ich dafür nicht extra mit Modulen hantieren will.

def u_I(I):
    # Nicht die Zählrate, sondern die Zahl der tatsächlich gemessenen Impulse ist Poisson-verteilt.
    # Wir rechnen daher den Fehler für die Impulsanzahl aus, bevor wir auf die Zählrate umrechnen.
    return ufloat(I, np.sqrt(I)) * ureg('Imp') # = N

# Daten aus „DatenHinweiseCompton.pdf“:

I_0 = u_I(2731) # ohne Al-Absorper
I_1 = u_I(1180) # mit Al-Absorber zwischen Röntgenröhre und Streuer
I_2 = u_I(1024) # mit Al-Absorber zwischen Streuer und Geiger-Müller-Zählrohr
t = ureg('300 s') # Integrationszeit

N_0 = I_0 / t # ohne Al-Absorper
N_1 = I_1 / t # mit Al-Absorber zwischen Röntgenröhre und Streuer
N_2 = I_2 / t # mit Al-Absorber zwischen Streuer und Geiger-Müller-Zählrohr
print(f'{N_0=}', f'{N_1=}', f'{N_2=}', sep='\n')

max_N_possible = (1 / τ).to('Imp/s')
max_N_measured = max(N_0, N_1, N_2)
assert max_N_possible > max_N_measured * 1e3
print('\n' f'größtmögliche Zählrate = 1/τ = {max_N_possible:.2f} ≫ {max_N_measured:.2f} = größte gemessene Zählrate')
print(f'→ um den Faktor {(max_N_possible / max_N_measured).m.n:.0f} größer!')

T_1 = N_1 / N_0 # Transmission der ungestreuten Röntgenstrahlung
T_2 = N_2 / N_0 # Transmission der gestreuten Röntgenstrahlung
print(f'T_1 = {T_1}', f'T_2 = {T_2}', sep='\n')
λ_1 = (T_1 - b)/a
λ_2 = (T_2 - b)/a
print(f'λ_1 = {λ_1:.2f}')
print(f'λ_2 = {λ_2:.2f}')
λ_C = λ_2 - λ_1 # Compton-Wellenlänge
λ_C_theo = 1 * ureg.h / (ureg.electron_mass * ureg.c)
print(tools.fmt_compare_to_ref(λ_C, λ_C_theo, 'λ_C', unit='pm'))
