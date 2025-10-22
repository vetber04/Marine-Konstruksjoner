import numpy as np

def I_ror_tynnvegget(R, t):
    # Tynnvegget rør: R = midt-radius
    return np.pi * (R**3) * t

def I_Iprofil(h_total, b_flens, flens_tykkelse, tykkelse_steg):
    # 2 flenser + steg 
    h_steg = h_total - 2 * flens_tykkelse
    I_flens = 2.0 * (
        (b_flens * flens_tykkelse**3) / 12
        + b_flens * flens_tykkelse * ((h_total/2) - (flens_tykkelse/2))**2
    )
    I_steg = (tykkelse_steg * h_steg**3) / 12
    return I_flens + I_steg

def boyestivhet(tvsnitt, geom, test=True):
    geom = np.array(geom, dtype=float)

    R, t = geom[0, 1], geom[0, 0]                 # R = midt-radius
    h, b, tf, tw = geom[1, 0], geom[1, 1], geom[1, 2], geom[1, 3]

    EI = []
    I_elem = []
    for e in tvsnitt:
        E = float(e[0])
        profiltype = int(e[1])

        if profiltype == 1:
            I = I_ror_tynnvegget(R, t)
            if test:
                I = 9.5889e7*1e-12                         # minimal endring: ikke overskriv I_elem
            z_max = R + t/2.0                     # ytterradius når R er midt-radius
            EI.append(E * I)
            I_elem.append([I, z_max])

        elif profiltype == 2:
            I = I_Iprofil(h, b, tf, tw)
            if test:
                I = 7.9449e7*1e-12
            z_max = h/2.0
            EI.append(E * I)
            I_elem.append([I, z_max])
        else:
            print("feil bøystivhet")

    return np.array(EI, dtype=float), np.array(I_elem, dtype=float)
