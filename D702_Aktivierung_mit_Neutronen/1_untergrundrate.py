import pint
ureg = pint.UnitRegistry()
import tools

NU = [129, 143, 144, 136, 139, 126, 158]
NU /= ureg('300 s') # Messintervall

NU_mean = tools.ufloat_from_list(NU)

def untergrundrate(ureg2):
    return NU_mean.m * ureg2('1/s')

if __name__ == '__main__':
    print(f"Zählrate: {NU_mean}")
    print(f"Anzahl: {NU_mean*ureg('300 s')}")
