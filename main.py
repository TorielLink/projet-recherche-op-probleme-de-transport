import os

from utils.io.table_reader import read_table_file
from utils.display.table_display import DisplayTable
from utils.math.cost import compute_total_cost

from algorithms.northwest import compute_northwest_solution
from algorithms.stepping_stone import solve_stepping_stone
from algorithms.balas_hammer import compute_balas_hammer_solution

def main():
    """
    Interface principale du programme.

    Principe :
        - Permet de choisir un problème de transport
        - Calcule une solution initiale (Nord-Ouest ou Balas-Hammer)
        - Propose une optimisation par le Marche-Pied
        - Affiche les résultats et les coûts
    """

    data_dir = "Tableaux"

    while True:
        # Liste des fichiers disponibles
        files = sorted([
            f for f in os.listdir(data_dir)
            if f.startswith("tableau") and f.endswith(".txt")
        ])

        print("\n=== Problèmes disponibles ===")
        for i, fname in enumerate(files, 1):
            print(f"{i}. {fname}")

        while True:
            user_input = input("\nChoisissez un numéro de problème : ").strip()

            if not user_input.isdigit():
                print("Veuillez entrer un nombre.")
                continue

            num_pb = int(user_input)

            if 1 <= num_pb <= len(files):
                break
            else:
                print(
                    f"Numéro invalide. Veuillez entrer un nombre entre 1 et {len(files)}."
                )

        chosen_file = files[num_pb - 1]
        full_path = os.path.join(data_dir, chosen_file)

        print(f"\nChargement du fichier : {chosen_file}")

        # Lecture du tableau choisi
        costs, supply, demand = read_table_file(full_path)

        # Affichage du tableau initial
        print("\n=== Tableau des coûts (données initiales) ===")
        table = DisplayTable()
        table.afficher_table(
            DisplayTable.DonneesTest(costs, supply, demand)
        )

        # Choix de l'algorithme initial
        print("\nSélectionnez l'algorithme pour la solution initiale :")
        print("1. Nord-Ouest")
        print("2. Balas-Hammer")

        while True:
            algo_input = input("> ").strip()

            if algo_input in ("1", "2"):
                choix = int(algo_input)
                break

            print("Veuillez entrer 1 ou 2.")

        # Solution initiale
        if choix == 1:
            solution = compute_northwest_solution(supply, demand)

            print("\n=== Solution initiale (Nord-Ouest) ===")
            table.afficher_table(
                DisplayTable.DonneesTest(solution, supply, demand)
            )

        else:
            solution = compute_balas_hammer_solution(costs, supply.copy(), demand.copy())

            print("\n=== Solution initiale (Balas-Hammer) ===")
            table.afficher_table(
                DisplayTable.DonneesTest(solution, supply, demand)
            )

        cost_initial = compute_total_cost(costs, solution)
        print(f"\nCoût initial : {cost_initial}")

        # Optimisation (Marche-Pied)
        while True:
            opt = input(
                "\nSouhaitez-vous optimiser la solution avec le Marche-Pied ? (Oui/Non) : "
            ).strip().lower()

            if opt in ("oui", "o", "non", "n"):
                break

            print("Merci de répondre par Oui ou Non.")

        if opt in ("oui", "o"):
            print("\nOptimisation avec la méthode du Marche-Pied :")

            solution = solve_stepping_stone(
                solution,
                costs,
                supply,
                demand,
                display=True
            )

            print("\n=== Solution finale optimisée ===")
            table.afficher_table(
                DisplayTable.DonneesTest(solution, supply, demand)
            )

            cost_final = compute_total_cost(costs, solution)
            print(f"\nCoût total optimisé : {cost_final}")

        else:
            print("\nSolution conservée sans optimisation.")

        # Continuer ou quitter
        while True:
            again = input(
                "\nSouhaitez-vous analyser un autre problème ? (Oui/Non) : "
            ).strip().lower()

            if again in ("oui", "o"):
                print("\n-----------------------------------------------")
                break

            if again in ("non", "n"):
                print("Fin du programme.")
                return

            print("Merci de répondre par Oui ou Non.")


if __name__ == "__main__":
    main()
