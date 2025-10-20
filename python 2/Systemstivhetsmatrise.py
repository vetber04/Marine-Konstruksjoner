import numpy as np
 #bør være lik størrelseorden som andre diagnoalelementer i K

def fjern_rad_kolloner(K, r_fixed, R, k_diagonal):
    for r in r_fixed:
        K[int(r), :] = 0
        K[:, int(r)] = 0
        K[int(r), int(r)] = k_diagonal
        R[int(r)] = 0
    return K, R



def systemstivhetsmatrise(MNPC, npunkt, tvsnitt, nelem, punkt, lengder, bøyestivheter, R, k_diagonal):
    K = np.zeros((npunkt, npunkt), dtype=float)
    #Lager stivhetsmatrisen k_i
    def K_i(L, EI,):
        return (EI/L) * np.array([[4.0, 2.0],[2.0, 4.0]])
        #return np.array([[4.0, 2.0],[2.0, 4.0]]) #for å teste bare k verdier
    #legger den inn systemstivhetsmatrise
    for e in range(nelem):
        ke = K_i(lengder[e], bøyestivheter[e]) 
        i, j = MNPC[e, 0], MNPC[e, 1]
        idx = [i, j]
        K[np.ix_(idx, idx)] += ke 
    
    fixed_r = [int(n) for n in range(punkt.shape[0]) if punkt[n, 2] == 1]
    fjern_rad_kolloner(K, fixed_r, R, k_diagonal)
           
    return K, R




