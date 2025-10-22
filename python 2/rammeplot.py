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

# --------- Hjelpere for å hente lastdata -> q1,q2, alpha, P ----------
def bygg_q_pairs(lastdata, nelem):
    q = np.full((nelem, 2), np.nan, dtype=float)
    for rec in lastdata:
        tl = int(rec[0])
        if tl == 2:  # trapes
            _, e, q1, q2, _ = rec
            q[int(e), 0] = float(q1)
            q[int(e), 1] = float(q2)
    return q

def bygg_alpha_P(lastdata, nelem):
    alpha = np.full(nelem, np.nan, dtype=float)
    P     = np.full(nelem, np.nan, dtype=float)
    for rec in lastdata:
        tl = int(rec[0])
        if tl == 1:  # punktlast
            _, e, a, p, _ = rec
            alpha[int(e)] = float(a)
            P[int(e)]     = float(p)
    return alpha, P

# --------- Momentbidrag i lokal akse (hogg > 0) ----------
def m_end_line(x, L, M1, M2):
    return M1 + (M2 - M1) * (x / L)

def m_trap_line_hogg(x, L, q1, q2):
    if np.isnan(q1) or np.isnan(q2):
        return np.zeros_like(x)
    k    = (q2 - q1) / L
    W    = (q1 + q2) * L / 2.0
    xbar = L * (q1 + 2*q2) / (3.0 * (q1 + q2))
    RA   = W * (L - xbar) / L  # sagging-konvensjon
    M_sag = RA * x - 0.5 * q1 * x**2 - (1.0/6.0) * k * x**3
    return -M_sag  # hogg > 0

def m_point_line_hogg(x, L, alpha, P):
    if np.isnan(alpha) or np.isnan(P):
        return np.zeros_like(x)
    a  = alpha * L
    RA = P * (L - a) / L
    M_sag = np.where(x < a, RA * x, RA * x - P * (x - a))
    return -M_sag  # hogg > 0

# --------- Tegn M-diagram langs medlem i globalt plan ----------
def plot_member_M_band(ax, n1, n2, L, M1, M2, q1, q2, alpha, P, scale=1/50000, n=201, fylle=True):
    """
    Tegner M-bånd langs elementet. Hvis fylle=True, fylles arealet mellom
    senterlinja og M-båndet (hogg>0).
    """
    # --- moment langs lokal akse ---
    xloc = np.linspace(0.0, L, n)

    Mend  = m_end_line(xloc, L, M1, M2)
    Mtrap = m_trap_line_hogg(xloc, L, q1, q2)
    Mpnt  = m_point_line_hogg(xloc, L, alpha, P)
    Mtot  = Mend + Mtrap + Mpnt  # [N·m]

    # --- global geometri ---
    x1, y1 = n1; x2, y2 = n2
    dx, dy = (x2 - x1), (y2 - y1)
    Lgeom = (dx**2 + dy**2) ** 0.5
    if Lgeom == 0:
        return
    # tangentretn. og normal (venstre normal)
    tx, ty = dx / Lgeom, dy / Lgeom
    nx, ny = -ty, tx

    # posisjon langs staven
    s  = xloc / L
    Xc = x1 + s * dx
    Yc = y1 + s * dy

    # forskyvning i normalretning
    off = scale * Mtot
    Xb  = Xc + nx * off
    Yb  = Yc + ny * off

    # tegn senterlinje
    ax.plot([x1, x2], [y1, y2], linewidth=1)

    # tegn båndet (linje)
    ax.plot(Xb, Yb, linewidth=1.5)

    if fylle:
        # Fyll polygon mellom bjelkelinje (senterlinje) og M-bånd (Xb,Yb)
        Xpoly = np.concatenate([Xc, Xb[::-1]])
        Ypoly = np.concatenate([Yc, Yb[::-1]])
        ax.fill(Xpoly, Ypoly, alpha=0.3)  # transparent fyll

    # marker midtverdi (valgfritt)
    midtverdi = False
    if midtverdi:
        xm = L * 0.5
        Mm = (m_end_line(xm, L, M1, M2)
            + m_trap_line_hogg(xm, L, q1, q2)
            + m_point_line_hogg(xm, L, alpha, P))
        Xm = x1 + 0.5 * dx + nx * (scale * Mm)
        Ym = y1 + 0.5 * dy + ny * (scale * Mm)
        ax.annotate(f"{Mm:.0f} N·m", (Xm, Ym),
                    textcoords="offset points", xytext=(0, -10), ha="center", fontsize=9)

