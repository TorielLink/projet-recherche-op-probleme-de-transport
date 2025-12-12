import time
import os
from contextlib import redirect_stdout

from algorithms.MarchePied import marche_pied
from algorithms.northwest import northwest_solution
from algorithms.BalasHammer import balas_hammer


# ---------------------------------------------------------------------
# Temps de l'algorithme Nord-Ouest
# θNO(n)
# ---------------------------------------------------------------------
def measure_time_nord_ouest(couts, P, C):
    start = time.perf_counter()
    northwest_solution(P, C)
    return time.perf_counter() - start


# ---------------------------------------------------------------------
# Temps de l'algorithme Balas-Hammer
# θBH(n)
# ---------------------------------------------------------------------
def measure_time_balas_hammer(couts, P, C):
    start = time.perf_counter()
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            balas_hammer(couts, P.copy(), C.copy())
    return time.perf_counter() - start


# ---------------------------------------------------------------------
# Temps de marche-pied avec solution issue de Nord-Ouest
# tNO(n)
# ---------------------------------------------------------------------
def measure_time_marche_pied_from_NO(couts, P, C):
    start = time.perf_counter()

    solution_initiale = northwest_solution(P.copy(), C.copy())
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            marche_pied(
                solution_initiale,
                couts,
                display=False
            )

    return time.perf_counter() - start


# ---------------------------------------------------------------------
# Temps de marche-pied avec solution issue de Balas-Hammer
# tBH(n)
# ---------------------------------------------------------------------
def measure_time_marche_pied_from_BH(couts, P, C):
    start = time.perf_counter()

    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            solution_initiale = balas_hammer(couts, P.copy(), C.copy())
            marche_pied(
                solution_initiale,
                couts,
                display=False
            )

    return time.perf_counter() - start
