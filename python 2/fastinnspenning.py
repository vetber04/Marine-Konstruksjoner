import numpy as np

def fastinnspenning(npunkt, lastedata, MNPC, lengder):
    """
    Bygger høyresiden for K*theta = R_nodal - S_fast
    Konvensjon: rotasjon med klokka (+), moment med klokka (+).
    tl:
      1 = punktlast P inne på element (q1a = alpha, q2P = P, nedover > 0)
      2 = lineært fordelt last q1->q2 langs element (N/m, nedover > 0)
      3 = nodemoment M i knutepunkt (med klokka > 0, last[4] = knutepunkt-id)
    """
    R_kp = np.zeros(int(npunkt), dtype=float)  # (momenter)
    S_fast  = np.zeros(int(npunkt), dtype=float)  # fastinnspenningsmomenter

    for last in lastedata:
        tl     = int(last[0])
        elemnr = int(last[1])
        q1a    = float(last[2])
        q2P    = float(last[3])

        if tl == 1:
            # Punktlast P på element 'elemnr' ved a = alpha*L fra venstre ende (nedover > 0)
            L = float(lengder[elemnr])
            A, B   = int(MNPC[elemnr, 0]), int(MNPC[elemnr, 1])
            alpha  = q1a
            P      = q2P
            a = alpha * L
            b = L - a
            # Med klokka positiv (nedoverlast gir strekk i bunn):
            M_A = - P * a * (b**2) / (L**2)   
            M_B = + P * (a**2) * b   / (L**2) 
            S_fast[A] += M_A
            S_fast[B] += M_B

        elif tl == 2:
            # Trapeslast q1->q2 (N/m) på element 'elemnr'
            L = float(lengder[elemnr])
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

        else:
            raise ValueError(f"Ukjent lastetype tl={tl}")

    R_eff = R_kp - S_fast
    return R_eff

