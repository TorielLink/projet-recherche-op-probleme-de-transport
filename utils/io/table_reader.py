import os


def read_table_file(path):
    """
    Lit un fichier texte décrivant un problème de transport.

    Format attendu :
        - première ligne : n m
        - n lignes suivantes : m coûts + 1 provision
        - dernière ligne : m commandes

    Args:
        path: chemin vers le fichier texte

    Retour :
        costs: matrice des coûts (n x m)
        provision: liste des provisions
        commande: liste des commandes
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    lines = []

    # Lecture du fichier et conversion en entiers
    with open(path, "r") as f:
        for line in f:
            parts = [p for p in line.strip().split() if p]
            if parts:
                lines.append([int(x) for x in parts])

    # Première ligne : dimensions n et m
    n, m = lines[0]
    expected_rows = n + 2

    if len(lines) != expected_rows:
        raise ValueError(
            f"Format invalide dans {path} : {len(lines)} lignes trouvées, "
            f"{expected_rows} attendues."
        )

    # Extraction des coûts et des provisions dans les n lignes suivantes
    costs = []
    provision = []

    for row in lines[1:1 + n]:
        if len(row) != m + 1:
            raise ValueError(
                f"Ligne invalide : {row}. "
                f"Une ligne doit contenir {m} coûts + 1 provision."
            )
        costs.append(row[:m])
        provision.append(row[m])

    # Dernière ligne : commandes
    commande_row = lines[-1]
    if len(commande_row) != m:
        raise ValueError(
            f"Ligne de commandes invalide : {commande_row}. "
            f"Elle doit contenir exactement {m} valeurs."
        )

    commande = commande_row

    return costs, provision, commande
