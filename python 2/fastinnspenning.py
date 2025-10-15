import numpy as np
from lengder import lengder


def fastinnspenning(npunkt, lastedata, MNPC, lengder):
    
    R = np.zeros(int(npunkt))

    for last in lastedata:
        tl     = int(last[0]) # lastetype
        elemnr = int(last[1])      
        q1a    = float(last[2])
        q2P    = float(last[3])

        if tl == 1:
            # Punktlast P [N] på elemnr, ved a = alpha*L fra venstre ende.
            L  = float(lengder[elemnr])
            A, B = int(MNPC[elemnr, 0]), int(MNPC[elemnr, 1])
            alpha = q1a
            P     = q2P

            a = alpha * L
            b = L - a

            # Faste endemomenter med klokka positiv:
            M1 = -( P * a * b**2 / L**2 )   # ved kp A
            M2 = +( P * a**2 * b / L**2 )   # ved kp B

            R[A] += M1
            R[B] += M2

        elif tl == 2:
            # Lineært fordelt last på element elemnr: q1a (ved A), q2P (ved B), i N/m
            L  = float(lengder[elemnr])
            A, B = int(MNPC[elemnr, 0]), int(MNPC[elemnr, 1])
            q1, q2 = q1a, q2P

            # Trapeslast, med klokka positiv M:
            M1 =  L**2 * (q1/20.0 + q2/30.0)   # ved node A
            M2 = -L**2 * (q1/30.0 + q2/20.0)   # ved node B

            R[A] += M1
            R[B] += M2

        elif tl == 3:
            # Påført endemoment ved KNUTEPUNKT elemnr (ikke elementnr)
            kp = elemnr
            M = q1a  # N·m, CW positiv
            R[kp] += M

        else:
            raise ValueError("Ukjent lastetype")
    return R



    

