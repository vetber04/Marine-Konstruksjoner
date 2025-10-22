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

# ---- helpers for å hente q1,q2 og punktlast fra lastdata ----
def bygg_q_pairs(lastdata, nelem):
    """(nelem,2) med [q1,q2] i N/m; np.nan hvis ikke trapeslast (tl!=2)."""
    q = np.full((nelem, 2), np.nan, dtype=float)
    for rec in lastdata:
        tl = int(rec[0])
        if tl == 2:
            _, e, q1, q2, _ = rec
            q[int(e)] = (float(q1), float(q2))
    return q

def bygg_alpha_P(lastdata, nelem):
    """1D alpha i [0..1] og 1D P i N; np.nan hvis ikke punktlast (tl!=1)."""
    alpha = np.full(nelem, np.nan, dtype=float)
    P     = np.full(nelem, np.nan, dtype=float)
    for rec in lastdata:
        tl = int(rec[0])
        if tl == 1:
            _, e, a, p, _ = rec
            alpha[int(e)] = float(a)
            P[int(e)]     = float(p)
    return alpha, P

# ---- momentbidrag (hogg > 0) ----
def _m_end_line(x, L, M1, M2):
    return M1 + (M2 - M1) * (x / L)

def _m_trap_line_hogg(x, L, q1, q2):
    if np.isnan(q1) or np.isnan(q2):
        return np.zeros_like(x)
    k    = (q2 - q1) / L
    W    = (q1 + q2) * L / 2.0
    xbar = L * (q1 + 2*q2) / (3.0 * (q1 + q2))
    RA   = W * (L - xbar) / L  # sagging-konvensjon
    M_sag = RA * x - 0.5 * q1 * x**2 - (1.0/6.0) * k * x**3
    return -M_sag  # hogg > 0

def _m_point_line_hogg(x, L, alpha, P):
    if np.isnan(alpha) or np.isnan(P):
        return np.zeros_like(x)
    a  = alpha * L
    RA = P * (L - a) / L
    M_sag = np.where(x < a, RA*x, RA*x - P*(x - a))
    return -M_sag  # hogg > 0

# ---- ett element: kun total-kurve, annoter verdier, ingen legend ----
def plot_element_M_clean(
    L, M1, M2,
    q1=np.nan, q2=np.nan,
    alpha=np.nan, P=np.nan,
    n=401, title=None, ax=None
):
    if ax is None:
        fig, ax = plt.subplots(figsize=(3, 1.8))

    x = np.linspace(0.0, L, n)
    Mend  = _m_end_line(x, L, M1, M2)
    Mtrap = _m_trap_line_hogg(x, L, q1, q2)
    Mpnt  = _m_point_line_hogg(x, L, alpha, P)
    Mtot  = Mend + Mtrap + Mpnt

    ax.plot(x, Mtot)                 # bare total-kurven
    ax.axhline(0.0, linewidth=2, color='black')     # nullinje / bjelkelinje

    # skriv midtverdien (samme “motor” som kurven)
    xm = 0.5 * L
    

    # hvis punktlast finnes: skriv verdien under punktet
    if not (np.isnan(alpha) or np.isnan(P)):
        xp = alpha * L
        Mp = (
            _m_end_line(xp, L, M1, M2)
            + _m_trap_line_hogg(xp, L, q1, q2)
            + _m_point_line_hogg(xp, L, alpha, P)
        )
        ax.annotate(f"{Mp:.2e} Nm", xy=(0, 10))

    ax.set_xlabel("[m]")
    ax.set_ylabel("[Nm]")
    ax.set_title(title or "M-diagram", loc='left')
    ax.grid(True)

# ---- grid for flere elementer (subplot), ingen legend, plt.show() én gang ----
def plot_elementer_grid_clean(
    lengder,           # 1D [m]
    M_ende,            # (nelem,2) [N·m], hogg>0
    q_pairs,           # (nelem,2) [N/m] (np.nan hvis ikke trapes)
    alpha=None,        # (nelem,) [0..1] eller np.nan
    P=None,            # (nelem,) [N] eller np.nan
    titles=None,
    n=401, cols=2
):
    nelem = len(lengder)
    if alpha is None: alpha = np.full(nelem, np.nan)
    if P     is None: P     = np.full(nelem, np.nan)

    rows = (nelem + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 4.5*rows))
    axes = np.atleast_1d(axes).ravel()

    for e in range(nelem):
        ax = axes[e]
        L  = float(lengder[e])
        M1, M2 = M_ende[e]
        q1, q2 = q_pairs[e]
        ttl = titles[e] if titles and e < len(titles) else f"Element {e}"

        plot_element_M_clean(
            L=L, M1=M1, M2=M2,
            q1=q1, q2=q2,
            alpha=alpha[e], P=P[e],
            n=n, title=ttl, ax=ax
        )

    for j in range(nelem, len(axes)):
        axes[j].axis("off")

    fig.tight_layout()
    plt.show()

# ================== HENT FRA main OG PLOTT ==================
# Kjør analysen din
res = main(lesinput, Printe=True)

# Prøv å hente direkte fra retur (slik vi gjorde sist)
try:
    L         = res["elemlen"]            # 1D [m]
    M_ende    = res["em"]                 # (nelem,2) [N·m]
    mid_trap  = res["mb"][0]              # 1D (ikke brukt her, vi annoterer nøkler direkte)
    under_P   = res["mb"][1]              # 1D (ikke brukt her)
    lastdata  = res["lastdata"]
    nelem     = res["nelem"]
except KeyError:
    # Fallback hvis main() ikke returnerer elemlen/lastdata
    npunkt, punkt, nelem, MNPC, tvsnitt, geom, lastdata = lesinput
    L = lengder(punkt, MNPC)
    M_ende = res["em"]

# Bygg q, alpha, P fra lastdata
q_pairs = bygg_q_pairs(lastdata, nelem)    # (nelem,2)
alpha, P = bygg_alpha_P(lastdata, nelem)   # (nelem,), (nelem,)

# Plott alle elementer i et ryddig grid
plot_elementer_grid_clean(
    lengder=L,
    M_ende=M_ende,
    q_pairs=q_pairs,
    alpha=alpha,
    P=P,
    titles=[f"{i}" for i in range(nelem)],
    cols=3  # endre til 3 om du vil ha 3 per rad
)