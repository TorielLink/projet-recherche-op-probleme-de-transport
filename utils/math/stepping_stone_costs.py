def compute_potentials_and_reduced_costs(arcs, couts, index_prov_arbitraire=0, display=True):
    """
    Calcule les potentiels et les coûts marginaux.

    Principe :
        - Fixe un potentiel fournisseur à 0
        - Propage les potentiels sur les arêtes de base
         - Calcule les coûts marginaux des autres cases

    Args:
        arcs: arêtes de base (i, j)
        couts: matrice des coûts
        index_prov_arbitraire: fournisseur de référence
        display: affiche les calculs si True

    Retour :
        Couts_pot: matrice des coûts potentiels
        Couts_mar: matrice des coûts marginaux
        E_prov: potentiels fournisseurs
        E_com: potentiels clients
    """

    n = len(couts)
    m = len(couts[0])

    E_prov = [None] * n
    E_com = [None] * m
    E_prov[index_prov_arbitraire] = 0

    if display:
        print(f"\nOn fixe de façon arbitraire E(P{index_prov_arbitraire + 1}) = 0")

    # Propagation des potentiels via les arêtes de base
    changed = True
    while changed:
        changed = False
        for (i, j) in arcs:
            if E_prov[i] is None and E_com[j] is not None:
                E_prov[i] = couts[i][j] + E_com[j]
                if display:
                    val_signe = f"+ ({E_com[j]})" if E_com[j] < 0 else f"+ {E_com[j]}"
                    print(
                        f"E(P{i + 1}) - E(C{j + 1}) = {couts[i][j]} => E(P{i + 1}) = {couts[i][j]} {val_signe} = {E_prov[i]}")
                changed = True
            if E_com[j] is None and E_prov[i] is not None:
                E_com[j] = E_prov[i] - couts[i][j]
                if display:
                    val_signe = f"- ({couts[i][j]})" if couts[i][j] < 0 else f"- {couts[i][j]}"
                    print(
                        f"E(P{i + 1}) - E(C{j + 1}) = {couts[i][j]} => E(C{j + 1}) = {E_prov[i]} {val_signe} = {E_com[j]}")
                changed = True

    # Calcul des coûts potentiels et marginaux
    Couts_pot = [[E_prov[i] - E_com[j] if E_prov[i] is not None and E_com[j] is not None else None
                  for j in range(m)] for i in range(n)]
    Couts_mar = [[couts[i][j] - Couts_pot[i][j] if Couts_pot[i][j] is not None else None
                  for j in range(m)] for i in range(n)]

    if display:
        print("\n--- Potentiels calculés ---")
        for i in range(n):
            print(f"E(P{i + 1}) = {E_prov[i]}")
        for j in range(m):
            print(f"E(C{j + 1}) = {E_com[j]}")

    return Couts_pot, Couts_mar, E_prov, E_com


def find_most_negative_reduced_cost(Couts_mar, base_cells):
    """
    Cherche la case hors-base au coût marginal le plus négatif.

    Args:
        Couts_mar: matrice des coûts marginaux
        base_cells: ensemble des cases de base

    Retour :
        (position, valeur) ou (None, None) si optimal
    """

    min_value = 0  # On cherche strictement négatif
    min_pos = None

    for i in range(len(Couts_mar)):
        for j in range(len(Couts_mar[0])):
            # Ignorer les cases de base et les valeurs None
            if (i, j) in base_cells:
                continue
            if Couts_mar[i][j] is None:
                continue
            if Couts_mar[i][j] < min_value:
                min_value = Couts_mar[i][j]
                min_pos = (i, j)

    return min_pos, min_value
