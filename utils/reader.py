import os


# ---------------------------------------------------------------------
# Lit un fichier texte contenant un tableau de transport
#
# Format des tableaux :
#   n m
#   a11 ... a1m  P1
#   ...
#   an1 ... anm  Pn
#   C1  ...  Cm
#
# Dans ce format :
# - n = nombre de fournisseurs
# - m = nombre de clients
# - chaque ligne i contient m coûts + la provision Pi
# - la dernière ligne contient les m commandes
#
# La fonction retourne trois objets Python :
#   - costs      : matrice des coûts (n × m)
#   - provision  : liste de taille n
#   - commande   : liste de taille m
# ---------------------------------------------------------------------
def read_table_file(path):
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
