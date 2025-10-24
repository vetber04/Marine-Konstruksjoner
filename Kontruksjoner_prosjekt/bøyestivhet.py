import numpy as np

def I_ror_tynnvegget(R, t):
    return (np.pi/4)*(R**4-(R-t)**4)

def I_Iprofil(h_total, b_flens, flens_tykkelse, tykkelse_steg):
    # 2 flenser + steg 
    h_steg = h_total - 2 * flens_tykkelse
    I_flens = 2.0 * (
        (b_flens * flens_tykkelse**3) / 12
        + b_flens * flens_tykkelse * ((h_total/2) - (flens_tykkelse/2))**2
    )
    I_steg = (tykkelse_steg * h_steg**3) / 12
    return I_flens + I_steg

def boyestivhet(tvsnitt, geom, elemgruppe):

    geom = np.array(geom, dtype=float)

    EI = []
    I_elem = []
    for i, e in enumerate(tvsnitt):
        E = float(e[0])
        profiltype = int(e[1])
        g = int(elemgruppe[i, 1]) 
        if profiltype == 1:
            R, t = geom[g, 1], geom[g, 0]
            I = I_ror_tynnvegget(R, t)
            z_max = R                 
            EI.append(E * I)
            I_elem.append([I, z_max])

        elif profiltype == 2:
            h, b, tf, tw = geom[g, 0], geom[g, 1], geom[g, 2], geom[g, 3]
            I = I_Iprofil(h, b, tf, tw)
            z_max = h/2.0
            EI.append(E * I)
            I_elem.append([I, z_max])
        else:
            print("feil bøystivhet")

    return np.array(EI, dtype=float), np.array(I_elem, dtype=float)
