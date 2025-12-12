from utils.graph_cycle import build_graph_from_solution, bfs_detect_cycle
from utils.maximisation_transport_sur_cycle import maximiser_transport_sur_cycle
from utils.connexite import connexite
from utils.calculs import cout_total


def get_costs(arcs, couts, index_prov_arbitraire=0, display=True):
    # 
    # Calcule les potentiels E(Pi) et E(Cj) ainsi que les coûts marginaux.
    
    # Méthode : On fixe E(P_k) = 0 pour un fournisseur arbitraire k,
    # puis on propage via la relation E(Pi) - E(Cj) = c_ij pour chaque
    # arête (i,j) de la base.
    
    # Args:
    #     arcs: liste des arêtes de base [(i, j), ...]
    #     couts: matrice des coûts unitaires (n × m)
    #     index_prov_arbitraire: indice du fournisseur dont on fixe E=0
    #     display: afficher les calculs intermédiaires
    
    # Returns:
    #     (Couts_pot, Couts_mar, E_prov, E_com)
    #     - Couts_pot : matrice des coûts potentiels
    #     - Couts_mar : matrice des coûts marginaux (c_ij - Couts_pot_ij)
    #     - E_prov : potentiels des fournisseurs
    #     - E_com : potentiels des clients
    # 
    n = len(couts)
    m = len(couts[0])

    E_prov = [None] * n
    E_com = [None] * m
    E_prov[index_prov_arbitraire] = 0
    
    if display:
        print(f"\nOn fixe de façon arbitraire E(P{index_prov_arbitraire+1}) = 0")

    # Propagation des potentiels via les arêtes de base
    changed = True
    while changed:
        changed = False
        for (i, j) in arcs:
            if E_prov[i] is None and E_com[j] is not None:
                E_prov[i] = couts[i][j] + E_com[j]
                if display:
                    val_signe = f"+ ({E_com[j]})" if E_com[j] < 0 else f"+ {E_com[j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(P{i+1}) = {couts[i][j]} {val_signe} = {E_prov[i]}")
                changed = True
            if E_com[j] is None and E_prov[i] is not None:
                E_com[j] = E_prov[i] - couts[i][j]
                if display:
                    val_signe = f"- ({couts[i][j]})" if couts[i][j] < 0 else f"- {couts[i][j]}"
                    print(f"E(P{i+1}) - E(C{j+1}) = {couts[i][j]} => E(C{j+1}) = {E_prov[i]} {val_signe} = {E_com[j]}")
                changed = True

    # Calcul des coûts potentiels et marginaux
    Couts_pot = [[E_prov[i] - E_com[j] if E_prov[i] is not None and E_com[j] is not None else None 
                  for j in range(m)] for i in range(n)]
    Couts_mar = [[couts[i][j] - Couts_pot[i][j] if Couts_pot[i][j] is not None else None 
                  for j in range(m)] for i in range(n)]

    if display:
        print("\n--- Potentiels calculés ---")
        for i in range(n):
            print(f"E(P{i+1}) = {E_prov[i]}")
        for j in range(m):
            print(f"E(C{j+1}) = {E_com[j]}")

    return Couts_pot, Couts_mar, E_prov, E_com


def lowest_cout_mar(Couts_mar, base_cells):
    # 
    # Trouve la case hors-base avec le coût marginal le plus négatif.
    
    # Args:
    #     Couts_mar: matrice des coûts marginaux
    #     base_cells: ensemble des arêtes de base {(i, j), ...}
    
    # Returns:
    #     (position, valeur) ou (None, None) si tous les coûts marginaux >= 0
    # 
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


