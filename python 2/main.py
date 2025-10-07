# Pakker
import numpy as np

# Funksjoner
from lesinput import lesinput
from lengder import lengder
from bøyestivhet import boyestivhet
from fastinnspenning import fastinnspenning
from Systemstivhetsmatrise import systemstivhetsmatrise
def main():

    # -----Leser inputdata
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata,  = lesinput()
    #print(lastdata)

    # -----Beregner elementlengder
    elemlen = lengder(punkt, MNPC)

    # -----Beregner bøyestivhet for alle elementer
    #EI = boyestivhet(tvsnitt, geom)
    
    R = fastinnspenning(npunkt, lastdata, MNPC, elemlen)

    K = systemstivhetsmatrise(MNPC, npunkt, tvsnitt, nelem, punkt)
    print(K)

    # ------Innfører grensebetingelser
    # Lag funksjonen selv basert på valgt metode for innføring av grensebetingelser
    # Kn, Rn = bc(punkt, K, R)

    # -----Løser ligningssystemet------
    # rot = np.linalg.solve(Kn, Rn)
    
    #------Beregner momentverdier for alle element ved endene, 
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