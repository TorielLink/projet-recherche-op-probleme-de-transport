import os
import matplotlib.pyplot as plt
import csv

from utils.ramdom_problem import generate_random_transport_problem
from utils.time_test_fonction import (
    measure_time_nord_ouest,
    measure_time_balas_hammer,
    measure_time_marche_pied_from_NO,
    measure_time_marche_pied_from_BH,
)


# ---------------------------------------------------------------------
# Création et nettoyage automatique des dossiers Figures/ et Data/
# ---------------------------------------------------------------------
def ensure_directories():
    # Dossiers à gérer
    folders = ["Figures", "Data"]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

        # Supprimer tous les anciens fichiers du dossier
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Erreur lors de la suppression de {file_path} : {e}")


# ---------------------------------------------------------------------
# Génère 100 mesures pour chaque taille n
# Stocke les résultats dans Data/
# ---------------------------------------------------------------------
def generate_cloud_data(n_list):
    results = {
        "theta_no": {},
        "theta_bh": {},
        "t_no": {},
        "t_bh": {},
        "sum_no": {},
        "sum_bh": {},
    }

    for n in n_list:
        print(f"\n--- Génération des données pour n = {n} ---")

        theta_no_values = []
        theta_bh_values = []
        t_no_values = []
        t_bh_values = []
        sum_no_values = []
        sum_bh_values = []

        # 100 répétitions par valeur de n
        for _ in range(100):
            couts, P, C = generate_random_transport_problem(n)

            t1 = measure_time_nord_ouest(couts, P, C)
            t2 = measure_time_balas_hammer(couts, P, C)
            t3 = measure_time_marche_pied_from_NO(couts, P, C)
            t4 = measure_time_marche_pied_from_BH(couts, P, C)

            theta_no_values.append(t1)
            theta_bh_values.append(t2)
            t_no_values.append(t3)
            t_bh_values.append(t4)
            sum_no_values.append(t1 + t3)
            sum_bh_values.append(t2 + t4)

        # Ajout en mémoire
        results["theta_no"][n] = theta_no_values
        results["theta_bh"][n] = theta_bh_values
        results["t_no"][n] = t_no_values
        results["t_bh"][n] = t_bh_values
        results["sum_no"][n] = sum_no_values
        results["sum_bh"][n] = sum_bh_values

        # Sauvegarde CSV propre (écrase automatiquement)
        with open(f"Data/results_n{n}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["theta_no", "theta_bh", "t_no", "t_bh", "sum_no", "sum_bh"])
            for i in range(100):
                writer.writerow([
                    theta_no_values[i],
                    theta_bh_values[i],
                    t_no_values[i],
                    t_bh_values[i],
                    sum_no_values[i],
                    sum_bh_values[i]
                ])

    return results


# ---------------------------------------------------------------------
# Crée un nuage de points et sauvegarde l'image
# ---------------------------------------------------------------------
def plot_cloud(results, title, key):
    plt.figure(figsize=(10, 6))

    for n, values in results[key].items():
        x = [n] * len(values)
        plt.scatter(x, values, s=10)

    plt.xlabel("Taille n du problème")
    plt.ylabel("Temps (secondes)")
    plt.title(title)
    plt.grid(True)

    # Sauvegarde PNG (écrase automatiquement si des résultats avaient été enregistrer avant)
    safe_title = title.replace("(", "").replace(")", "").replace(" ", "_")
    output_path = f"Figures/{safe_title}.png"
    plt.savefig(output_path)

    print(f"Figure enregistrée : {output_path}")


# ---------------------------------------------------------------------
# Main : exécute tous les graphes
# ---------------------------------------------------------------------
if __name__ == "__main__":
    ensure_directories()

    # Définition des tailles des problèmes de transport
    n_values = [10, 40, 100]

    all_results = generate_cloud_data(n_values)

    plot_cloud(all_results, "θNO(n)", "theta_no")
    plot_cloud(all_results, "θBH(n)", "theta_bh")
    plot_cloud(all_results, "tNO(n)", "t_no")
    plot_cloud(all_results, "tBH(n)", "t_bh")
    plot_cloud(all_results, "θNO(n) + tNO(n)", "sum_no")
    plot_cloud(all_results, "θBH(n) + tBH(n)", "sum_bh")

    plt.show()
