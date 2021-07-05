import itertools
import numpy as np
import pandas as pd
from generate_table import generate_table

α1, α2 = np.genfromtxt(f'data/Reflexionsgesetz.csv', comments='#', delimiter=',', unpack=True)
generate_table(f'tab/mess_reflexionsgesetz', list(zip(α1, α2)), col_fmt=[{'d': 0},{'d': 2}])


α, β = np.genfromtxt(f'data/Brechungsgesetz.csv', comments='#', delimiter=',', unpack=True)
generate_table(f'tab/mess_brechungsgesetz', list(zip(α, β)), col_fmt=[{'d': 0},{'d': 2}])


# α1, α2_grün, α2_rot = np.genfromtxt(f'data/Prisma.csv', comments='#', delimiter=',', unpack=True)
# generate_table(f'tab/mess_prisma', list(zip(α1, α2_grün, α2_rot)), col_fmt=[{'d': 0},{'d': 2},{'d': 2}])


# –––

d_list = [100, 300, 600] # Gitterkonstante
colors = ['gruen', 'rot']

files = [f'data/Beugung_{d}_{color}.csv' for d, color in itertools.product(d_list, colors)] # Dateipfade generieren
df_list = [pd.read_csv(file, comment='#', delimiter='\t', header=None, index_col=0) for file in files] # jeweils die Daten in ein DataFrame laden
df = pd.concat(df_list, axis=1) # die DataFrames unter Berücksichtigung des Index `k` zusammenführen
df.reset_index(level=0, inplace=True) # den Index `k` zu einer normalen Spalte machen, damit er gleich mit ausgegeben wird
# df['k'] = df.index # Alternative, die den `k`-Index beibehält

generate_table(f'tab/mess_beugung', df.to_numpy(), col_fmt=[{'d': 0}]+[{'d': 2}]*len(df_list), headers=['k'] + files)