def trouver_cycle_avec_case(solution, base_cells, nouvelle_case, display=True):
    # 
    # Construit un cycle incluant une nouvelle case et les arêtes de base.
    
    # Le cycle retourné est orienté de telle sorte que la nouvelle case
    # soit en première position (position d'ajout +δ).
    
    # Args:
    #     solution: matrice de transport actuelle
    #     base_cells: liste des arêtes de base
    #     nouvelle_case: tuple (i, j) de la case à ajouter
    #     display: afficher les informations
    
    # Returns:
    #     cycle: liste des sommets du cycle ['P0', 'C1', 'P2', ...]
    #            ou None si aucun cycle trouvé
    # 
    from collections import deque
    
    n = len(solution)
    m = len(solution[0])
    i_new, j_new = nouvelle_case
    
    # Construire le graphe avec les arêtes de base uniquement
    graph = {f"P{i}": [] for i in range(n)}
    graph.update({f"C{j}": [] for j in range(m)})
    
    for (i, j) in base_cells:
        if (i, j) != nouvelle_case:
            graph[f"P{i}"].append(f"C{j}")
            graph[f"C{j}"].append(f"P{i}")
    
    # La nouvelle arête va de P{i_new} à C{j_new}
    # On cherche un chemin de C{j_new} vers P{i_new} dans le graphe existant
    start = f"C{j_new}"
    end = f"P{i_new}"
    
    # BFS pour trouver un chemin
    visited = {start}
    parent = {start: None}
    queue = deque([start])
    found = False
    
    while queue and not found:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor == end:
                parent[neighbor] = current
                found = True
                break
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    if not found:
        if display:
            print(f"Aucun chemin trouvé de {start} à {end}")
        return None
    
    # Reconstruire le chemin de end vers start
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]
    
    
    cycle = [f"P{i_new}", f"C{j_new}"]
    # Ajouter le chemin de C{j_new} vers P{i_new} (sans les extrémités)
    inner_path = path[1:-1]  # Enlever P{i_new} au début et C{j_new} à la fin
    inner_path.reverse()
    cycle.extend(inner_path)
    
    if display:
        print(f"\nCycle détecté : {' -> '.join(cycle)} -> {cycle[0]}")
    
    return cycle


def afficher_matrice_couts_marginaux(Couts_mar, base_cells):
    # Affiche la matrice des coûts marginaux de façon lisible.
    n = len(Couts_mar)
    m = len(Couts_mar[0])
    
    print("\n--- Matrice des coûts marginaux ---")
    header = "     " + "  ".join(f"C{j+1:>3}" for j in range(m))
    print(header)
    
    for i in range(n):
        row_str = f"P{i+1}  "
        for j in range(m):
            if (i, j) in base_cells:
                row_str += f"  [B]"  # Case de base
            elif Couts_mar[i][j] is None:
                row_str += f"  ---"
            else:
                row_str += f"{Couts_mar[i][j]:>5}"
        print(row_str)


