import numpy as np

# Midtmoment fra trapeslast 
def M_midt_fordeltlast(lastdata, nelem, lengder):
    M_mid_last = np.zeros(nelem, dtype=float)
    for last in lastdata:
        tl = last[0]
        e = int(last[1])
        q1 = last[2]
        q2 = last[3]
        if int(tl) != 2:
            continue
        
        L = float(lengder[e])   
        M_mid_last[e] += -(L**2) * (float(q1) + float(q2)) / 16.0 
    return M_mid_last

# Midtmoment fra endemomenter:
def M_midt_endemoment(M_ende, nelem, lastdata):
    M_mid = np.zeros(nelem, dtype=float)
    sett = set()
    for last in lastdata:
        tl = last[0]
        e = last[1]
        if int(tl) != 2:
            continue
        e = int(e)
        if e in sett:
            continue
        M1, M2 = M_ende[e]      # i Nm 
        M_mid[e] = 0.5*(M1 + M2)
        sett.add(e)
    return M_mid

# Moment under en punktlast i posisjon a = alpha*L
def M_under_punktlast(lastedata, nelem, M_ende, lengder):
    M_under = np.zeros(nelem, dtype=float)
    for tl, e, alpha, P, M_kp in lastedata:
        if int(tl) != 1:
            continue
        e = int(e)
        L = float(lengder[e])
        a = float(alpha) * L
        b = L - a
        M1, M2 = M_ende[e]
        # Bidrag fra endemomenter:
        M_under[e] += M1 + (M2 - M1) * (a / L)
        # Bidrag fra punktlast 
        M_under[e] += - float(P) * a * b / L
    return M_under

def momenterbjelke(lastedata, nelem, lengder, M_ende):
    M_mid_ende = M_midt_endemoment(M_ende, nelem, lastedata)
    M_mid_last_fordelt = M_midt_fordeltlast(lastedata, nelem, lengder) + M_mid_ende #superpos
    M_under_punkt = M_under_punktlast(lastedata, nelem, M_ende, lengder)
    return M_mid_last_fordelt, M_under_punkt