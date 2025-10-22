import numpy as np
import matplotlib.pyplot as plt

# ================== IMPORTS OG INN-LASINGER ==================
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
from main import main
import math


# NB: lesinput() i din kode returnerer en *tuple* med data.
lesinput = lesinput()

# ================== HENT VERDIER FRA main OG PLOTT ==================
import numpy as np
import matplotlib.pyplot as plt
import math



import numpy as np
import matplotlib.pyplot as plt

# ---------- Hent alpha (posisjon for punktlast) fra lastdata ----------
def bygg_alpha(lastdata, nelem):
    """
    Returnerer 1D-array alpha i [0..1] for EN punktlast per element.
    np.nan hvis ingen punktlast registrert for elementet.
    Forventet lastdata: rader med tl==1: (tl, e, alpha, P, M_kp)
    """
    alpha = np.full(nelem, np.nan, dtype=float)
    for rec in lastdata:
        tl = int(rec[0])
        if tl == 1:
            _, e, a, _, _ = rec
            alpha[int(e)] = float(a)
    return alpha

# ---------- Skjær langs element (bruker ENKEL lineær interpolasjon) ----------
def v_line(x, L, V1, V2):
    """
    Skjærkraft V(x) langs elementet fra endeverdier.
    Enkel lineær interpolasjon mellom V1 (venstre) og V2 (høyre).
    (Endeverdiene antas allerede å inkludere effekten av alle laster.)
    Enheter: V i N, L i m, x i m.
    """
    return V1 + (V2 - V1)*(x/L)

# ---------- Tegn fylt skjær-bånd langs ett element ----------
def plot_member_V_band(ax, n1, n2, L, V1, V2, alpha=np.nan, scale=1/2, n=201, fylle=True):
    """
    Fyller arealet mellom stavens senterlinje og forskjøvet V-kurve.
    Sign: mot klokka (CCW) = positiv skjær -> offset på "venstre" side av lokal akse.
    """
    # Diskretisering i lokal x
    xloc = np.linspace(0.0, L, n)
    Vx   = v_line(xloc, L, V1, V2)  # N

    # Global geometri
    x1, y1 = n1; x2, y2 = n2
    dx, dy = (x2 - x1), (y2 - y1)
    Lgeom  = np.hypot(dx, dy)
    if Lgeom == 0:
        return
    # tangent og venstre normal
    tx, ty = dx / Lgeom, dy / Lgeom
    nx, ny = -ty, tx

    # Senterlinje langs staven
    s  = xloc / L
    Xc = x1 + s * dx
    Yc = y1 + s * dy

    # Offset i normalretning proporsjonal med V (N * m_per_N = m)
    off = scale * Vx
    Xb  = Xc + nx * off
    Yb  = Yc + ny * off

    # Senterlinje
    ax.plot([x1, x2], [y1, y2], color="#888888", linewidth=1)

    # Bånd-kurve
    ax.plot(Xb, Yb, linewidth=1.5)

    # Fyll areal
    if fylle:
        Xpoly = np.concatenate([Xc, Xb[::-1]])
        Ypoly = np.concatenate([Yc, Yb[::-1]])
        ax.fill(Xpoly, Ypoly, alpha=0.3)

    # Marker punktlastposisjon (kun visuelt, ingen verdier)
    if not np.isnan(alpha):
        xp = alpha * L
        # global posisjon på senterlinja ved alpha
        Xp = x1 + (xp/L) * dx
        Yp = y1 + (xp/L) * dy
        # liten "tverrstrek" for markering
        tick = 0.01 * Lgeom  # lengde på markør ~1% av elementlengde
        ax.plot([Xp - nx*tick, Xp + nx*tick], [Yp - ny*tick, Yp + ny*tick], linewidth=1)

# ---------- Hovedplot: skjærkraft for hele ramme ----------
def plot_rammediagram_shear():
    # Kjør analysen din
    res = main(lesinput, Printe=False)

    # Pakk ut nødvendig info
    try:
        elemlen  = np.asarray(res["elemlen"], float)    # (nelem,)
        V_ende   = np.asarray(res["Q"], float)          # (nelem,2) ende-skjær (N)
        MNPC     = np.asarray(res["MNPC"], int)
        nelem    = int(res["nelem"])
        # Punkt-koordinater (x,y) hentes trygt fra lesinput (der ligger noder)
        npunkt, punkt, _, MNPC_in, _, _, lastdata = lesinput
    except KeyError:
        # Fallback om noen nøkler ikke ligger i res
        npunkt, punkt, nelem, MNPC_in, tvsnitt, geom, lastdata = lesinput
        elemlen = np.asarray(lengder(punkt, MNPC_in), float)
        V_ende  = np.asarray(res["Q"], float)           # (nelem,2)
        MNPC    = np.asarray(MNPC_in, int)

    punkt = np.asarray(punkt, float)

    # Hent alpha for markør (om finnes)
    alpha = bygg_alpha(lastdata, nelem)

    # Oppdag 0- vs 1-indekserte MNPC
    n_nodes = punkt.shape[0]
    max_idx = int(MNPC.max())
    shift = 0 if max_idx <= n_nodes-1 else 1
    if max_idx > n_nodes:
        raise IndexError(f"MNPC refererer node {max_idx}, men det finnes bare {n_nodes} noder.")

   
    # ---- Plot ----
    fig, ax = plt.subplots(figsize=(10, 6))
    for e in range(nelem):
        i = int(MNPC[e,0]) - shift
        j = int(MNPC[e,1]) - shift
        if not (0 <= i < n_nodes and 0 <= j < n_nodes):
            continue  # hopp usikre elementer

        n1 = (punkt[i,0], punkt[i,1])
        n2 = (punkt[j,0], punkt[j,1])

        L   = float(elemlen[e])
        V1, V2 = V_ende[e]              # N (mot klokka positiv)
        a    = alpha[e]                 # posisjon for punktlast (kun markør)

        plot_member_V_band(ax, n1, n2, L, V1, V2, alpha=a,
                           scale=1/15000, n=201, fylle=True)

    ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, linestyle=':')
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Skjærkraft-diagram langs rammen u/ punktlast på topp")
    plt.tight_layout()
    plt.show()

# ---- Kjør plot ----
plot_rammediagram_shear()
