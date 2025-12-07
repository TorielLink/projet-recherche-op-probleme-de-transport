import time
from algorithms.northwest import northwest_solution


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
    # sol = balas_hammer(couts, P, C)   # TODO lorsque BH sera implémenté
    time.sleep(0.0001)  # à supprimer (évite un temps nul)
    return time.perf_counter() - start


# ---------------------------------------------------------------------
# Temps de marche-pied avec solution issue de Nord-Ouest
# tNO(n)
# ---------------------------------------------------------------------
def measure_time_marche_pied_from_NO(couts, P, C):
    start = time.perf_counter()
    # sol = northwest_solution(P, C)
    # marche_pied(sol, couts)           # TODO
    time.sleep(0.0001)  # à supprimer (évite un temps nul)
    return time.perf_counter() - start


# ---------------------------------------------------------------------
# Temps de marche-pied avec solution issue de Balas-Hammer
# tBH(n)
# ---------------------------------------------------------------------
def measure_time_marche_pied_from_BH(couts, P, C):
    start = time.perf_counter()
    # sol = balas_hammer(couts, P, C)   # TODO
    # marche_pied(sol, couts)           # TODO
    time.sleep(0.0001)  # à supprimer (évite un temps nul)
    return time.perf_counter() - start
