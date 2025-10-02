import numpy as np


def lesinput():

    # Åpner inputfilen
    fid = open("python 2/input.txt", "r")

    # Leser totalt antall punkt
            #  Leser kommentarlinje. Må leses fordi 'readline' leser 1 linje, linje for linje
    fid.readline() #Antall knutepunkt
    npunkt = int(fid.readline())
    
  
    # x- og y-koordinater til knutepunktene og grensebetingelse

    # Knutepunktnummer tilsvarer radnummer
    # x-koordinat lagres i kolonne 1, y-koordinat i kolonne 2
    # Grensebetingelse lagres i kolonne 3; 1 = fast innspent og 0 = fri rotasjon
    comlin = fid.readline()

    punkt = np.loadtxt(fid, dtype = int, max_rows = npunkt)     
																
    comlin = fid.readline() # Antall element
 
    nelem = int(fid.readline())

    comlin = fid.readline() #MNPC
    elem = np.loadtxt(fid, dtype = int, max_rows = nelem)

    # Elementkonnektivitet
    # Kolonne 1: Systemfrihetsgrad for elementfrihetsgrad 1
    # Kolonne 2: Systemfrihetsgrad for elementfrihetsgrad 2
    elemkonn = elem[0:nelem,0:2]

    # Tverrsnittsdata
    # Kolonne 1: E-modul
    # Kolonne 2: Tverrsnittstype, I-profil=1 og rørprofil=2
    tvsnitt = elem[0:nelem,2:4]

    # Leser antall laster som virker på rammen
    comlin = fid.readline()
 
    ngeom = int(fid.readline())

    # Leser geometridata for tverrsnittstypene
    comlin = fid.readline()

    geom = np.loadtxt(fid, dtype = float, max_rows = ngeom)
    

    # Leser antall laster som virker på rammen
    comlin = fid.readline()
    nlast = int(fid.readline())

    # Leser lastdata
    #lastdata = np.loadtxt(fid, dtype = float, max_rows = nlast)     # <-- Forslag til innlesing av lastdata

    # Lukker input-filen
    fid.close()

    return npunkt, punkt, nelem, elemkonn, tvsnitt

for n in range(5):
    print(lesinput()[n])