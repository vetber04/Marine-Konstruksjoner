import numpy as np


def M_spenning(M_ende, M_upl , M_fl, I_og_Z_max):
    
    bøyespenninger_ender = np.zeros((len(M_ende), 2))
    bøyespenninger_under_punktlast = np.zeros(len(M_upl))
    bøyespenninger_midt_fordelt_last = np.zeros(len(M_fl))

    for e in range(len(M_ende)):
        M1, M2 = M_ende[e]
        I, Z_max = I_og_Z_max[e]

        sigma_M_1 = (M1/I)*Z_max
        sigma_M_2 = (M2/I)*Z_max
        bøyespenninger_ender[e, 0] = sigma_M_1
        bøyespenninger_ender[e, 1] = sigma_M_2
    
    for e in range(len(M_upl)):
        M = M_upl[e]
        I, Z_max = I_og_Z_max[e]
        Z_max = I_og_Z_max[e, 1]
        sigma_M = (M/I)*Z_max

        bøyespenninger_under_punktlast[e] = sigma_M
    
    for e in range(len(M_fl)):
        M = M_fl[e]
        I, Z_max = I_og_Z_max[e]
        Z_max = I_og_Z_max[e, 1]
        sigma_M = (M/I)*Z_max

        bøyespenninger_midt_fordelt_last[e] = sigma_M

    return bøyespenninger_ender, bøyespenninger_under_punktlast, bøyespenninger_midt_fordelt_last 










    
        
        







        

   
   

