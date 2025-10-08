# Pakker
import numpy as np
import pandas as pd
# Funksjoner
from lesinput import lesinput
from lengder import lengder
from bøyestivhet import boyestivhet
from fastinnspenning import fastinnspenning
from endemoment import endemoment
#from Systemstivhetsmatrise import systemstivhetsmatrise
from Systemstivhetsmatriseøving8 import systemstivhetsmatrise8
def main():

    # -----Leser inputdata
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata,  = lesinput()
    print(lastdata)

    # -----Beregner elementlengder
    elemlen =  lengder(punkt, MNPC) # ? mm slik at det går opp med EI N/mm^2 MPa

    # -----Beregner bøyestivhet for alle elementer
    #EI = boyestivhet(tvsnitt, geom)
    
    R = fastinnspenning(npunkt, lastdata, MNPC, elemlen)
    #print(EI)
    #print(elemlen)
    #print(R)


    K = systemstivhetsmatrise8(MNPC, npunkt, tvsnitt, punkt)

    #printer K matrise i pandas, lettere å lese
    df = pd.DataFrame(K)
    fmt = lambda x: "0" if np.isclose(x, 0.0, atol=1e-12) else f"{x:.2f}"
    print(df.to_string(formatters={c: fmt for c in df.columns}))


 
    # -----Løser ligningssystemet------
    rot = np.linalg.solve(K, R)
    print(rot)

    #------Beregner momentverdier for alle element ved endene, 
    #em = endemoment(MNPC, rot, tvsnitt, lengder, nelem)
    #print(em*1e4)
    
    #------og ved midtpunkt for fordelt last og under punktlaster
    #------vha. superposisjonsprinsippet
    # Lag funksjonen selv
    # Mval = moment(nlast, last, MNPC, elemlen, rot, tvsnitt, EI, ...

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