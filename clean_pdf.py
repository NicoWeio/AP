#!/usr/bin/env python3

"""
Bereinigt die übergebene PDF-Datei, um ihre Erstellung deterministisch/reproduzierbar zu machen.
Schuld an den nicht deterministischen Ausgaben ist offenbar die Zeile `pgf.texsystem : lualatex` in der matplotlibrc.
Neben der hier stattfindenden Ersetzung muss auch sichergestellt werden,
dass die Umgebungsvariable SOURCE_DATE_EPOCH konstant bleibt.
"""

import sys
filename = sys.argv[1]
REPLACEMENT = b'/ID [ <00000000000000000000000000000000> <00000000000000000000000000000000> ]'

with open(filename, 'rb') as f:
    c = f.read()
    index = c.find(b'/ID [ <')
    if index == -1:
        print('No /ID found')
        exit(1)
    new_c = c[:index] + REPLACEMENT + c[index + len(REPLACEMENT):]

if c == new_c:
    print('Unchanged')
    exit(0)

with open(filename, 'wb') as f:
    f.write(new_c)

print('Done')
