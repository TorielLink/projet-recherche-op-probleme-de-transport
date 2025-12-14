from utils.graph.connectivity import ensure_connectivity
from utils.graph.cycle_graph import find_cycle_with_entering_cell
from utils.graph.cycle_optimization import maximize_flow_on_cycle
from utils.math.cost import compute_total_cost
from utils.math.stepping_stone_costs import (
    compute_potentials_and_reduced_costs,
    find_most_negative_reduced_cost,
)


def solve_stepping_stone(solution, couts, provision=None, commande=None, display=True):
    """
    Optimise une solution de transport avec l’algorithme du Marche-Pied.

    Principe :
        - Rend la base connexe
        - Calcule les potentiels et coûts marginaux
        - Choisit une case entrante négative
        - Construit le cycle associé
        - Applique un transfert sur le cycle
        - Répète jusqu’à optimalité

    Args:
        solution: solution initiale de transport
        couts: matrice des coûts
        provision: provisions (optionnel)
        commande: commandes (optionnel)
        display: affiche les étapes si True

    Retour :
        solution: solution optimisée
    """

    # Copie de la solution
    sol = [row.copy() for row in solution]

    if display:
        print("\n" + "=" * 60)
        print("MARCHE-PIED")
        print("=" * 60)
        print(f"Coût initial : {compute_total_cost(couts, sol)}")

    # Rend la base connexe et correcte
    sol, base_cells = ensure_connectivity(sol, couts)
    base_set = set(base_cells)

    iteration = 0
    MAX_ITER = 200  # Sécurité anti-boucle infinie

    while True:
        iteration += 1

        if display:
            print(f"\n--- Itération {iteration} ---")

        # Potentiels + coûts marginaux
        Couts_pot, Couts_mar, _, _ = compute_potentials_and_reduced_costs(
            base_cells, couts, index_prov_arbitraire=0, display=display
        )

        # Recherche de la case entrante
        min_pos, min_value = find_most_negative_reduced_cost(Couts_mar, base_set)

        # Condition d'arrêt : optimalité atteinte
        if min_pos is None:
            if display:
                print("\nAucun coût marginal négatif n’a été détecté.")
                print("Solution optimale atteinte.")
            return sol

        if display:
            print(
                f"Case entrante : P{min_pos[0] + 1}-C{min_pos[1] + 1} "
                f"(coût marginal = {min_value})"
            )

        # Recherche du cycle
        cycle = find_cycle_with_entering_cell(
            sol,
            base_cells,
            min_pos,
            display
        )

        if cycle is None:
            if display:
                print("Erreur : aucun cycle trouvé.")
            return sol

        # Ajout de la case entrante à la solution temporaire
        i_new, j_new = min_pos
        sol[i_new][j_new] = 0

        # Maximisation sur le cycle
        sol, delta, aretes_supprimees = maximize_flow_on_cycle(sol, cycle)

        # Condition d'arrêt : delta nul
        if delta == 0:
            if display:
                print("Arrêt : delta nul (solution dégénérée ou déjà optimale).")
                print(f"Coût final : {compute_total_cost(couts, sol)}")
            return sol

        if display:
            print(f"δ appliqué : {delta}")
            print(f"Coût après itération {iteration} : {compute_total_cost(couts, sol)}")

        base_set.add(min_pos)

        # Retrait d'une arête
        for (i, j) in aretes_supprimees:
            if (i, j) in base_set and (i, j) != min_pos:
                base_set.remove((i, j))
                if display:
                    print(f"Arête retirée : P{i + 1}-C{j + 1}")
                break

        base_cells = list(base_set)

        # Condition d'arrêt : nombre maximal d'itérations
        if iteration >= MAX_ITER:
            if display:
                print("Arrêt : nombre maximal d'itérations atteint.")
                print(f"Coût courant : {compute_total_cost(couts, sol)}")
            return sol
