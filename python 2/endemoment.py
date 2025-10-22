import numpy as np

def M_ytrelast(e, lastdata, lengder, MNPC):
    S_i_fast = np.array([0.0, 0.0])

    for last in lastdata:
        tl     = int(last[0])
        elemnr = int(last[1])
        q1a    = float(last[2])
        q2P    = float(last[3])
        L      = float(lengder[elemnr])

        if tl == 1 and e == elemnr:
            # Punktlast P ved a = alpha*L fra venstre ende
            P = q2P
            a = q1a * L
            b = L - a
            M1 =  - P * a * (b**2) / (L**2)   # ved venstre ende (med klokka +)
            M2 =  + P * (a**2) * b / (L**2)   # ved høyre  ende
            S_i_fast[0] += M1
            S_i_fast[1] += M2

        elif tl == 2 and e == elemnr:
            # Lineært fordelt last q1 -> q2 (nedover > 0)
            q1 = q1a
            q2 = q2P
            M1 = - L**2 * (q1/20.0 + q2/30.0)  # venstre ende
            M2 = + L**2 * (q1/30.0 + q2/20.0)  # høyre  ende
            S_i_fast[0] += M1
            S_i_fast[1] += M2

    return S_i_fast


def endemoment(MNPC, rot, bøyestivhet, lengder, nelem, R, lastdata):
    M_ende = np.zeros((nelem, 2))

    for e in range(nelem):
        kp_1 = int(MNPC[e, 0])
        kp_2 = int(MNPC[e, 1])
        r = np.array([rot[kp_1], rot[kp_2]])  # rotasjoner for element e
        k_i = (bøyestivhet[e] / lengder[e]) * np.array([[4.0, 2.0], [2.0, 4.0]])
        S_i_fast = M_ytrelast(e, lastdata, lengder, MNPC)
        # Endemoment = deformasjon + fastinnspenningsbidrag
        M_ende[e, :] = k_i @ r + S_i_fast
    
    M_ende[:, 0] *=-1 #endrer fortegn til global moment konvensjon

    return M_ende


