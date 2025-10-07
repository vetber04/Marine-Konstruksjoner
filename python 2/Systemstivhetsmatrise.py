import numpy as np
k_fjær = 10e6

def rotasjonsfjær(K, r_fixed, k_fjær):
    for r in r_fixed:
        K[int(r), int(r)] += float(k_fjær)



def systemstivhetsmatrise(MNPC, npunkt, tvsnitt, nelem, punkt):
    K = np.zeros((npunkt, npunkt), dtype=float)
    def K_i(EIL):
        #må endre dette når vi ikke regner på oppg 8 må ha bøyestivhet og lengder
        return (EIL) * np.array([[4.0, 2.0],[2.0, 4.0]])
 
    for e in range(nelem):
        ke = K_i(tvsnitt[e, 0]) 
        i, j = MNPC[e, 0], MNPC[e, 1]
        idx = [i, j]
        K[np.ix_(idx, idx)] += ke 
    
    fixed_r = [int(n) for n in range(punkt.shape[0]) if punkt[n, 2] == 1]
    rotasjonsfjær(K, fixed_r, k_fjær)
           
    return K




