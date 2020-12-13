import numpy as np
from uncertainties import ufloat
import uncertainties.unumpy as unp

Lrund =  np.array([60.05,61.00,60.00,60.00,60.00]) #cm
Leckig = np.array([60.30,60.30,60.30,60.30,60.34]) #cm
drund =  np.array([10.00,9.95 ,10.00,10.00,10.00]) #mm
aeckig = np.array([12.00,12.00,11.95,12.00,12.00]) #mm
beckig = np.array([10.00,9.95,9.90,9.95,10.00]) #mm

u_Lrund = ufloat(np.mean(Lrund), np.std(Lrund))
u_Leckig = ufloat(np.mean(Leckig), np.std(Leckig))
u_drund = ufloat(np.mean(drund), np.std(drund))
u_aeckig = ufloat(np.mean(aeckig), np.std(aeckig))
u_beckig = ufloat(np.mean(beckig), np.std(beckig))

print('u_Lrund', u_Lrund)
print('u_Leckig', u_Leckig)
print('u_drund', u_drund)
print('u_aeckig', u_aeckig)
print('u_beckig', u_beckig)

# –––––––––

# !!! vmtl. falsch ↓
# # Flächenträgheitsmoment:
# I = (u_aeckig*u_beckig**3)/12
# print("––––––")
# print(f"{I=} mm^4")
