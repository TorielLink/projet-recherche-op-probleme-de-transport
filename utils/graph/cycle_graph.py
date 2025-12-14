from collections import deque


def build_graph_from_solution(solution):
    """
    Construit le graphe biparti associé à une solution de transport.

    Principe :
        - Un sommet Pi pour chaque fournisseur
        - Un sommet Cj pour chaque client
        - Une arête Pi–Cj si la quantité transportée est > 0

    Args:
        solution: matrice de transport

    Retour :
        graph: graphe biparti sous forme de dictionnaire
    """

    n = len(solution)
    m = len(solution[0])

    graph = {f"P{i}": [] for i in range(n)}
    graph.update({f"C{j}": [] for j in range(m)})

    for i in range(n):
        for j in range(m):
            if solution[i][j] > 0:
                graph[f"P{i}"].append(f"C{j}")
                graph[f"C{j}"].append(f"P{i}")

    return graph


def bfs_detect_cycle(graph):
    visited = set()
    parent = {}

    for start in graph:
        if start not in visited:

            queue = deque([start])
            visited.add(start)
            parent[start] = None

            while queue:
                u = queue.popleft()

                for v in graph[u]:

                    if v not in visited:
                        visited.add(v)
                        parent[v] = u
                        queue.append(v)

                    elif parent[u] != v:
                        return True, build_cycle(u, v, parent)

    return False, None


def build_cycle(u, v, parent):
    """
    Reconstruit un cycle simple à partir des parents du BFS.

    Principe :
        - Remonter les parents depuis u et v
        - Trouver le premier sommet commun
        - Combiner les deux chemins

    Args:
        u: premier sommet
        v: second sommet
        parent: dictionnaire des parents

    Retour :
        cycle: liste des sommets du cycle
    """
    path_u = []
    x = u
    while x is not None:
        path_u.append(x)
        x = parent[x]

    path_v = []
    y = v
    while y is not None:
        path_v.append(y)
        y = parent[y]

    for node in path_u:
        if node in path_v:
            common = node
            break

    cycle = []
    for node in path_u:
        cycle.append(node)
        if node == common:
            break

    path_v = path_v[:path_v.index(common)]
    cycle += reversed(path_v)

    return cycle


def find_cycle_with_entering_cell(solution, base_cells, nouvelle_case, display=True):
    """
    Construit le cycle du marche-pied associé à une case entrante.

    Principe :
        - Graphe construit à partir de la base
        - Recherche d’un chemin reliant les deux sommets
        - Cycle orienté pour appliquer le delta

    Args:
        solution: solution courante
        base_cells: arêtes de la base
        entering_cell: case candidate
        display: affiche le cycle si True

    Retour :
        cycle: cycle du marche-pied ou None
    """

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

    # Reconstruire le chemin depuis la fin au début
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent[current]

    cycle = [f"P{i_new}", f"C{j_new}"]

    # Ajouter le chemin de C{j_new} vers P{i_new} (sans les extrémités)
    inner_path = path[1:-1]
    inner_path.reverse()
    cycle.extend(inner_path)

    if display:
        print(f"\nCycle détecté : {' -> '.join(cycle)} -> {cycle[0]}")

    return cycle
