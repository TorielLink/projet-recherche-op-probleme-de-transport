from collections import deque


# ---------------------------------------------------------------------
# Construit un graphe biparti à partir d'une matrice de transport.
#
# - P0, P1, ... représentent les fournisseurs
# - C0, C1, ... représentent les clients
#
# Une arête est créée entre Pi et Cj si la quantité transportée > 0.
# Ce graphe est utilisé pour vérifier l’existence d’un cycle dans
# une proposition de transport.
# ---------------------------------------------------------------------
def build_graph_from_solution(solution):
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


# ---------------------------------------------------------------------
# Détecte la présence d’un cycle dans le graphe à l’aide d’un BFS.
#
# Principe :
# - On explore chaque composante du graphe.
# - Si l’on revisite un sommet déjà visité et que ce n’est pas
#   le parent direct, cela signifie qu’un cycle est présent.
#
# La fonction renvoie :
#   (True, liste_des_sommets_du_cycle)
#   (False, None) si aucun cycle n'est trouvé.
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Reconstruit un cycle simple à partir de deux sommets détectés.
#
# Méthode :
# - On remonte séparément les parents de u et de v.
# - On trouve leur premier ancêtre commun.
# - On combine les deux chemins pour obtenir un cycle lisible.
# ---------------------------------------------------------------------
def build_cycle(u, v, parent):
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


# ---------------------------------------------------------------------
# Vérifie si un graphe est connexe grâce à un BFS.
#
# Si le graphe n'est pas connexe :
#   - renvoie False
#   - renvoie la liste des composantes connexes (liste de listes)
#
# Si le graphe est connexe :
#   - renvoie True
#   - renvoie [liste complète des nœuds]
# ---------------------------------------------------------------------
def check_connectivity(graph):
    visited = set()
    components = []

    for start in graph:
        if start not in visited:
            queue = deque([start])
            visited.add(start)
            component = [start]

            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if v not in visited:
                        visited.add(v)
                        queue.append(v)
                        component.append(v)

            components.append(component)

    # Si plus d'une composante, le graphe n'est PAS connexe
    if len(components) > 1:
        return False, components

    return True, components

