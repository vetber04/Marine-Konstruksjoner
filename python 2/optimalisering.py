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
from main import main


def scale_geom_type(geom, s, profiltype):
    g = geom.copy()
    if profiltype == 1:          # rør: [t, R_mid, 0, 0]
        g[0,0] *= s              # t
        g[0,1] *= s              # R_mid
    elif profiltype == 2:        # I-profil: [h, b, tf, tw]
        g[1,0] *= s              # h
        g[1,1] *= s              # b
        g[1,2] *= s              # tf
        g[1,3] *= s              # tw
    return g

def iterate_to_yield(lesinput, fy, safety=0.7, max_iter=8, tol=1e-3, alpha=1.0, verbose=True):
    # startgeometri fra input
    _, _, _, _, tvsnitt, geom0, _ = lesinput
    geom_cur = np.array(geom0, dtype=float)

    for it in range(1, max_iter+1):
        out = main(lesinput, geom_override=geom_cur, quiet=True)
        worst = out["worst_sigma"]                 # (nelem,)
        tv = out["tvsnitt"]                        # forventet rader [E, profiltype]
        limit = safety * fy
        util = worst / limit                       # utnyttelse per element

        # maks utnyttelse per profiltype (1 = rør, 2 = I)
        mask_ror = (tv[:,1].astype(int) == 1)
        mask_I   = (tv[:,1].astype(int) == 2)

        u_ror = float(util[mask_ror].max()) if mask_ror.any() else 0.0
        u_I   = float(util[mask_I].max())   if mask_I.any()   else 0.0

        if verbose:
            print(f"\nIterasjon {it}: utnyttelse rør={u_ror:.3f}, I={u_I:.3f}")

        changed = False
        if u_ror > 1.0 + tol:
            s = (u_ror ** (1.0/3.0)) ** alpha
            geom_cur = scale_geom_type(geom_cur, s, profiltype=1)
            changed = True
        if u_I > 1.0 + tol:
            s = (u_I ** (1.0/3.0)) ** alpha
            geom_cur = scale_geom_type(geom_cur, s, profiltype=2)
            changed = True

        if not changed:
            if verbose:
                print("✅ Begge profiltyper tilfredsstiller kravet (≤ 0.7·fy).")
            break

    # siste kjøring for rapport
    final = main(lesinput, geom_override=geom_cur, quiet=False)
    final["geom_optimized"] = geom_cur
    final["utilization"] = util
    return final

fy = 355e6  # Pa 
result = iterate_to_yield(lesinput, fy, safety=0.7, max_iter=8, alpha=1.0, verbose=True)
print(result)
print("\nOptimalisert geometri:")
print("Rør   [t, R_mid] :", result["geom_optimized"][0,:2])
print("I-pro [h,b,tf,tw]:", result["geom_optimized"][1,:4])