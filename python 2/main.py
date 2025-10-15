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
#from Systemstivhetsmatriseøving8 import systemstivhetsmatrise8
def main():
    # ---printefunksjon ---
    def fmt_arr(a, fmt="{:.2e}"):
        a = np.asarray(a, dtype=float)
        if a.ndim == 1:
            return "[" + ", ".join(fmt.format(x) for x in a) + "]"
        elif a.ndim == 2:
            rows = ["[" + ", ".join(fmt.format(x) for x in row) + "]" for row in a]
            return "[\n  " + ",\n  ".join(rows) + "\n]"
        else:
            return np.array2string(a)


    # -----Leser inputdata
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata,  = lesinput()
    print(lengder)
    # ------Beregner elementlengder----
    elemlen =  lengder(punkt, MNPC) #[m]
    # Beregner bøyestivhet for alle elementer
    EI = boyestivhet(tvsnitt, geom)
    print(" I (i mm^4):", (EI/tvsnitt[:, 0])*1e12) #EI i MNm2
    # -----Setter opp R vektor------------------------
    R = fastinnspenning(npunkt, lastdata, MNPC, elemlen)
    
    # -----Setter opp systemstivhetsmatrise K og modifiserer R for faste knutepunkter
    K, R = systemstivhetsmatrise(MNPC, npunkt, tvsnitt, nelem, punkt, elemlen, EI, R)
    print("R: kNm", fmt_arr(R, fmt="{:.2f}")) #R i kN
    
    #-----printer K matrise i pandas, lettere å lese-----------------------
    print("Systemstivhetsmatrise K (i MN/m):")
    df = pd.DataFrame(K*1e-6)  # Skalerer for bedre lesbarhet
    fmt = lambda x: "0" if np.isclose(x, 0.0, atol=1e-12) else f"{x:.2f}"
    print(df.to_string(formatters={c: fmt for c in df.columns}))

    # -----Løser ligningssystemet------
    rot = np.linalg.solve(K, R)
    print("rotasjon * 1e-3 \n", fmt_arr((rot*1e3), fmt="{:.2f}")) #rot i mrad

    #------Beregner momentverdier for alle element ved endene, 
    em = endemoment(MNPC, rot, EI, elemlen, nelem, R, lastdata)
    print("Endemoment kNm:\n", fmt_arr(em, fmt="{:.4f}")) #em i kNm
    
    #------Beregner momentverdier for alle element ved midtpunkt for fordelt last,
    #------og under punktlast, vha. superposisjonsprinsippet
    mb = momenterbjelke(lastdata, nelem, elemlen, em)
    print("Moment midt på bjelke pga av fordelt last kN/m \n", fmt_arr(np.array(mb[0]*1e-3), fmt="{:.2f}"))
    print("Moment under punktlast kN/m\n", fmt_arr(np.array(mb[1]*1e-3), fmt="{:.2f}"))
   

    #------Beregner skjærkraftverdier for alle element ved endene

    #------vha. enkel derivasjon (Q=dM/ds) for Q-bidrag fra moment pga.
    #------bjelkeenderotasjoner, og bruker superposisjonsprinsippet
    #------for å addere til Q-bidrag fra ytre last
    # Lag funksjonen selv
    # Qval = shear(nlast, last, MNPC, elemlen, rot, tvsnitt, ...

    #------Beregner bøyespenning for alle element ved endene, 
    #------og ved midtpunkt for fordelt last og under punktlaster
    # Lag funksjonen selv
    # sigma_M = boyespenn(Mval, tvsnitt, ...

    #-----Printer bøyespenninger for alle elementene
    # print("Bøyespenninger:")
    # print(sigma_M)

    #-----Printer momentverdier for alle elementer
    # print("Momentverdier for tegning av M-diagram (for hånd):")
    # print(Mval)

    #-----Printer skjærkraftverdier ved endene for alle elementer
    # print("Skjærkraftverdier for tegning av Q-diagram (for hånd):")
    # print(Qval)

main()