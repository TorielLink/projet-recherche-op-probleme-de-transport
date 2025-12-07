import random

# ---------------------------------------------------------------------
# Génère un problème de transport carré de taille n :
# - Matrice des coûts A (n × n)
# - Matrice auxiliaire temp (n × n)
# - Provisions P_i et commandes C_j
#
# Toutes les valeurs générées sont dans [1, 100].
#
# Retour :
#   A, P, C
# ---------------------------------------------------------------------
def generate_random_transport_problem(n):

    # Matrice des coûts A : valeurs entre 1 et 100
    A = [
        [random.randint(1, 100) for _ in range(n)]
        for _ in range(n)
    ]

    temp = [
        [random.randint(1, 100) for _ in range(n)]
        for _ in range(n)
    ]

    P = [sum(temp[i][j] for j in range(n)) for i in range(n)]

    C = [sum(temp[i][j] for i in range(n)) for j in range(n)]

    return A, P, C


# ---------------------------------------------------------------------
# Fonction d'affichage rapide (optionnelle)
# ---------------------------------------------------------------------
def print_random_problem(A, P, C):
    n = len(P)

    print("\n=== Problème généré aléatoirement ===")
    for i in range(n):
        print(A[i], " | ", P[i])
    print("Commandes :", C)
