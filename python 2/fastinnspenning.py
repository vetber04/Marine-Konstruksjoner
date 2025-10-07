import numpy as np
from lesinput import lesinput
from lengder import lengder
# tl: type last: punkt = 1 gjevnt fordelt = 2 moment = 3
# elemnr: elementnr (må hente hvilke rotasjoner fra MNPC)
# q1a: 1: q ved knutepunkt A MNPC[0], 2: alfa (punktlast avstand fra ventre ende), 3: Moment [kN/m]
# q2P: 1: q ved knutepunkt B MNPC [1], 2: punktlast P kN
def fastinnspenning(npunkt,lastedata, MNPC, lengder): 
    R = np.zeros(npunkt)
    for last in lastedata:
        tl = last[0] 
        elemnr = int(last[1])
        q1a = last[2]
        q2P = last[3]
        L = lengder[elemnr]
        if tl == 1:
            P = q2P
            a = q1a
            b = 1-a
            

            R[MNPC[elemnr, 0]] += -(P*a*(b**2))/(L**2)
            R[MNPC[elemnr, 1]] += -(P*a*(b**2))/(L**2)
        elif tl == 2:
            
            #Lineært fordelt last med endeverdier q1 og q2
            q1 = q1a  # ved ende 1 (nedover > 0)
            q2 = q2P  # ved ende 2 (nedover > 0)

            M1 =  L**2 * (q1/20.0 + q2/30.0)
            M2 =  -L**2 * (q1/30.0 + q2/20.0)
            R[MNPC[elemnr, 0]] += M1
            R[MNPC[elemnr, 1]] += M2
            
        elif tl == 3:
            M1 = q1a
            # Kun rotasjonspunkt
            R[MNPC[elemnr, 0]] += M1
        
    return R









    

