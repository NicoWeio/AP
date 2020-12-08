import numpy as np

def quotTheorie(w):
    return np.sqrt((1/9)*((w**2-1)**2)/((1-w**2)**2 + 9*w**2))

f2 = quotTheorie(2)

print(f"{f2=}")
