# Kleiner Helfer, um einen „schönen“ Index auf GitHub Pages zu generieren.

import pathlib

cwd = pathlib.Path.cwd()

def protokolle():
    return sorted([file.relative_to(cwd) for file in cwd.glob('[DV]*')], key=lambda x: x.parts[0][1:4])

def abbildungen(protokoll):
    return sorted(protokoll.glob('content/img/*.pdf'))


protokolle_list = protokolle()

out = ''
out += '# Protokolle\n\n'
out += '\n'.join([f'- [{x.parts[0]}]({x}/build/main.pdf)' for x in protokolle_list]) + '\n'*3
out += '\n\n# Abbildungen\n\n'
for protokoll in protokolle_list:
    abb_list = abbildungen(protokoll)
    if len(abb_list) == 0:
        continue
    out += f'- {protokoll.parts[0]}\n'
    out += '\n'.join([f'\t- [{x.parts[-1]}]({x})' for x in abb_list]) + '\n'*3

print(out)
