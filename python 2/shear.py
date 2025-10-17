import numpy as np

#Skjærbidrag fra endemomenter
def Q_endemoment(M_ende, lengder):
    
    Q = np.zeros((len(lengder), 2))
    for e in range(len(M_ende)):
        M1, M2 = M_ende[e]
        V = -(M2 + M1) / lengder[e]
        Q[e, 0] += V     
        Q[e, 1] += V   
    return Q

# Skjærbidrag fra ytre laster
def Q_laster(lastedata, lengder, M_ende, M_under_P): 
    Q = np.zeros((len(lengder), 2))
    for tl, e, a_q1, P_q2 in lastedata:
        e = int(e)
        if int(tl) == 1:
            alpha = a_q1
            P = P_q2
            a = alpha * lengder[e]
            M1 = M_ende[e, 0]
            M2 = M_ende[e, 1]
            M_P = M_under_P[e]          
            L   = lengder[e]
            print(M1*56, M2*56, M_P*56, a, L)


            QA = (M_P - M1) / a
            QB = (M2 - M_P) / (L - a)

            Q[e, 0] += QA
            Q[e, 1] -= QB

        elif int(tl) == 2:
            Q = np.zeros((len(lengder), 2))
    return Q

def Q_superpos(lastedata, M_ende, lengder, M_under_P):
    Q = np.zeros((len(lengder), 2))
    Q +=  Q_laster(lastedata, lengder, M_ende, M_under_P)
    #Q_em = Q_endemoment(M_ende, lengder)
    return Q