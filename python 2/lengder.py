import numpy as np
from lesinput import lesinput

input = lesinput()

def lengder(punkt, MNPC):

    elemlen = np.array([])
    # Beregner elementlengder vha. Pythagoras
    for i in MNPC:
        dx = punkt[i[1], 0] - punkt[i[0], 0]
        dy = punkt[i[1], 1] - punkt[i[0], 1]
   
        elemlen = np.append(elemlen, np.sqrt(dx*dx + dy*dy))

    return elemlen