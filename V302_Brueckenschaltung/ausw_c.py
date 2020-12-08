from uncertainties import ufloat
import uncertainties.unumpy as unp

L2 = [27.5, 14.6] # [mH]
R2 = [57, 33]
# R2 = [ufloat(x, (3/100)*x) for x in R2] #TODONEW
R3 = [605.5, 740.5]
R4 = [394.5, 259.5]

RX = [87.4866920152091, 94.1676300578035] # [Ohm]
LX = [42.2084917617237, 41.66204238921] # [mH]

R3divR4 = [ufloat(r3/r4, (r3/r4)*(0.5/100)) for (r3, r4) in zip(R3, R4)]

RX_calc = [r2*r3divr4 for (r2, r3divr4) in zip(R2, R3divR4)]
RX_merged = sum(RX_calc)/len(RX_calc)

LX_calc = [l2*r3divr4 for (l2, r3divr4) in zip(L2, R3divR4)]
LX_merged = sum(LX_calc)/len(LX_calc)

print(f"{R3divR4=}\n\n{LX_calc=}\n\n{LX_merged=}\n\n{RX_calc=}\n\n{RX_merged=}")
