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

def boyestivhet(tvsnitt, geom, oving8=False, test=False, dbeam=True):
    if oving8:
        EI = tvsnitt[:, 0]
        print("Bøyestivheter EI fra inputfil (kN·m²):", EI)
        return EI # EI er oppgitt direkte i inputfil
    # Ellers regner vi ut I for de ulike profilene
    if dbeam:
        ipe = 7.9449e7
        ror = 9.5889e7
        I = [ror, ror, ror, ipe, ror, ror, ipe, ror, ror, ipe, ipe]
        E = 210e3  # N/mm^2 (= MPa)
        return np.array(E * np.array(I) * 1e-6)  # -> N·m^2
    if test:
        I = 2.8981e6   # mm^4
        E = 210e3      # N/mm^2 (= MPa)
        EI = E * I * 1e-6   # -> N·m^2
        return np.array([[EI], [EI]])  

    
    geom = np.array(geom)

    
    R, t = geom[0, 0], geom[0, 1]
    h, b, tf, tw = geom[1, 0], geom[1, 1], geom[1, 2], geom[1, 3]


    EI = []
    for e in tvsnitt:
        E = float(e[0])
        profiltype = int(e[1])

        if profiltype == 1:
            I = I_ror_tynnvegget(R, t)
            EI.append(E * I)
        elif profiltype == 2:
            I = I_Iprofil(h, b, tf, tw)
            EI.append(E* I)
            
        else:
            EI.append(np.nan)  
    return np.array(EI)

