from collections import deque

def calculer_potentiels(solution, couts, origine_u=None, base_cells=None):
    """
    Calcule les potentiels u (origines) et v (destinations) en partant d'une arête
    de base fixée à 0 comme point de référence, puis en appliquant u_i + v_j = c_ij
    pour chaque arête de base.

    Args:
        solution: matrice des allocations (m x n).
        couts: matrice des coûts unitaires (m x n).
        origine_u: indice de la ligne dont on fixe u=0. Si None, on prend la première
                   ligne qui possède une arête de base.
        base_cells: liste des arêtes de base [(i, j), ...]. Si None, on prend les cellules
                    où solution[i][j] > 0 (y compris les 0 qui pourraient être ajoutés).

    Returns:
        (u, v): listes de potentiels (float ou None) pour les lignes et colonnes.
    """

    m = len(solution)
    n = len(solution[0]) if solution else 0

    # Affichages des tableaux fournis
    print("Tableau des allocations (solution) :")
    for row in solution:
        print(row)
    print("Tableau des coûts :")
    for row in couts:
        print(row)

    # Arêtes de base : cellules avec allocation > 0, ou fournies en paramètre
    if base_cells is None:
        base_cells = [(i, j) for i in range(m) for j in range(n) if solution[i][j] > 0]

    if not base_cells:
        print("Aucune arête de base : potentiels non calculables.")
        return [None] * m, [None] * n

    # Choix du point d'origine u_k = 0
    if origine_u is None:
        origine_u = base_cells[0][0]

    u = [None] * m
    v = [None] * n
    u[origine_u] = 0.0

    # Adjacence sur les arêtes de base
    rows = {i: [] for i in range(m)}
    cols = {j: [] for j in range(n)}
    for i, j in base_cells:
        rows[i].append(j)
        cols[j].append(i)

    q = deque([('u', origine_u)])
    while q:
        kind, idx = q.popleft()
        if kind == 'u':
            i = idx
            if u[i] is None:
                continue
            for j in rows[i]:
                if v[j] is None:
                    v[j] = couts[i][j] - u[i]
                    q.append(('v', j))
        else:
            j = idx
            if v[j] is None:
                continue
            for i in cols[j]:
                if u[i] is None:
                    u[i] = couts[i][j] - v[j]
                    q.append(('u', i))

    # Affichage concis
    print("Potentiels par sommet :")
    for i, val in enumerate(u):
        print(f"u[{i}] = {None if val is None else float(val)}")
    for j, val in enumerate(v):
        print(f"v[{j}] = {None if val is None else float(val)}")

    # Vérification sur les arêtes de base
    incoherences = []
    for i, j in base_cells:
        if u[i] is not None and v[j] is not None:
            if abs(u[i] + v[j] - couts[i][j]) > 1e-8:
                incoherences.append((i, j))
    if incoherences:
        print("Attention : incohérences détectées sur les arêtes de base :", incoherences)

    return u, v