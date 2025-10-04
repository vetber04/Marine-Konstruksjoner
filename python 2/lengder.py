import numpy as np
from lesinput import lesinput

input = lesinput()

def lengder(punkt, MNPC):

    elemlen = np.array([])
    # Beregner elementlengder vha. Pythagoras
    for MNPC in MNPC:
        dx = punkt[MNPC[1], 0] - punkt[MNPC[0], 0]
        dy = punkt[MNPC[1], 1] - punkt[MNPC[0], 1]
        elemlen = np.append(elemlen, np.sqrt(dx*dx + dy*dy))

    return elemlen

