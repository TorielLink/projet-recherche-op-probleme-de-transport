import random

def generate_random_transport_problem(n):
    """
    Génère un problème de transport carré aléatoire de taille n.

    Principe :
        - Génère une matrice des coûts (n × n)
        - Génère une matrice auxiliaire pour construire
          des provisions et des commandes équilibrées
        - Toutes les valeurs sont dans [1, 100]

    Args:
        n: taille du problème (nombre de fournisseurs = clients)

    Retour :
        A: matrice des coûts
        P: liste des provisions
        C: liste des commandes
    """

    # Matrice des coûts
    A = [
        [random.randint(1, 100) for _ in range(n)]
        for _ in range(n)
    ]

    # Matrice auxiliaire pour garantir l’équilibre
    temp = [
        [random.randint(1, 100) for _ in range(n)]
        for _ in range(n)
    ]

    # Provisions et commandes équilibrées
    P = [sum(temp[i][j] for j in range(n)) for i in range(n)]
    C = [sum(temp[i][j] for i in range(n)) for j in range(n)]

    return A, P, C



def print_random_problem(A, P, C):
    """
    Affiche rapidement un problème de transport généré.

    Fonction utilitaire destinée au debug.
    """

    n = len(P)

    print("\n=== Problème généré aléatoirement ===")
    for i in range(n):
        print(A[i], " | ", P[i])
    print("Commandes :", C)
