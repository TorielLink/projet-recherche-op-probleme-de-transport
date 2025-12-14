import csv
import multiprocessing
import os
import psutil
import sys

import matplotlib.pyplot as plt

from utils.benchmark.timing import (
    measure_time_nord_ouest,
    measure_time_balas_hammer,
    measure_time_marche_pied_from_NO,
    measure_time_marche_pied_from_BH,
)
from utils.generation.ramdom_problem import generate_random_transport_problem


def ensure_directories():
    """
    Crée et nettoie les dossiers de sortie.

    Principe :
        - Crée les dossiers Figures/ et Data/
        - Supprime les fichiers existants
    """
    folders = ["Figures", "Data"]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)


# Génère les mesures de temps
def generate_cloud_data(n_values_all, n_values_marche_pied, repetitions=100):
    """
    Génère les données de temps pour les nuages de points.

    Principe :
        - Génère des problèmes aléatoires
        - Mesure les temps des algorithmes
         - Sauvegarde les résultats en CSV

    Args:
        n_values_all: tailles testées pour NO et BH
        n_values_marche_pied: tailles testées pour le Marche-Pied
        repetitions: nombre de répétitions par taille

    Retour :
        results: dictionnaire des temps mesurés
    """

    results = {
        "theta_no": {},
        "theta_bh": {},
        "t_no": {},
        "t_bh": {},
        "sum_no": {},
        "sum_bh": {},
    }

    for n in n_values_all:
        print(f"\n--- Génération des données pour n = {n} ---")

        theta_no_values = []
        theta_bh_values = []
        t_no_values = []
        t_bh_values = []
        sum_no_values = []
        sum_bh_values = []

        for _ in range(repetitions):
            couts, P, C = generate_random_transport_problem(n)

            t_no = measure_time_nord_ouest(couts, P, C)
            t_bh = measure_time_balas_hammer(couts, P, C)

            theta_no_values.append(t_no)
            theta_bh_values.append(t_bh)

            # Marche-pied seulement jusqu’à 160 (sinon temps trop long)
            if n in n_values_marche_pied:
                t_mp_no = measure_time_marche_pied_from_NO(couts, P, C)
                t_mp_bh = measure_time_marche_pied_from_BH(couts, P, C)

                t_no_values.append(t_mp_no)
                t_bh_values.append(t_mp_bh)
                sum_no_values.append(t_no + t_mp_no)
                sum_bh_values.append(t_bh + t_mp_bh)
            else:
                t_no_values.append(None)
                t_bh_values.append(None)
                sum_no_values.append(None)
                sum_bh_values.append(None)

        # Stockage mémoire
        results["theta_no"][n] = theta_no_values
        results["theta_bh"][n] = theta_bh_values
        results["t_no"][n] = t_no_values
        results["t_bh"][n] = t_bh_values
        results["sum_no"][n] = sum_no_values
        results["sum_bh"][n] = sum_bh_values

        # Sauvegarde CSV
        with open(f"Data/results_n{n}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["theta_no", "theta_bh", "t_no", "t_bh", "sum_no", "sum_bh"])
            for i in range(repetitions):
                writer.writerow([
                    theta_no_values[i],
                    theta_bh_values[i],
                    t_no_values[i],
                    t_bh_values[i],
                    sum_no_values[i],
                    sum_bh_values[i],
                ])

    return results


def plot_cloud(results, title, key):
    """
    Trace un nuage de points à partir des données de benchmark.

    Args:
        results: dictionnaire des résultats
        title: titre du graphique
        key: clé des données à tracer
    """

    plt.figure(figsize=(10, 6))

    for n, values in results[key].items():
        filtered = [(n, v) for v in values if v is not None]
        if not filtered:
            continue
        x, y = zip(*filtered)
        plt.scatter(x, y, s=10)

    plt.xlabel("Taille n du problème")
    plt.ylabel("Temps (secondes)")
    plt.title(title)
    plt.grid(True)

    safe_title = title.replace("(", "").replace(")", "").replace(" ", "_")
    plt.savefig(f"Figures/{safe_title}.png")
    print(f"Figure enregistrée : Figures/{safe_title}.png")


if __name__ == "__main__":
    """
    Script principal pour générer et afficher
    les nuages de points de complexité.
    """

    ensure_directories()

    # Force en mono-cœur
    p = psutil.Process(os.getpid())
    p.cpu_affinity([0])

    n_values_all = [10, 20, 40, 80, 160, 320, 640]
    n_values_marche_pied = [10, 20, 40, 80, 160]

    all_results = generate_cloud_data(
        n_values_all,
        n_values_marche_pied,
        repetitions=100
    )

    # Rétablir tous les cœurs
    p.cpu_affinity(list(range(multiprocessing.cpu_count())))

    plot_cloud(all_results, "θNO(n)", "theta_no")
    plot_cloud(all_results, "θBH(n)", "theta_bh")
    plot_cloud(all_results, "tNO(n)", "t_no")
    plot_cloud(all_results, "tBH(n)", "t_bh")
    plot_cloud(all_results, "θNO(n) + tNO(n)", "sum_no")
    plot_cloud(all_results, "θBH(n) + tBH(n)", "sum_bh")

    plt.show()
    sys.exit(0)
