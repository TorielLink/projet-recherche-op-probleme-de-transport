def compute_penalties(C, lignes_actives, colonnes_actives):
    """
    Calcule les pénalités de Balas-Hammer.

    Principe :
        - Pour chaque ligne active, la pénalité est la différence
          entre les deux plus petits coûts de la ligne
        - Même principe pour chaque colonne active

    Args:
        C: matrice des coûts
        lignes_actives: indices des lignes encore actives
        colonnes_actives: indices des colonnes encore actives

    Retour :
        penalites: dictionnaire {("ligne"/"colonne", index): pénalité}
    """

    penalites = {}

    # Pénalités des lignes
    for i in lignes_actives:
        couts = [C[i][j] for j in colonnes_actives]
        couts_tries = sorted(couts)
        if len(couts_tries) >= 2:
            penalites[("ligne", i)] = couts_tries[1] - couts_tries[0]
        else:
            penalites[("ligne", i)] = 0

    # Pénalités des colonnes
    for j in colonnes_actives:
        couts = [C[i][j] for i in lignes_actives]
        couts_tries = sorted(couts)
        if len(couts_tries) >= 2:
            penalites[("colonne", j)] = couts_tries[1] - couts_tries[0]
        else:
            penalites[("colonne", j)] = 0

    return penalites


def afficher_penalites(penalites, lignes_actives, colonnes_actives):
    """
        Affiche l’évolution des pénalités à chaque itération.

        Principe :
            - Affiche les lignes et colonnes supprimées
            - Affiche la pénalité maximale courante

        Cette fonction est uniquement destinée au debug.
        """
    # Initialisation sans afficher la première itération vide
    if not hasattr(afficher_penalites, "iter"):
        afficher_penalites.iter = 0
        afficher_penalites.prev_lignes = set(lignes_actives)
        afficher_penalites.prev_colonnes = set(colonnes_actives)
        return

    afficher_penalites.iter += 1
    current_lignes = set(lignes_actives)
    current_colonnes = set(colonnes_actives)

    removed_lignes = sorted(afficher_penalites.prev_lignes - current_lignes)
    removed_colonnes = sorted(afficher_penalites.prev_colonnes - current_colonnes)

    if removed_lignes:
        lignes_str = "  ".join(f"P{idx+1}" for idx in removed_lignes)
    else:
        lignes_str = "Aucun"

    if removed_colonnes:
        colonnes_str = "  ".join(f"C{idx+1}" for idx in removed_colonnes)
    else:
        colonnes_str = "Aucun"

    max_pen = max(penalites.values()) if penalites else 0

    print(f"Itération {afficher_penalites.iter}: Lignes supprimées : {lignes_str} | Colonnes supprimées : {colonnes_str} | Pénalité max : {max_pen}")

    afficher_penalites.prev_lignes = current_lignes
    afficher_penalites.prev_colonnes = current_colonnes

def compute_balas_hammer_solution(C, O, D, display=True):
    """
    Calcule une solution initiale du problème de transport
    avec la méthode de Balas-Hammer.

    Principe :
        - Calcul des pénalités lignes / colonnes
        - Sélection de la pénalité maximale
        - Allocation sur la case de coût minimal correspondante
        - Mise à jour des offres et demandes
        - Répétition jusqu’à épuisement

    Args:
        C: matrice des coûts
        O: offres (provisions)
        D: demandes (commandes)
        display: affiche les pénalités si True

    Retour :
        X: solution initiale de transport
    """

    m = len(C)
    n = len(C[0])

    # Indices actifs
    lignes_actives = set(range(m))
    colonnes_actives = set(range(n))

    # Solution initialisée à 0
    X = [[0 for _ in range(n)] for _ in range(m)]

    while lignes_actives and colonnes_actives:

        # 1. Calcul des pénalités
        penalites = compute_penalties(C, lignes_actives, colonnes_actives)
        if display:
            afficher_penalites(penalites, lignes_actives, colonnes_actives)

        # 2. Sélection de la plus grande pénalité
        (type_sel, index_sel), _ = max(penalites.items(), key=lambda item: item[1])

        # 3. Déterminer la case de coût minimal dans la ligne/colonne choisie
        if type_sel == "ligne":
            i = index_sel
            # choisir la colonne avec le coût minimum parmi les colonnes actives
            j = min(colonnes_actives, key=lambda col: C[i][col])
        else:
            j = index_sel
            # choisir la ligne avec le coût minimum parmi les lignes actives
            i = min(lignes_actives, key=lambda row: C[row][j])

        # 4. Allocation
        quantite = min(O[i], D[j])
        X[i][j] = quantite

        # 5. Mise à jour offre / demande
        O[i] -= quantite
        D[j] -= quantite

        # 6. Désactivation ligne ou colonne
        if O[i] == 0:
            lignes_actives.remove(i)
        if D[j] == 0:
            colonnes_actives.remove(j)

    return X
