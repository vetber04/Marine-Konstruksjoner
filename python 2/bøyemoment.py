import numpy as np

def bøyespenning(elem,M_mid_last_fordelt, M_under_punkt,M_ende,EI,E,geom,tverrsnittype):
    bøyemomenter=np.zeros(nelem,3)
    
    for e in elem:
        I= EI[e] / E[e]

        if tverrsnittype[e]==1:
            z_maks=geom[e]/2
        elif tverrsnittype[e]==2:
            z_maks=geom[e][0]/2
        else:
            raise ValueError("Ugyldig tverrsnittype")


        bøye_e=np.zeros(3)

        bøyemoment= M_ende[e][0] / I *z_maks
        bøye_e[0]=bøyemoment

        bøyemoment= M_ende[e][1] / I *z_maks
        bøye_e[1]=bøyemoment

        if M_mid_last_fordelt[e] != 0:
            bøyemoment= M_mid_last_fordelt[e] / I *z_maks
            bøye_e[2]=bøyemoment

        elif M_under_punkt[e] != 0:
            bøyemoment= M_under_punkt[e]/ I *z_maks
            bøye_e[2]=bøyemoment
        
        bøyemomenter[e,:]=bøye_e
    return bøyemomenter




        

   
   

