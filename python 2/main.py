# Pakker
import numpy as np
import pandas as pd
# Funksjoner
from lesinput import lesinput
from lengder import lengder
from bøyestivhet import boyestivhet
from fastinnspenning import fastinnspenning
from endemoment import endemoment
from momenterbjelke import momenterbjelke
from Systemstivhetsmatrise import systemstivhetsmatrise
from shear import Q_superpos
from bøyespenning import M_spenning
from printefunk import fmt_arr
lesinput = lesinput()
def main(lesinput, geom_override=None, Printe=False):
    # ---printefunksjon ---
    
    #---- faktorer for skalering -------------
    k_diagonal = 1e6
    s = 1
    f = 1e-6 #faktor til systemstivhetsmatrise
    bs = 1e-6
    # ----- Leser inputdata -------
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata,  = lesinput
    if geom_override is not None:
        geom = np.array(geom_override, dtype=float)   #endrer viss i løkke
    elemlen =  lengder(punkt, MNPC) #[m]
    # Beregner bøyestivhet for alle elementer
    EI = boyestivhet(tvsnitt, geom)[0]
    I_zmax = boyestivhet(tvsnitt, geom)[1]
    # -----Setter opp R vektor------------------------
    R = fastinnspenning(npunkt, lastdata, MNPC, elemlen)
    # -----Setter opp systemstivhetsmatrise K og modifiserer R for faste knutepunkter
    K, R = systemstivhetsmatrise(MNPC, npunkt, tvsnitt, nelem, punkt, elemlen, EI, R, k_diagonal)
    # -----Løser ligningssystemet------
    rot = np.linalg.solve(K, R)
    #------Beregner momentverdier for alle element ved endene, 
    em =endemoment(MNPC, rot, EI, elemlen, nelem, R, lastdata)
    #------Beregner momentverdier for alle element ved midtpunkt for fordelt last,
    #------og under punktlast, vha. superposisjonsprinsippet
    mb =  momenterbjelke(lastdata, nelem, elemlen, em)
    #------Beregner skjærkraftverdier for alle element ved enden
    Q = Q_superpos(lastdata, em, elemlen)
    #----Bøyespenning-----
    sigma_M =  M_spenning(em, mb[1], mb[0], I_zmax) 
    sigma_ender = sigma_M[0]
    sigma_punkt = sigma_M[1]
    sigma_ford = sigma_M[2]
    if Printe:
        df = pd.DataFrame(K*f)  # Skalerer for bedre lesbarhet
        fmt = lambda x: "0" if np.isclose(x, 0.0, atol=1e-12) else f"{x:.2f}"
        print(EI)
        print(df.to_string(formatters={c: fmt for c in df.columns}))
        print("\nR: KNm", fmt_arr(R*s, fmt="{:.6f}")) #R i kN
        print(f"\n Systemstivhetsmatrise K (*{f}:)")
        print(f"\nRotasjon (grader){(180/np.pi)}", fmt_arr(((180/np.pi)*rot), fmt="{:.7f}")) #rot i mrad
        print(f"\nEndemoment Nm: *{s}\n", fmt_arr(em*s, fmt="{:.5f}")) #em i Nm
        print(f"Moment midt på bjelke pga av fordelt last Nmm (*{1000})\n", fmt_arr(np.array(mb[0]*1000), fmt="{:.2e}"))
        print(f"Moment under punktlast N/m *{s}\n", fmt_arr(np.array(mb[1]*s), fmt="{:.4f}"))
        print(f"Skjærkraft [KN] *{s}\n", fmt_arr(np.array(Q*s), fmt="{:.2f}"))
        print(f"\nSigma ender [Mpa]  (*{bs})", fmt_arr(sigma_M[0]*bs, fmt="{:.3f}"))
        print(f"\nSigma pkt [Mpa]  (*{bs})",fmt_arr(sigma_M[1]*bs, fmt="{:.3f}"))
        print(f"\nSigma  fordelt-last [Mpa]  (*{bs})\n",fmt_arr(sigma_M[2]*bs, fmt="{:.3f}"))
    # Finn "verste" (maks absolutt) spenning per element
    worst = np.maximum.reduce([
        np.abs(sigma_ender[:,0]),
        np.abs(sigma_ender[:,1]),
        np.abs(sigma_punkt),
        np.abs(sigma_ford)
    ])

    return {
        "em": em,
        "mb": mb,
        "I_zmax": I_zmax,
        "worst_sigma": worst,   # (nelem,)
        "EI": EI,
        "Q": Q,
        "rot": rot,
        "nelem": nelem,
        "MNPC": MNPC,
        "tvsnitt": tvsnitt,
        "geom": geom,           # faktisk brukt geometri
        "lastdata": lastdata,
        "elemlen": elemlen,

    }

main(lesinput,Printe=True)