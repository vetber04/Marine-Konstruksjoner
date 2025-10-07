import numpy as np

def I_ror_tynnvegget(R, t):
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

def boyestivhet(tvsnitt, geom):

    geom = np.array(geom)

    
    R, t = geom[0, 0], geom[0, 1]
    h, b, tf, tw = geom[1, 0], geom[1, 1], geom[1, 2], geom[1, 3]


    EI = []
    for rad in tvsnitt:
        E = float(rad[0])
        profiltype = int(rad[1])

        if profiltype == 1:
            I = I_ror_tynnvegget(R, t)
            EI.append(E * I)
        elif profiltype == 2:
            I = I_Iprofil(h, b, tf, tw)
            EI.append(E* I)
            
        else:
            EI.append(np.nan)  
    return np.array(EI)

