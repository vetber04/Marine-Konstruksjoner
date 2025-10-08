import numpy as np

def endemoment(MNPC, rot, EIL, lengder, nelem):
    M_ende = np.zeros((nelem, 2))

    for e in range(nelem):
        kp_1 =  MNPC[e, 0] #knutepunkt 1
        kp_2 = MNPC[e, 1] #knutepunkt 2
        r = np.array([rot[kp_1], rot[kp_2]]) #rotasjon for element e
        k_i = EIL[e, 0] * np.array([[4.0, 2.0],[2.0, 4.0]])
        M_ende[e, :] = k_i @ r
    return M_ende
