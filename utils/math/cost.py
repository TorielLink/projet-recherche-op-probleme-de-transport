def compute_total_cost(couts, solution):
    """
    Calcule le coût total d’une solution de transport.

    Principe :
        - Multiplie chaque quantité transportée
          par son coût unitaire
        - Additionne toutes les contributions

    Args:
        couts: matrice des coûts unitaires
        solution: matrice de transport

    Retour :
        total: coût total du transport
    """

    total = 0
    for i in range(len(couts)):
        for j in range(len(couts[0])):
            total += couts[i][j] * solution[i][j]
    return total
