from uncertainties import ufloat

def wrapper_num(content):
    return r"\num{" + content + "}"

def stringify(value, scientific):
    if isinstance(value, str):
        return value
    elif isinstance(value, int):
        return wrapper_num(str(value))
    # elif isinstance(value, ufloat):
    else:
        try:
            if scientific:
                return wrapper_num(f"{value.n:.3e}") + " ± " + wrapper_num(f"{value.s:.3e}")
            else:
                return wrapper_num(f"{value.n:.3f}") + " ± " + wrapper_num(f"{value.s:.3f}")
        except: #numpy.float64' object has no attribute 'n'
            # return wrapper_num(f"{value:.3f}")
            return wrapper_num(f"{value}")
    # else:
        # return foo.__str__()

def generate_table(name, rows, **kwargs):
    with open(f"build/{name}.tex", 'w') as f:
        numCols = len(rows[0])

        #TODO: einmal umgekehrt betrachten, um die maxColWidth zu errechnen…
        maxColWidth = [max([len(stringify(r[i_col], kwargs.get('scientific', False))) for r in rows]) for i_col in range(numCols)]

        for row in rows:
            for i, col in enumerate(row):
                col_out = stringify(col, kwargs.get('scientific', False))
                thisColWidth = len(col_out)
                f.write(col_out)
                f.write(" " * (maxColWidth[i] - thisColWidth))
                f.write((r" \\" + '\n') if (i == numCols - 1) else " & ")
