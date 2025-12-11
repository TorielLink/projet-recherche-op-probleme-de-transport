def get_costs(solution, couts, index_prov_arbitraire, display):
    # Calcule les potentiels E pour lignes (E_prov) et colonnes (E_com),
    # puis les coûts potentiels (Couts_pot) et les coûts marginaux (Couts_mar).
    # Params:
    #  - solution: matrice indiquant les arcs présents (None si pas d'arc)
    #  - couts: matrice des coûts originaux associés aux arcs
    #  - index_prov_arbitraire: indice de la ligne dont on fixe E = 0 pour lancer la propagation
    #  - display: bool pour afficher les étapes de calcul

    n = len(solution)
    m = len(solution[0])
    n_couts = len(couts)
    m_couts = len(couts[0]) if couts else 0
    
    # Vérifier que les dimensions correspondent
    if n != n_couts or m != m_couts:
        print(f"Erreur: dimensions incompatibles - solution {n}x{m}, couts {n_couts}x{m_couts}")
        return None, None, None, None

    # Liste des arcs (i,j) présents dans la solution
    arcs = [(i, j) for i in range(n) for j in range(m) if solution[i][j] is not None]

    # Initialisation des potentiels (None = inconnu)
    E_prov = [None] * n  # potentiels des lignes (fournisseurs)
    E_com = [None] * m   # potentiels des colonnes (clients)
    E_prov[index_prov_arbitraire] = 0  # on fixe arbitrairement un potentiel de référence
    print(f"\nOn fixe de façon arbitraire E(P{index_prov_arbitraire+1}) = 0")

    # Propagation des potentiels tant qu'on découvre des valeurs nouvelles
    changed = True
    while changed:
        changed = False
        for (i, j) in arcs:
            # Si la colonne j n'a pas de potentiel mais l'arc part de la ligne de référence,
            # on en déduit E_com[j] = -couts[i][j] (car E_prov - E_com = cout)
            if i == index_prov_arbitraire and E_com[j] is None:
                if display:
                    print(f"E(P{index_prov_arbitraire+1}) - E(C{j+1}) = {couts[i][j]} => E(C{j+1}) = {-couts[i][j]}")
                E_com[j] = -couts[i][j]
                changed = True

            # Si E_com[j] connu et E_prov[i] inconnu, on calcule E_prov[i] = couts[i][j] + E_com[j]
            if E_prov[i] is None and E_com[j] is not None:
                if display:
                    val_signe = f"+ ({E_com[j]})" if E_com[j] < 0 else f"+ {E_com[j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(P{i+1}) = {couts[i][j]} {val_signe} = {couts[i][j] + E_com[j]}")
                E_prov[i] = couts[i][j] + E_com[j]
                changed = True

            # Si E_prov[i] connu et E_com[j] inconnu, on calcule E_com[j] = E_prov[i] - couts[i][j]
            if E_com[j] is None and E_prov[i] is not None:
                if display:
                    val_signe = f"- ({couts[i][j]})" if couts[i][j] < 0 else f"- {couts[i][j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(C{j+1}) = {E_prov[i]} {val_signe}  = {E_prov[i] - couts[i][j]}")
                E_com[j] = E_prov[i] - couts[i][j]
                changed = True

    # Matrice des coûts potentiels: différence des potentiels ligne - colonne
    Couts_pot = [[E_prov[i] - E_com[j] for j in range(m)] for i in range(n)]
    # Matrice des coûts marginaux (réduits): couts originaux - coûts potentiels
    Couts_mar = [[couts[i][j] - Couts_pot[i][j] for j in range(m)] for i in range(n)]

    if display:
        print()
        for i in range(len(E_prov)):
            print(f"E(P{i+1}) = {E_prov[i]}")
        for i in range(len(E_com)):
            print(f"E(C{i+1}) = {E_com[i]}")
        print("Valeurs la plus négative des coûts marginaux :", end=" ")
        most_neg = find_most_negative(Couts_mar)
        if most_neg is None:
            print("Aucune (tous >= 0)")
        else:
            i, j, val = most_neg
            print(f"E(C{i+1}, P{j+1}) = {val}")

    return Couts_pot, Couts_mar, E_prov, E_com

def find_most_negative(couts_mar):
    """
    Parcourt la matrice des coûts marginaux et retourne (i, j, valeur)
    de la valeur la plus négative si elle est < 0, sinon retourne None.
    """
    if not couts_mar:
        return None
    min_val = float('inf')
    min_pos = None
    for i, row in enumerate(couts_mar):
        for j, val in enumerate(row):
            if val is None:
                continue
            if val < min_val:
                min_val = val
                min_pos = (i, j)
    if min_pos is None or min_val >= 0:
        return None
    i, j = min_pos
    return i, j, min_val