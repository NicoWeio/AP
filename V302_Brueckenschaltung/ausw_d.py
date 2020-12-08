from uncertainties import ufloat
import uncertainties.unumpy as unp

R2 = [664, 664, 332]

R3 = [81.5, 137.5, 277.5]
R3 = [ufloat(x, (3/100)*x) for x in R3]

R4 = [608 , 1003, 1003]
R4 = [ufloat(x, (3/100)*x) for x in R4]

C4 = [750, 450, 450] #[nF]
# C4 = [x/(10**3) for x in C4] #[uF]
C4 = [x/(10**6) for x in C4] #[mF]
# C4 = [x/(10**9) for x in C4] #[F]

RX = [89.0065789473684, 91.0269192422732, 91.8544366899302]
# LX = [40587000, 41085000, 41458500] #[nH]
LX = [40.587, 41.085, 41.4585] #[mH]


RX_calc = [(r2*r3)/r4 for (r2, r3, r4) in zip(R2, R3, R4)]
RX_merged = sum(RX_calc)/len(RX_calc)

LX_calc = [l2*r3*c4 for (l2, r3, c4) in zip(R2, R3, C4)]
LX_merged = sum(LX_calc)/len(LX_calc)

print(f"{LX_calc=}\n\n{LX_merged=}\n\n{RX_calc=}\n\n{RX_merged=}")
