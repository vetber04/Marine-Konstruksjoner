import numpy as np

def Q_superpos(lastdata, M_ende, lengder):

    nelem = len(lengder)

    Q = np.zeros((nelem, 2), dtype=float)

    # 1) Skjær fra endemomenter (bruker differanse)
    for e in range(nelem):
        M1, M2 = M_ende[e, 0], M_ende[e, 1]
        L = float(lengder[e])
        V_m = (M2 - M1) / L
        Q[e, 0] -=  V_m
        Q[e, 1] -= V_m
        

    for last in lastdata:
        tl = int(last[0]); e = int(last[1])
        L = float(lengder[e])

        if tl == 1:            # punktlast
            alpha = float(last[2]); P = float(last[3])
            Q[e, 0] +=  P*(1 - alpha)
            
            Q[e, 1] -= P*alpha
            

        elif tl == 2:          # trapeslast 
            q1 = float(last[2]); q2 = float(last[3])
            Q[e, 0] = L * (7/20*q1 + 3/20*q2)   # venstre endeskjær
            Q[e, 1] -= L * (3/20*q1 + 7/20*q2)

    return Q
