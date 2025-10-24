import numpy as np


def lesinput():
    #Leser .txt fil med readline() numpy funksjon, bruker comlin  til å hoppe over kommentarlinjer
    #loadtxt() lagrer ønsket linjer som array, trenger max_rows= fra inputfil for å lese riktig antall linjer
    
    # Åpner inputfilen
    fid = open("Kontruksjoner_prosjekt/inputfiler/input.txt", "r") 
    #Antall knutepunkt
    fid.readline() 
    npunkt = int(fid.readline())
    
    # x- og y-koordinater til knutepunktene og grensebetingelse
    comlin = fid.readline() 
    punkt = np.loadtxt(fid, dtype = int, max_rows = npunkt)     

    #Antall element
    comlin = fid.readline() #leser en kommentarlinje, men lagrer ikke verdi
    nelem = int(fid.readline())

    #leser inn data om elementer, indeks viser hvilken kollone de ligger i 
    # og deler de opp i to array
    # MNPC = [0, 1], E-modul = [2], Profiltype = [3], Elementgruppe = [4]
    comlin = fid.readline() 
    elem = np.loadtxt(fid, dtype = float, max_rows = nelem)

    # Elementkonnektivitet (MNPC)
    # [0]: Systemfrihetsgrad for elementfrihetsgrad 1
    # [1]: Systemfrihetsgrad for elementfrihetsgrad 2
    MNPC = np.asarray(elem[:nelem, 0:2])     
    MNPC = MNPC.astype(int) #gjør om til int    

    # Tverrsnittsdata
    # [0]: E-modul
    # 
    tvsnitt = elem[0:nelem,2:4]

    #Elementgruppe og profiltype for iterasjon
    # kollone [0]: Tverrsnittstype, I-profil=1 og rørprofil=2
    # kollone [1]: Elementgruppe 1,1,2,2.. for eks 
    elemgruppe = elem[0:nelem,3:5]


    #Antall laster 
    comlin = fid.readline()
    nlast = int(fid.readline())

    # Leser lastdata
    # Forklaring på kollonene i lastdata:
    # [0] typelast punkt=1 fordelt=2 moment = 3 
    # [1] elementnr for last (ikke moment i kp) 
    # [2] Avtand fra venstre punktlast (alfa)[-], q1 [N/m] ved knutepunkt A, Momentverdi M [Nm] med klokka +
    # [3] q2 [N/m] ved knutepunkt B
    # [4] Knutepunkt til moment (kp_M)
    comlin = fid.readline()
    lastdata = np.loadtxt(fid, dtype = float, max_rows = nlast)     

    #Antall tversnitttyper
    comlin = fid.readline()
    ngeom = int(fid.readline())

    # Leser geometridata for tverrsnittstypene
    #rør profiltype 1 eller I profil profiltype 2
    #Tynvegget rør: [0] tykkelse, [1] midlere radius
    #I profil: [0] total høyde, [1] bredde flens, [2] tykkelse steg, [3] tykkelse flens
    comlin = fid.readline()
    geom = np.loadtxt(fid, dtype = float, max_rows = ngeom)

    # Lukker input-filen
    fid.close()

    return npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata, elemgruppe
