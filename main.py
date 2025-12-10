import os
from utils.reader import read_table_file
from utils.display import DisplayTable
from algorithms.northwest import afficher_solution_nord_ouest
from algorithms.BalasHammer import balas_hammer

def main():
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

            numPb = int(user_input)

            if 1 <= numPb <= len(files):
                break
            else:
                print(f"Numéro invalide. Veuillez entrer un nombre entre 1 et {len(files)}.")

        chosen_file = files[numPb - 1]
        full_path = os.path.join(data_dir, chosen_file)

        print(f"\nChargement du fichier : {chosen_file}")

        # Lecture du tableau choisi
        couts, provision, commande = read_table_file(full_path)

        # Affichage du tableau initial
        print("\n=== Tableau des coûts (données initiales) ===")
        data_initiale = DisplayTable.DonneesTest(couts, provision, commande)

        table = DisplayTable()
        table.afficher_table(data_initiale)

        # Choix de l'algorithme initial
        print("\nSélectionnez l'algorithme pour la solution initiale :")
        print("1. Nord-Ouest")
        print("2. Balas-Hammer")

        # TODO : proposer toutes les étapes de Balas-Hammer lorsqu'il sera implémenté.
        while True:
            algo_input = input("> ").strip()

            if not algo_input.isdigit():
                print("Veuillez entrer 1 ou 2.")
                continue

            choix = int(algo_input)

            if choix in (1, 2):
                break
            else:
                print("Veuillez entrer 1 ou 2.")

        if choix == 1:
            afficher_solution_nord_ouest(provision, commande, couts)
        elif choix == 2:
            # TODO : appeler ici la méthode Balas-Hammer une fois implémentée
            print("\nLa méthode Balas-Hammer n'est pas encore implémentée.")
            solution = balas_hammer(couts, provision, commande)
            print("\nSolution proposée (matrice des allocations) :")

            for ligne in solution:
                print(ligne)

        # TODO : implémenter l'algorithme du Marche-Pied
        print("\nOptimisation avec la méthode du Marche-Pied :")
        print("Cette partie sera intégrée plus tard.")

        # TODO : afficher la solution finale optimisée une fois l'optimisation programmée
        print("\nLa solution finale optimisée sera affichée ici lorsqu'elle sera disponible.")

        # Choix de continuer ou quitter
        while True:
            again = input("\nSouhaitez-vous analyser un autre problème ? (Oui/Non) : ").strip().lower()

            if again in ("oui", "o"):
                print("\n-----------------------------------------------")
                break
            elif again in ("non", "n"):
                print("Fin du programme.")
                return
            else:
                print("Merci de répondre par Oui ou Non.")


if __name__ == "__main__":
    main()
