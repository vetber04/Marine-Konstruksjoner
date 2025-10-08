import numpy as np
from fastinnspenning import fastinnspenning

def M_ytrelast(e, R, lastdata, nelem, lengder):
    if e not in lastdata[:, 1]:
        return np.array([0.0, 0.0])
    
    S_i_fast = np.array([0.0, 0.0])
    lastdata_e = lastdata[lastdata[:, 1] == e]
    for last in lastdata_e:
        tl = last[0] 
        elemnr_ml = int(last[1])
        q1a = last[2]
        q2P = last[3]
        L = lengder[elemnr_ml]
        if tl == 1:
            P = q2P
            a = q1a*L
            b = (1-a)*L
            
            M1 = -(P*a*(b**2))/(L**2)
            M2 = (P*a*(b**2))/(L**2)

            S_i_fast[0] += -M1
            S_i_fast[1] += -M2
        elif tl == 2:
            
            #Lineært fordelt last med endeverdier q1 og q2
            q1 = q1a  # ved ende 1 (nedover > 0)
            q2 = q2P  # ved ende 2 (nedover > 0)

            M1 =  L**2 * (q1/20.0 + q2/30.0)
            M2 =  -L**2 * (q1/30.0 + q2/20.0)
            S_i_fast[0] += -M1
            S_i_fast[1] += -M2
            
        elif tl == 3:
            M1 = q1a
            # Kun rotasjonspunkt
            S_i_fast += -M1
        
    return S_i_fast
   
    

def endemoment(MNPC, rot, EIL, lengder, nelem, R, lastdata):
    M_ende = np.zeros((nelem, 2))

    for e in range(nelem):
        kp_1 =  MNPC[e, 0] #knutepunkt 1
        kp_2 = MNPC[e, 1] #knutepunkt 2
        r = np.array([rot[kp_1], rot[kp_2]]) #rotasjon for element e
        k_i = EIL[e, 0] * np.array([[4.0, 2.0],[2.0, 4.0]])
        S_i_fast = M_ytrelast(e, R, lastdata, nelem, lengder)
        M_ende[e, :] = k_i @ r + S_i_fast
    return M_ende