def marche_pied(solution, couts, display=True):
    # 
    # Algorithme du Marche-Pied (Stepping Stone) pour optimiser une solution de transport.
    
    # Étapes :
    # 1. Vérifier/garantir la connexité et compléter la base à m+n-1 arêtes
    # 2. Calculer les potentiels E(Pi) et E(Cj)
    # 3. Calculer les coûts marginaux pour les cases hors-base
    # 4. Tant qu'il existe un coût marginal négatif :
    #    a. Sélectionner la case avec le coût marginal le plus négatif
    #    b. Construire un cycle incluant cette case
    #    c. Maximiser le transport sur ce cycle (méthode du stepping stone)
    #    d. Mettre à jour la base et recalculer
    # 5. Retourner la solution optimale
    
    # Args:
    #     solution: matrice de transport initiale (n × m)
    #     couts: matrice des coûts unitaires (n × m)
    #     display: afficher les étapes intermédiaires
    
    # Returns:
    #     solution: matrice de transport optimisée
    # 
    n = len(solution)
    m = len(couts[0]) if couts else 0
    iteration = 0
    
    if display:
        print("=" * 60)
        print("ALGORITHME DU MARCHE-PIED")
        print("=" * 60)
        cout_init = cout_total(couts, solution)
        print(f"\nCoût initial : {cout_init}")
    
    # Étape 1 : Vérifier et garantir la connexité, compléter la base
    if display:
        print("\n--- Étape 1 : Vérification de la connexité ---")
    
    solution, base_cells = connexite(solution, couts)
    base_set = set(base_cells)
    
    if display:
        print(f"Base initiale : {len(base_cells)} arêtes (attendu : {n + m - 1})")
        print(f"Arêtes de base : {[(i+1, j+1) for (i, j) in base_cells]}")
    
    # Boucle principale d'optimisation
    while True:
        iteration += 1
        
        if display:
            print(f"\n{'='*60}")
            print(f"ITÉRATION {iteration}")
            print(f"{'='*60}")
        
        # Étape 2 : Calcul des potentiels
        if display:
            print("\n--- Calcul des potentiels ---")
        
        Couts_pot, Couts_mar, E_prov, E_com = get_costs(
            base_cells, couts, index_prov_arbitraire=0, display=display
        )
        
        # Affichage de la matrice des coûts marginaux
        if display:
            afficher_matrice_couts_marginaux(Couts_mar, base_set)
        
        # Étape 3 : Trouver le coût marginal minimal (hors base)
        min_pos, min_value = lowest_cout_mar(Couts_mar, base_set)
        
        if display:
            if min_pos:
                print(f"\nCoût marginal minimal : {min_value} en position P{min_pos[0]+1}-C{min_pos[1]+1}")
            else:
                print("\nTous les coûts marginaux sont >= 0")
        
        # Condition d'arrêt : solution optimale
        if min_pos is None:
            if display:
                print("\n" + "=" * 60)
                print("SOLUTION OPTIMALE ATTEINTE")
                print("=" * 60)
                cout_final = cout_total(couts, solution)
                print(f"Coût final : {cout_final}")
            break
        
        # Étape 4 : Trouver le cycle incluant la nouvelle case
        if display:
            print(f"\n--- Recherche du cycle avec la case ({min_pos[0]+1}, {min_pos[1]+1}) ---")
        
        cycle = trouver_cycle_avec_case(solution, base_cells, min_pos, display)
        
        if cycle is None:
            if display:
                print("ERREUR : Aucun cycle trouvé. Vérifiez la connexité de la base.")
            break
        
        # Étape 5 : Maximiser le transport sur le cycle
        # On doit d'abord ajouter temporairement la nouvelle case à la solution
        i_new, j_new = min_pos
        solution[i_new][j_new] = 0  # Valeur temporaire pour le cycle
        
        solution, delta, aretes_supprimees = maximiser_transport_sur_cycle(solution, cycle)
        
        if display:
            print(f"\nδ appliqué : {delta}")
            cout_actuel = cout_total(couts, solution)
            print(f"Coût après itération {iteration} : {cout_actuel}")
        
        # Étape 6 : Mise à jour de la base
        # Ajouter la nouvelle arête
        base_set.add(min_pos)
        
        # Retirer UNE SEULE arête parmi celles dont le flux est devenu nul
        # (pour maintenir m+n-1 arêtes dans la base)
        removed_one = False
        for (i, j) in aretes_supprimees:
            if (i, j) in base_set and (i, j) != min_pos and not removed_one:
                base_set.discard((i, j))
                removed_one = True
                if display:
                    print(f"Arête retirée de la base : P{i+1}-C{j+1}")
        
        # Si plusieurs arêtes ont été mises à 0, garder les autres comme arêtes dégénérées
        
        # Reconstruire la liste des arêtes de base
        base_cells = list(base_set)
        
        if display:
            print(f"\nNouvelle base : {len(base_cells)} arêtes")
            print(f"Arêtes de base : {[(i+1, j+1) for (i, j) in base_cells]}")
        
        # Sécurité : limite d'itérations
        if iteration > 100:
            if display:
                print("\nATTENTION : Limite d'itérations atteinte (100)")
            break
    
    return solution


def afficher_solution(solution, couts):
    # Affiche la solution finale avec le coût total.
    n = len(solution)
    m = len(solution[0])
    
    print("\n--- Solution finale ---")
    header = "     " + "  ".join(f"C{j+1:>4}" for j in range(m))
    print(header)
    
    for i in range(n):
        row_str = f"P{i+1}  "
        for j in range(m):
            if solution[i][j] > 0:
                row_str += f"{solution[i][j]:>5}"
            else:
                row_str += f"    -"
        print(row_str)
    
    total = cout_total(couts, solution)
    print(f"\nCoût total : {total}")
