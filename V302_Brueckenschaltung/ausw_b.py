from uncertainties import ufloat
import uncertainties.unumpy as unp

C2 = [750, 450]
R3 = [630, 508]
R4 = [370, 492]
R2 = [267, 438.5]
R2 = [ufloat(x, (3/100)*x) for x in R2]

# CX [nF] = [440.476190476191, 435.826771653543]
# RX = [454.621621621622, 452.760162601626]


R3divR4 = [ufloat(r3/r4, (r3/r4)*(0.5/100)) for (r3, r4) in zip(R3, R4)]
R4divR3 = [1/x for x in R3divR4]

CX_calc = [c2*r4divr3 for (c2, r4divr3) in zip(C2, R4divR3)]
CX_merged = sum(CX_calc)/len(CX_calc)

RX_calc = [r2*r3divr4 for (r2, r3divr4) in zip(R2, R3divR4)]
RX_merged = sum(RX_calc)/len(RX_calc)

print(f"{R3divR4=}\n\n{R4divR3=}\n\n{CX_calc=}\n\n{CX_merged=}\n\n{RX_calc=}\n\n{RX_merged=}")
