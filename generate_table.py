from uncertainties import ufloat

def wrapper_num(content):
    return r"\num{" + content + "}"

def n_digits(num, n):
    return ('{0:.'+str(n)+'f}').format(num)

def depint(num):
    # Tupel für uncertainty?
    try:
        return num.m
    except:
        return num

def stringify(value, scientific, fmt=[]):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    elif isinstance(value, int):
        return wrapper_num(str(value))
    else:
        try:
            if 'd' in fmt:
                d = fmt['d']
                if isinstance(d, tuple):
                    return wrapper_num(n_digits(value.n, d[0])) + " ± " + wrapper_num(n_digits(value.s, d[1]))
                else:
                    # return wrapper_num(n_digits(depint(value), d))
                    # CHANGED: Wir benutzen SIUNITX zum alignen, da stört \num{…} nur…
                    return n_digits(depint(value), d)

            return "TODO"

        except Exception as e:
            print(e)
            print("That didn't work:", value)
            print("Got a", type(value))
            return wrapper_num(f"{value}")

def generate_table(name, rows, **kwargs):
    with open(f"build/{name}.tex", 'w') as f:
        numCols = len(rows[0])
        col_fmt = kwargs.get('col_fmt', [None]*numCols)
        if headers := kwargs.get('headers'):
            f.write('% ' + ' | '.join(headers) + '\n')

        #TODO: einmal umgekehrt betrachten, um die maxColWidth zu errechnen…
        maxColWidth = [max([len(stringify(r[i_col], kwargs.get('scientific', False), col_fmt[i_col])) for r in rows]) for i_col in range(numCols)]

        for row in rows:
            for i, col in enumerate(row):
                col_out = stringify(col, kwargs.get('scientific', False), col_fmt[i])
                thisColWidth = len(col_out)
                f.write(col_out)
                f.write(" " * (maxColWidth[i] - thisColWidth))
                f.write((r" \\" + '\n') if (i == numCols - 1) else " & ")
