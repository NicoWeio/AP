import numpy as np
import pandas as pd
import tools

def prepare(part, names, scale_out):
    print(f"\n\n{part=}")
    scale, scale_y = np.genfromtxt(f'data/{part}_scale.csv', comments='#', unpack=True, delimiter=', ')

    ## Skalen-Transformation bestimmen
    distances = np.diff(scale)
    print(f"{distances=}")
    scale_in = tools.ufloat_from_list(distances)
    print(f"scale_in = {scale_in:.3f}")
    print(f"scale_out = {scale_out:.3f}")
    scale_in = scale_in.n # die Abweichung lassen wir beim Speichern ohnehin aus
    print(f"→ scale_factor = {(scale_out / scale_in):.3f}")

    start_in = np.min(scale)
    start_out = 0

    def val_map(x):
        return (x - start_in) * scale_out / scale_in + start_out

    ## Skalen-Transformation anwenden
    for name in names:
        U, I_A = np.genfromtxt(f'data/{part}_{name}.csv', comments='#', unpack=True, delimiter=', ')
        U = val_map(U)

        df = pd.DataFrame({'U': U, 'I_A': I_A})
        df.to_csv(f'build/dat/{part}_{name}.csv', header=None, index=None)


prepare('energieverteilung', ['23_7', '148'], scale_out = 1)
prepare('franck_hertz', ['166_6', '183_8'], scale_out = 5)

#TODO: y-Achse!
