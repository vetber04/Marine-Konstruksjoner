import numpy as np
k_fjær = 1e6

def rotasjonsfjær(K, r_fixed, k_fjær):
    for r in r_fixed:
        K[int(r), int(r)] += float(k_fjær)



def systemstivhetsmatrise8(MNPC, npunkt, tvsnitt, punkt):
    K = np.zeros((npunkt, npunkt), dtype=float)
    #Lager stivhetsmatrisen k_i
    def K_i(EIL):

        return (EIL) * np.array([[4.0, 2.0],[2.0, 4.0]])
        #return np.array([[4.0, 2.0],[2.0, 4.0]]) #for å teste bare k verdier
    #legger den inn systemstivhetsmatrise
    for e in range(len(tvsnitt)):
        ke = K_i(tvsnitt[e, 0]) 
        i, j = MNPC[e, 0], MNPC[e, 1]
        idx = [i, j]
        K[np.ix_(idx, idx)] += ke 
    
    fixed_r = [int(n) for n in range(punkt.shape[0]) if punkt[n, 2] == 1]
    rotasjonsfjær(K, fixed_r, k_fjær)
           
    return K




