# Module: connexite.py
# Fonctions pour vérifier et garantir la connexité d'un graphe biparti dérivé d'une "solution"
# (matrice solution) et pour compléter une base sans créer de cycles.
# Utilise build_graph_from_solution pour construire le graphe initial et
# bfs_detect_cycle pour détecter la présence de cycles.

from utils.graph_cycle import build_graph_from_solution, bfs_detect_cycle


def _components(graph):
    """
    Calcule les composantes connexes du graphe.
    - graph : dictionnaire {noeud: [voisins,...]}
    Retour :
    - comp  : dictionnaire {noeud: id_composante}
    - cid   : nombre de composantes distinctes
    Méthode : parcours en profondeur (stack) itératif.
    """
    comp = {}
    cid = 0
    for node in graph:
        if node in comp:
            continue
        stack = [node]
        comp[node] = cid
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in comp:
                    comp[v] = cid
                    stack.append(v)
        cid += 1
    return comp, cid


def _connect_graph(graph, edges, solution, candidates):
    """
    Tente de rendre le graphe connexe en ajoutant des arêtes à coût minimal
    parmi les "candidates" (liste triée de tuples (cout, i, j) correspondant
    aux cases solution[i][j] == 0). On ajoute une arête seulement si elle
    relie deux composantes distinctes et si l'arête n'est pas déjà présente.
    Modifie :
    - graph (ajout des voisins),
    - edges (ensemble des arêtes de la base),
    - solution (marque la case correspondante à 0 pour indiquer l'ajout).
    Retour :
    - True si le graphe devient connexe, False sinon.
    """
    comp, num_comp = _components(graph)
    if num_comp == 1:
        print("Le graphe est déjà connexe.")
        return True

    print(f"Le graphe n'est pas connexe ({num_comp} composantes). Ajout d'arêtes...")

    # Copie de la liste de candidats pour pouvoir pop sans altérer l'original.
    remaining = list(candidates)
    
    while num_comp > 1 and remaining:
        added = False
        
        for idx, (cost, i, j) in enumerate(remaining):
            u, v = f"P{i}", f"C{j}"
            # Ignorer si arête déjà présente
            if (u, v) in edges:
                continue
            # Les deux noeuds doivent exister dans le graphe
            if u not in comp or v not in comp:
                continue
            # Ne relier que des composantes différentes
            if comp[u] == comp[v]:
                continue

            # Ajout temporel de l'arête dans la structure du graphe
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
            # Mettre à jour la "solution" pour marquer l'ajout (convention locale)
            solution[i][j] = 0
            added = True

            print(f"  - Connexion des composantes via (P{i+1}, C{j+1}) coût {cost}")

            # Recalculer les composantes après ajout et retirer le candidat utilisé
            comp, num_comp = _components(graph)
            remaining.pop(idx)
            break

        if not added:
            # Plus aucun candidat ne permet de connecter deux composantes distinctes
            print("Impossible de connecter toutes les composantes avec les cases à 0 disponibles.")
            return False

    return num_comp == 1


def _complete_basis(graph, edges, solution, candidates, target_edges):
    """
    Complète la base jusqu'à target_edges arêtes sans créer de cycle.
    Parcourt les candidats (copie) et ajoute une arête si elle ne crée pas de
    cycle (vérifié par bfs_detect_cycle) et si elle n'appartient pas déjà à la même composante.
    Modifie graph, edges et solution.
    """
    remaining = list(candidates)
    
    while len(edges) < target_edges and remaining:
        comp, _ = _components(graph)
        added = False

        for idx, (cost, i, j) in enumerate(remaining):
            u, v = f"P{i}", f"C{j}"
            # Ignorer arêtes déjà présentes
            if (u, v) in edges:
                continue
            # Ignorer si u et v sont déjà dans la même composante (ajout créerait un cycle)
            if u in comp and v in comp and comp[u] == comp[v]:
                continue

            # Tester l'ajout temporaire
            graph[u].append(v)
            graph[v].append(u)

            # Vérifier s'il y a maintenant un cycle
            has_cycle, _ = bfs_detect_cycle(graph)
            if has_cycle:
                # Annuler l'ajout si cycle détecté
                graph[u].pop()
                graph[v].pop()
                continue

            # Valider l'ajout : mise à jour de l'ensemble d'arêtes et de la solution
            edges.add((u, v))
            solution[i][j] = 0
            added = True

            print(f"  - Ajout de l'arête (P{i+1}, C{j+1}) coût {cost} (aucun cycle créé)")
            remaining.pop(idx)
            break

        if not added:
            # Aucun candidat ne peut être ajouté sans former un cycle
            print("Aucune arête supplémentaire ne peut être ajoutée sans créer de cycle.")
            break


def connexite(solution, couts):
    """
    Interface principale :
    - Vérifie la connexité du graphe biparti issu de 'solution' (matrice m x n).
    - Si nécessaire, ajoute des arêtes (cases à 0) de coût minimal pour connecter
      le graphe.
    - Puis complète la base jusqu'à m + n - 1 arêtes sans créer de cycle.
    Retour :
    - (solution_modifiee, base_cells)
      où base_cells est la liste des tuples (i, j) correspondant aux arêtes de la base.
    """

    m = len(solution)  # nombre de fournisseurs (lignes)
    n = len(solution[0]) if solution else 0  # nombre de clients (colonnes)

    # Construire le graphe initial à partir de la solution (utilise la convention P{i}, C{j})
    graph = build_graph_from_solution(solution)
    # S'assurer que tous les noeuds existent dans le dictionnaire même s'ils n'ont pas de voisins
    for i in range(m):
        graph.setdefault(f"P{i}", [])
    for j in range(n):
        graph.setdefault(f"C{j}", [])

    # Ensemble des arêtes présentes (base) : on considère solution[i][j] > 0 comme arête
    edges = {(f"P{i}", f"C{j}") for i in range(m) for j in range(n) if solution[i][j] > 0}
    target_edges = m + n - 1  # taille attendue d'une base pour un graphe connexe sans cycles

    if len(edges) >= target_edges:
        print("La base contient déjà au moins n+m-1 arêtes (aucun ajout nécessaire).")
        base_cells = [(i, j) for i in range(m) for j in range(n) if (f"P{i}", f"C{j}") in edges]
        return solution, base_cells

    # Liste des candidats triés par coût puis indices (cases où solution[i][j] == 0)
    candidates = sorted(
        [(couts[i][j], i, j) for i in range(m) for j in range(n) if solution[i][j] == 0],
        key=lambda x: (x[0], x[1], x[2])
    )

    # 1) Rendre le graphe connexe si nécessaire
    connected = _connect_graph(graph, edges, solution, candidates)
    if not connected:
        # Retourner la solution telle quelle si impossible de connecter
        base_cells = [(i, j) for i in range(m) for j in range(n) if (f"P{i}", f"C{j}") in edges]
        return solution, base_cells

    # 2) Compléter la base jusqu'à m+n-1 sans créer de cycles
    _complete_basis(graph, edges, solution, candidates, target_edges)

    # Construire la liste finale des arêtes de base (indices i,j en 1-based)
    base_cells = [(i, j) for i in range(m) for j in range(n) if (f"P{i}", f"C{j}") in edges]
    return solution, base_cells
