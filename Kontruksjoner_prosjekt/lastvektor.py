import numpy as np

def lastvektor(npunkt, lastedata, MNPC, lengder):
    #definrer vektorene lastvektor i knutepunkt (R_kp) og fastinnspenningmomenter (S_fast)
    #dimensjonen er lik antall knutepunkt
    R_kp = np.zeros(int(npunkt))  # Lastvektor for laster (momenter) i knutepunkt 
    S_fast  = np.zeros(int(npunkt))  # fastinnspenningsmomenter

    for last in lastedata:
        tl     = int(last[0])   # type last
        elemnr = int(last[1])   # elementnummer (0 indeksert)
        q1a    = float(last[2]) # tl=1: q1 [N/m] eller tl=2: alpha [-]
        q2P    = float(last[3]) # tl=1: q2 [N/m] eller tl=2: P [N]
       
        L      = float(lengder[elemnr]) #finner lengde for element

        # Punktlast P på element 'elemnr' ved a = alpha*L fra venstre ende (nedover > 0)
        if tl == 1:
            #Finner knutepunkt til element i MNPC
            A, B   = int(MNPC[elemnr, 0]), int(MNPC[elemnr, 1]) 
            alpha  = q1a
            P      = q2P
            a      = alpha * L
            b      = L - a
            # Med klokka positiv:
            M_A        = - P * a * (b**2) / (L**2)   
            M_B        = + P * (a**2) * b   / (L**2) 
            #legger innspenningmomenter inn i S_fast vekot i riktig knutepunkt
            S_fast[A] += M_A
            S_fast[B] += M_B 

        elif tl == 2:
            # Trapeslast q1->q2 (N/m) på element 'elemnr'
            
            A, B   = int(MNPC[elemnr, 0]), int(MNPC[elemnr, 1])
            q1, q2 = q1a, q2P
            # Med klokka positiv:
            M_A = - L**2 * (q1/20.0 + q2/30.0)  # venstre
            M_B = + L**2 * (q1/30.0 + q2/20.0)  # høyre
            S_fast[A] += M_A
            S_fast[B] += M_B

        elif tl == 3:
            # Nodemoment M i knutepunkt (med klokka > 0)
            kp = int(last[4])
            M  = q1a
            R_kp[kp] += M  # samme fortegn som definert

    R = R_kp - S_fast
    return R

