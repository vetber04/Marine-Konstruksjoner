# Pakker
import numpy as np
import pandas as pd
# Funksjoner
from lesinput import lesinput
from lengder import lengder
from bøyestivhet import boyestivhet
from lastvektor import lastvektor
from endemoment import endemoment
from momenterbjelke import momenterbjelke
from Systemstivhetsmatrise import systemstivhetsmatrise
from shear import Q_superpos
from bøyespenning import M_spenning
from printefunk import fmt_arr

lesinput = lesinput() #legger inn lesinput funksjon

def main(lesinput, Printe=False): #legger inn verdier
    
    #Flytespenning stål
    fy = 355*1e6 #Mpa
    #Sikkerhetsfakor
    sf = 0.7

    # -----  inputdata ------- 
    # antall knutepunkt, kord. til knutepunkt, antall element, MNPC, tversnitt, geomtri tvsnitt, lastdata
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata, elemgruppe = lesinput

    #beregner lengder for elementer
    elemlen =  lengder(punkt, MNPC) #[m] 
    # Beregner bøyestivhet for alle elementer
    # og aretreghetsmoment og største avstand fra arealsenter
    EI = boyestivhet(tvsnitt, geom, elemgruppe)[0] #[Nm^2]
    I_zmax = boyestivhet(tvsnitt, geom, elemgruppe)[1] #[m^4, m]
    # Setter opp R (last) vektor
    R = lastvektor(npunkt, lastdata, MNPC, elemlen)

    # Setter opp systemstivhetsmatrise K 
    # og legger til grensebetingelse for K og R for faste knutepunkter 
    K, R = systemstivhetsmatrise(MNPC, npunkt, nelem, punkt, elemlen, EI, R, k_diagonal=1)
    
    # Løser ligningssystemet Kr = R 
    rot = np.linalg.solve(K, R) #rotasjoner (rad)
    
    #Beregner momentverdier for alle element ved endene 
    em =endemoment(MNPC, rot, EI, elemlen, nelem, R, lastdata)
    
    #Beregner momentverdier for alle element ved midtpunkt for fordelt last,
    # ,under punktlast, vha. superposisjonsprinsippet
    mb =  momenterbjelke(lastdata, nelem, elemlen, em)
    
    #Beregner skjærkraftverdier for alle element ved ender fra endemoment og ytre laster
    Q = Q_superpos(lastdata, em, elemlen)
    
    #----Bøyespenning-----
    sigma_M =  M_spenning(em, mb[1], mb[0], I_zmax) 
    sigma_ender = sigma_M[0]
    sigma_punkt = sigma_M[1]
    sigma_ford = sigma_M[2]
    
     # Finner (maks absolutt) bøyespenning per element for bruk i iterasjon
    sigma_max = np.maximum.reduce([
        np.abs(sigma_ender[:,0]),
        np.abs(sigma_ender[:,1]),
        np.abs(sigma_punkt),
        np.abs(sigma_ford)
    ])
    
    grupper = np.unique(elemgruppe[:, 1].astype(int))
    sigma_max_gruppe = np.zeros(grupper.size) #finner antall grupper 
    for i, gruppe_nr in enumerate(grupper):
        f = elemgruppe[:, 1].astype(int) == gruppe_nr #tar med de indekense (elementene) fra sigma_max som er i gruppen
        sigma_max_gruppe[i] = sigma_max[f].max()

    gruppe_id = elemgruppe[:, 1].astype(int)
    grupper = np.unique(gruppe_id)


    sigma_kritisk = (fy*sf)
    utnyttelse_gruppe = sigma_max_gruppe / sigma_kritisk


    
    #---- Skaleringfaktorer for lesbarhet -------
    s = 1e-3  # moment og skjærkraft, gir svar i KNm/KN
    bs = 1e-6 # bøyespenninger, gir svar i MPa
    f = 1e-6  # systemstivhetsmatrise, gir svar i MNm
    
    #Legger alle printlinjer samlet for ryddighet og kunne iterere main()
    # fmt() funk. formaterer array for lesbarhet
    
    if Printe:
        df = pd.DataFrame(K*f)  # Bruker pandas dataframe for å printe K matrise
        fmt = lambda x: "0" if np.isclose(x, 0.0, atol=1e-12) else f"{x:.2f}"
        print(df.to_string(formatters={c: fmt for c in df.columns}))
        
        print("\nSigma max per gruppe [Mpa]:", fmt_arr(sigma_max_gruppe*1e-6, "{:.3f}"))
        print("\nUtnyttelse per gruppe sigma_max/sigma_kritisk:", np.round(utnyttelse_gruppe, 3), "\n")
        print(f"\n Systemstivhetsmatrise K (*{f}:)")
        print(fmt_arr(K*f, "{:.2f}"))
        print(f"EI", fmt_arr(I_zmax*1e12,"{:.3e}"), EI)
        print("\nR: kNm", fmt_arr(R*s, "{:.6f}")) 
        print(f"\nRotasjon (grader)", fmt_arr(((180/np.pi)*rot), "{:.7f}")) #rot i grader
        print(f"\nEndemoment kNm: \n", fmt_arr(em*s, "{:.5f}"))
        print(f"Moment midt på bjelke pga av fordelt last kNm \n", fmt_arr(np.array(mb[0]*s), "{:.2e}"))
        print(f"Moment under punktlast N/m *{s}\n", fmt_arr(np.array(mb[1]*s), fmt="{:.4f}"))
        print(f"Skjærkraft [kN] \n", fmt_arr(np.array(Q*s), "{:.3f}"))
        print(f"\nSigma ender [Mpa] ", fmt_arr(sigma_M[0]*bs, "{:.3f}"))
        print(f"\nSigma pkt [Mpa] ",fmt_arr(sigma_M[1]*bs, "{:.3f}"))
        print(f"\nSigma  fordelt-last [Mpa] \n",fmt_arr(sigma_M[2]*bs, "{:.3f}"))
    
   
    
    return {
        "em": em,
        "mb": mb,
        "I_zmax": I_zmax,
        "sigma_max": sigma_max, 
        "sigma_max_gruppe": sigma_max_gruppe,  
        "EI": EI,
        "Q": Q,
        "rot": rot,
        "nelem": nelem,
        "MNPC": MNPC,
        "tvsnitt": tvsnitt,
        "geom": geom,      
        "lastdata": lastdata,
        "elemlen": elemlen,
        "elemgruppe": elemgruppe
    }

main(lesinput,Printe=True)