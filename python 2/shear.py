import numpy as np

#Skjærbidrag fra endemomenter
def Q_endemoment(M_ende, lengder, Q):
    for e in range(len(M_ende)):
        M1, M2 = M_ende[e]
        V = (M2 - M1) / lengder[e]
        Q[e, 0] += V     
        Q[e, 1] += V   
    return Q

# Skjærbidrag fra ytre laster
def Q_laster(lastdata, lengder, M_ende, M_under_P, Q): 
    for last in lastdata:
        tl = int(last[0])
        e  = int(last[1])
        a_q1 = float(last[2])
        P_q2 = float(last[3])
        if tl == 1:
            P = P_q2
            alpha = a_q1
            #bjelke forløper fra venstre til høyre
            QA  = P*(1 - alpha)   
            QB = -P*alpha        
            Q[e, 0] += QA
            Q[e, 1] += QB
        elif tl == 2:
            q1 = a_q1
            q2 = P_q2
            L  = lengder[e]

            QA = L * (0.35*q1 + 0.15*q2)
            QB = L * (0.15*q1 + 0.35*q2)

            Q[e, 0] += QA
            Q[e, 1] += QB
    
    return Q

def Q_superpos(lastedata, M_ende, lengder, M_under_P):
    Q = np.zeros((len(lengder), 2))
    M_ende_global = np.zeros((len(M_ende),2))
    for e in range(len(M_ende)):
        M_ende_global[e] = M_ende[e]
        M_ende_global[e,0] = -M_ende[e,0]

    Q = np.zeros((len(lengder), 2))
    Q += Q_laster(lastedata, lengder, M_ende_global, M_under_P, Q)
    Q += Q_endemoment(M_ende_global, lengder, Q)
    return Q