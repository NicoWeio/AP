from uncertainties import ufloat
import pint
ureg = pint.UnitRegistry()
ureg.setup_matplotlib()

time_per_div = ureg('100 µs')
time_per_subdiv = time_per_div / 5
subdivs = 5.5
# subdivs = 5.75
u_subdivs = ufloat(subdivs, 1)
time = time_per_subdiv*u_subdivs

print(time)
