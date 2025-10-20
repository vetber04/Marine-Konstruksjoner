import numpy as np


def lesinput():
    print("hei")
    # Åpner inputfilen
    fid = open("python 2/inputfiler/input.txt", "r") #Husk å endre bøyestivhet funk ved endring av inputfil
    #Antall knutepunkt
    fid.readline() 
    npunkt = int(fid.readline())
    
    # x- og y-koordinater til knutepunktene og grensebetingelse
    comlin = fid.readline() 
    punkt = np.loadtxt(fid, dtype = int, max_rows = npunkt)     

    #Antall element
    comlin = fid.readline() 
    nelem = int(fid.readline())

    #MNPC, E-modul, Profiltype
    comlin = fid.readline() 
    elem = np.loadtxt(fid, dtype = float, max_rows = nelem)

    # Elementkonnektivitet (MNPC)
    # Kolonne 1: Systemfrihetsgrad for elementfrihetsgrad 1
    # Kolonne 2: Systemfrihetsgrad for elementfrihetsgrad 2
    if nelem == 1:
        MNPC = np.array([[int(elem[0]), int(elem[1])]])
    else:
        MNPC = np.asarray(elem[:nelem, 0:2])           # tar kolonne 2 og 3 (slutten eksklusiv)
    # hvis de er float, men egentlig heltall:
    if np.allclose(MNPC, np.rint(MNPC)):
        MNPC = np.rint(MNPC).astype(np.intp)       # trygg konvertering til int-indekser
    else:
        raise ValueError("Utsnittet inneholder ikke-heltallige verdier.")
    # Tverrsnittsdata
    # Kolonne 1: E-modul
    # Kolonne 2: Tverrsnittstype, I-profil=1 og rørprofil=2
    if nelem == 1:
        tvsnitt = np.array([[elem[2], elem[3]]])
    else:
        tvsnitt = elem[0:nelem,2:4]

    #Antall laster 
    comlin = fid.readline()
    nlast = int(fid.readline())

     #Leser lastdata
    comlin = fid.readline()
    lastdata = np.loadtxt(fid, dtype = float, max_rows = nlast)     

    #Antall tversnitttyper
    comlin = fid.readline()
    ngeom = int(fid.readline())

    # Leser geometridata for tverrsnittstypene
    comlin = fid.readline()
    geom = np.loadtxt(fid, dtype = float, max_rows = ngeom)

    
   
    # Lukker input-filen
    fid.close()

    return npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata
