from utils.display import DisplayTable
from utils.calculs import cout_total

# ---------------------------------------------------------------------
# Calcule une solution initiale avec la méthode du Nord-Ouest.
#
# On remplit la matrice de transport en partant du coin supérieur gauche.
# À chaque case, on place la quantité maximale possible, puis on avance
# soit sur la ligne suivante, soit sur la colonne suivante en fonction
# de l’épuisement des provisions ou des commandes.
#
# Cette méthode produit toujours une solution réalisable.
# ---------------------------------------------------------------------
def northwest_solution(provision, commande):
    n = len(provision)
    m = len(commande)
    solution = [[None] * m for _ in range(n)]

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


# ---------------------------------------------------------------------
# Affiche la solution Nord-Ouest sous forme de tableau et calcule son coût.
#
# Affiche :
# - la matrice de la solution
# - les provisions et commandes
# - le coût total de transport
# ---------------------------------------------------------------------
def afficher_solution_nord_ouest(provision, commande, couts):
    solution = northwest_solution(provision, commande)

    data = DisplayTable.DonneesTest(
        couts=solution,
        provision=provision,
        commande=commande
    )

    print("\n=== Solution Nord-Ouest ===")
    table = DisplayTable()
    table.afficher_table(data)

    cout = cout_total(couts, solution)
    print("\nCoût total du transport :", cout)

    return solution, cout
