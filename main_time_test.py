import multiprocessing
import os
import psutil

from utils.benchmark.timing import (
    measure_time_nord_ouest,
    measure_time_balas_hammer,
    measure_time_marche_pied_from_NO,
    measure_time_marche_pied_from_BH,
)
from utils.generation.ramdom_problem import generate_random_transport_problem


def benchmark(n_values):
    """
    Lance un benchmark des algorithmes de transport
    pour différentes tailles de problèmes.

    Principe :
        - Génère un problème aléatoire de taille n
        - Mesure le temps d’exécution de chaque algorithme
        - Affiche les résultats pour comparaison

    Args:
        n_values: liste des tailles n à tester
    """

    print("\n=== Benchmark des algorithmes ===\n")

    for n in n_values:
        print(f"--- Taille n = {n} ---")

        couts, P, C = generate_random_transport_problem(n)

        # θNO(n)
        t_no = measure_time_nord_ouest(couts, P, C)
        print(f"θNO(n)  : {t_no:.6f} s")

        # θBH(n)
        t_bh = measure_time_balas_hammer(couts, P, C)
        print(f"θBH(n)  : {t_bh:.6f} s")

        # tNO(n)
        t_mp_no = measure_time_marche_pied_from_NO(couts, P, C)
        print(f"tNO(n)  : {t_mp_no:.6f} s")

        # tBH(n)
        t_mp_bh = measure_time_marche_pied_from_BH(couts, P, C)
        print(f"tBH(n)  : {t_mp_bh:.6f} s")

        print()


if __name__ == "__main__":
    """
    Point d’entrée du script de benchmark.

    Principe :
         - Force l’exécution sur un seul cœur CPU
         - Lance les benchmarks
         - Rétablit l’affinité CPU à la fin
    """

    # Limite l'exécution à un seul cœur CPU
    p = psutil.Process(os.getpid())
    p.cpu_affinity([0])
    benchmark([3, 5, 8, 10])
    p.cpu_affinity(list(range(multiprocessing.cpu_count())))
