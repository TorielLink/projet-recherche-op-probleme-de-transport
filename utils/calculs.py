# Calcule le coût total d'un transport en multipliant
# chaque quantité transportée par son coût unitaire.
def cout_total(couts, solution):
    total = 0
    for i in range(len(couts)):
        for j in range(len(couts[0])):
            total += couts[i][j] * solution[i][j]
    return total
