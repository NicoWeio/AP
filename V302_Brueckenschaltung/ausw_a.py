from uncertainties import ufloat
import uncertainties.unumpy as unp

R2 = [664, 332, 332, 664]
R3 = [317, 483, 488, 323]
R4 = [683, 517, 512, 677]
# RX = [308.181551976574, 310.166344294004, 316.4375, 316.797636632201]

R3divR4 = [ufloat(r3/r4, (r3/r4)*(0.5/100)) for (r3, r4) in zip(R3, R4)]
RX_calc = [r2*r3divr4 for (r2, r3divr4) in zip(R2, R3divR4)]
RX_merged = sum(RX_calc)/len(RX_calc)

print(f"{R3divR4=}\n\n{RX_calc=}\n\n{RX_merged=}")