def plot_rammediagram():
    # Kjør analysen (bruker din main)
    res = main(lesinput, Printe=False)

    # Pakk ut fra lesinput (her ligger punktene!)
    npunkt, punkt, nelem_in, MNPC_in, tvsnitt, geom, lastdata = lesinput

    # Hent det vi trenger fra res
    elemlen = np.asarray(res["elemlen"], float)      # (nelem,)
    M_ende  = np.asarray(res["em"], float)           # (nelem,2)
    MNPC    = np.asarray(res["MNPC"], int) if "MNPC" in res else np.asarray(MNPC_in, int)
    nelem   = int(res["nelem"])

    punkt = np.asarray(punkt, float)                 # (n_nodes, 2) forventet
    if punkt.ndim != 2 or punkt.shape[1] < 2:
        raise ValueError(f"'punkt' må være (n,2) med x,y. Fikk shape {punkt.shape}")

    # Bygg laster pr. element
    q_pairs  = bygg_q_pairs(lastdata, nelem)         # (nelem,2)
    alpha, P = bygg_alpha_P(lastdata, nelem)         # (nelem,), (nelem,)

    # Oppdag 0- vs. 1-indeksert MNPC
    max_idx = int(MNPC.max())
    n_nodes = punkt.shape[0]
    if max_idx <= n_nodes - 1:
        shift = 0   # 0-basert
    elif max_idx <= n_nodes:
        shift = 1   # 1-basert
    else:
        raise IndexError(
            f"MNPC refererer node {max_idx} men 'punkt' har kun {n_nodes} noder.\n"
            "Sjekk at du bruker riktige 'punkt' og at MNPC matcher (0/1-basert)."
        )

    # Sikkerhet: sjekk alle indekser før plotting
    bad = []
    for e in range(nelem):
        i_raw, j_raw = int(MNPC[e,0]), int(MNPC[e,1])
        i, j = i_raw - shift, j_raw - shift
        if not (0 <= i < n_nodes and 0 <= j < n_nodes):
            bad.append((e, i_raw, j_raw, i, j))
    if bad:
        lines = "\n".join(f"  e={e}: MNPC=({ir},{jr}) -> ({i},{j}) out of [0,{n_nodes-1}]"
                          for (e, ir, jr, i, j) in bad)
        raise IndexError("Ugyldige element-indekser funnet:\n" + lines)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    for e in range(nelem):
        i = int(MNPC[e,0]) - shift
        j = int(MNPC[e,1]) - shift
        n1 = (punkt[i,0], punkt[i,1])
        n2 = (punkt[j,0], punkt[j,1])

        L      = float(elemlen[e])
        M1, M2 = M_ende[e]
        q1, q2 = q_pairs[e]
        a, p   = alpha[e], P[e]

        # Skaleringsfaktor for båndets tykkelse (m per N·m) – justér etter behov
        plot_member_M_band(ax, n1, n2, L, M1, M2, q1, q2, a, p,
                           scale=1/50000, n=201)

    ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, linestyle=':')
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("M-diagram")
    plt.tight_layout()
    plt.show()

# Kjør
plot_rammediagram()


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
def plot_member_V_band(ax, n1, n2, L, V1, V2, alpha=np.nan, scale=1/2e4, n=201, fylle=True):
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

    # ---- Auto-skalering av båndtykkelse ----
    # Finn maks |V| i alle ender (enkel og robust målestokk)
    Vmax = float(np.max(np.abs(V_ende))) if V_ende.size else 1.0
    minL = float(np.min(elemlen)) if elemlen.size else 1.0
    target_offset = 0.05 * minL     # ~5% av korteste elementlengde
    scale = target_offset / (Vmax if Vmax > 0 else 1.0)
    print(f"[shear auto-scale] Vmax={Vmax:.2f} N, minL={minL:.3f} m -> scale={scale:.6g} m/N")

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
                           scale=scale, n=201, fylle=True)

    ax.set_aspect('equal', adjustable='datalim')
    ax.grid(True, linestyle=':')
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_title("Skjærkraft-diagram langs rammen (CCW positiv)")
    plt.tight_layout()
    plt.show()

# ---- Kjør plot ----
plot_rammediagram_shear()
