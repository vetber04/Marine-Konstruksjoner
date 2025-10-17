import numpy as np

#Moment midt på bjelke kun fra ytre last (linært fordelt)
def M_midt_fordeltlast(lastedata, nelem, lengder):
        M_mid_last = np.zeros(nelem)
        for ei in lastedata:
            tl, e, q1, q2 = ei
            if tl != 2:
                continue

            e = int(e)                # elementindeks
            L = lengder[e]            # elementlengde
            M_mid_last[e] += -(L**2 / 16.0) * (q1 + q2)
        return M_mid_last
#Moment midt på bjelke fra endemoment
def M_midt_endemoment(M_ende, nelem, lastdata):
    M_mid_ende = np.zeros(nelem)
    for last in lastdata:
        tl, e, q1, q2 = last
        if int(tl) == 2:        
            M1, M2 = M_ende[int(e)]
            M_mid_ende[int(e)] = (M1 + M2) / 2.0
        else:
            continue
    return M_mid_ende
     


#Antar kunn en punktlast per element
def M_under_punktlast(lastedata, nelem, M_ende, lengder):
    # M_ende er totale endemomenter (kθ − r_e)
    
    M_under = np.zeros(nelem)
    for last in lastedata:
        tl, e, alpha, P = last
        if int(tl) != 1:
            continue
        e  = int(e) # posisjon punktlast i forhold til elementlengde (0-1)
        M1, M2 = M_ende[e,0], M_ende[e,1]
        M_under[e]  = (1.0 - alpha) * M1 + alpha * M2
        M_under[e] += - P * alpha * (1.0 - alpha) * lengder[e]

    return M_under

def momenterbjelke(lastedata, nelem, lengder, M_ende):  
    M_mid_ende = M_midt_endemoment(M_ende, nelem, lastedata)
    M_mid_last_fordelt = M_midt_fordeltlast(lastedata, nelem, lengder) + M_mid_ende
    M_under_punkt = M_under_punktlast(lastedata, nelem, M_ende, lengder)
    return M_mid_last_fordelt, M_under_punkt
