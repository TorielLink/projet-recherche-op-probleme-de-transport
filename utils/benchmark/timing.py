import os
import time
from contextlib import redirect_stdout

from algorithms.balas_hammer import compute_balas_hammer_solution
from algorithms.northwest_corner import compute_northwest_solution
from algorithms.stepping_stone import solve_stepping_stone


def measure_time_nord_ouest(couts, P, C):
    """
    Mesure le temps d’exécution de la méthode du Nord-Ouest.

    Principe :
        - Calcule une solution initiale avec Nord-Ouest
        - Mesure le temps écoulé

    Args:
        couts: matrice des coûts (non utilisée ici)
        P: provisions des fournisseurs
        C: commandes des clients

    Retour :
        durée d’exécution en secondes
    """
    start = time.perf_counter()
    compute_northwest_solution(P, C)
    return time.perf_counter() - start


def measure_time_balas_hammer(couts, P, C):
    """
    Mesure le temps d’exécution de l’algorithme de Balas-Hammer.

    Principe :
        - Exécute Balas-Hammer
        - Redirige les affichages vers /dev/null
        - Mesure le temps écoulé

    Args:
        couts: matrice des coûts
        P: provisions des fournisseurs
        C: commandes des clients

    Retour :
        durée d’exécution en secondes
    """
    start = time.perf_counter()
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            compute_balas_hammer_solution(couts, P.copy(), C.copy())
    return time.perf_counter() - start


def measure_time_marche_pied_from_NO(couts, P, C):
    """
    Mesure le temps du Marche-Pied à partir d’une solution Nord-Ouest.

    Principe :
        - Calcule une solution initiale Nord-Ouest
        - Applique le Marche-Pied
        - Mesure le temps total

    Args:
        couts: matrice des coûts
        P: provisions des fournisseurs
        C: commandes des clients

    Retour :
        durée d’exécution en secondes
    """
    start = time.perf_counter()

    solution_initiale = compute_northwest_solution(P.copy(), C.copy())
    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            solve_stepping_stone(
                solution_initiale,
                couts,
                display=False
            )

    return time.perf_counter() - start


def measure_time_marche_pied_from_BH(couts, P, C):
    """
    Mesure le temps du Marche-Pied à partir d’une solution Balas-Hammer.

    Principe :
        - Calcule une solution avec Balas-Hammer
        - Applique le Marche-Pied
        - Mesure le temps total

    Args:
        couts: matrice des coûts
        P: provisions des fournisseurs
        C: commandes des clients

    Retour :
        durée d’exécution en secondes
    """
    start = time.perf_counter()

    with open(os.devnull, "w") as fnull:
        with redirect_stdout(fnull):
            solution_initiale = compute_balas_hammer_solution(couts, P.copy(), C.copy())
            solve_stepping_stone(
                solution_initiale,
                couts,
                display=False
            )

    return time.perf_counter() - start
