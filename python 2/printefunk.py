import numpy as np

def fmt_arr(a, fmt="{:.2e}"):
        a = np.asarray(a, dtype=float)
        if a.ndim == 1:
            return "[" + ", ".join(fmt.format(x) for x in a) + "]"
        elif a.ndim == 2:
            rows = ["[" + ", ".join(fmt.format(x) for x in row) + "]" for row in a]
            return "[\n  " + ",\n  ".join(rows) + "\n]"
        else:
            return np.array2string(a)