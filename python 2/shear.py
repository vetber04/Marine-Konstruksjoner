import numpy as np

def Q_superpos(lastedata, M_ende, lengder, scale=1):
    """
    Konvensjon:
      - M_ende[e,0] = venstre ende (CCW +)
      - M_ende[e,1] = høyre  ende (CW +)
      - Skjær oppover = positiv

    Endeskjær:
      V_m = (M2 - M1) / L   <-- viktig endring
      Q_left  =  V_m + lastbidrag
      Q_right = -V_m + lastbidrag
    """
    M_ende  = np.asarray(M_ende, dtype=float)
    lengder = np.asarray(lengder, dtype=float)
    lastdata = np.asarray(lastedata)
    nelem = len(lengder)

    Q = np.zeros((nelem, 2), dtype=float)

    # 1) Skjær fra endemomenter (bruk differanse)
    for e in range(nelem):
        M1, M2 = M_ende[e, 0], M_ende[e, 1]
        L = float(lengder[e])
        V_m = (M2 - M1) / L
        Q[e, 0] +=  V_m
        Q[e, 1] += V_m
        

    # 2) Hopp fra laster
    for last in lastdata:
        tl = int(last[0]); e = int(last[1])
        L = float(lengder[e])

        if tl == 1:            # punktlast
            alpha = float(last[2]); P = float(last[3])
            Q[e, 0] +=  -P*(1 - alpha)
            
            Q[e, 1] += P*alpha
            

        elif tl == 2:          # trapeslast q1 -> q2 (ned>0)
            q1 = float(last[2]); q2 = float(last[3])
            Q[e, 0] += L*(0.35*q1 + 0.15*q2)
            Q[e, 1] += L*(0.15*q1 + 0.35*q2)
    return Q
