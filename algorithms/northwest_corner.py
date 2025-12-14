def compute_northwest_solution(provision, commande):
    """
    Calcule une solution initiale du problème de transport
    en utilisant la méthode du coin Nord-Ouest.

    Principe :
    - On démarre à la case (0,0)
    - À chaque étape, on alloue la quantité maximale possible
    - On avance sur la ligne ou la colonne selon l’épuisement
      des provisions ou des commandes

    Cette méthode garantit une solution réalisable
    mais pas nécessairement optimale.

    Args:
        provision: liste des provisions des fournisseurs
        commande: liste des commandes des clients

    Retour :
        solution: matrice de transport (liste de listes)
    """

    n = len(provision)
    m = len(commande)
    solution = [[0] * m for _ in range(n)]

    p = provision.copy()
    c = commande.copy()

    i = 0
    j = 0

    while i < n and j < m:
        q = min(p[i], c[j])
        solution[i][j] = q
        p[i] -= q
        c[j] -= q

        if p[i] == 0 and c[j] == 0:
            i += 1
            j += 1
        elif p[i] == 0:
            i += 1
        elif c[j] == 0:
            j += 1

    return solution
