from typing import List, Optional, Tuple

from BalasHammer import balas_hammer

def load_tableau(file_path: Optional[str] = None) -> Tuple[List[List[int]], List[int], List[int]]:
    """
    Retourne (tab, provision, commande).
    Si file_path is None -> retourne trois listes vides.
    """
    # Si aucun chemin fourni, renvoyer des structures vides (utile pour tests ou UI)
    if file_path is None:
        return [], [], []

    # On va lire le fichier ligne par ligne et convertir chaque ligne en liste d'entiers.
    # Cela permet de supporter deux formats distincts décrits ci-dessous.
    lines_tokens: List[List[int]] = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                s = line.strip()
                if not s:
                    # Ignorer les lignes vides
                    continue
                # Convertir chaque token numérique en int ; ignorer les tokens vides
                toks = [int(tok) for tok in s.split() if tok]
                if toks:
                    lines_tokens.append(toks)
    except FileNotFoundError:
        # Remonter l'erreur après message explicite
        print("An error occurred: fichier non trouvé.")
        raise

    # Vérification minimale : on veut au moins deux entiers en première ligne : rows et cols
    if not lines_tokens or len(lines_tokens[0]) < 2:
        raise ValueError("Le fichier doit commencer par deux entiers (rows cols).")

    # Récupération du nombre de lignes (rows) et colonnes (cols)
    rows = lines_tokens[0][0]
    cols = lines_tokens[0][1]
    print(f"Création du tableau 2D\nDimensions : {rows} x {cols}")

    # Initialisation des structures de sortie :
    # tab : matrice rows x cols, provision : liste de taille rows, commande : liste de taille cols
    tab: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
    provision: List[int] = []
    commande: List[int] = []

    # Les lignes restantes après la première ligne de dimensions
    remaining_lines = lines_tokens[1:]

    # Tentative d'interprétation du format "ligne-par-ligne":
    # Chaque ligne de la matrice contient cols valeurs, suivies éventuellement d'une valeur de provision.
    if len(remaining_lines) >= rows and all(len(remaining_lines[i]) >= cols for i in range(rows)):
        # Détecter si les premières `rows` lignes contiennent cols+1 tokens (valeurs + provision)
        is_row_with_prov = all(len(remaining_lines[i]) >= cols + 1 for i in range(rows))
        if is_row_with_prov:
            # On remplit la matrice ligne par ligne et on lit la provision à la fin de chaque ligne
            print("Remplissage du tableau principal (format ligne-par-ligne : provision en fin de ligne)")
            for i in range(rows):
                row_tokens = remaining_lines[i]
                # Copier les `cols` valeurs dans la matrice
                for j in range(cols):
                    tab[i][j] = row_tokens[j]
                # Le token suivant est la provision pour cette ligne
                provision.append(row_tokens[cols])

            # Les lignes restantes après la matrice contiennent les commandes (peuvent être sur plusieurs lignes)
            tail_tokens: List[int] = []
            for line in remaining_lines[rows:]:
                tail_tokens.extend(line)
            # Vérifier qu'on a assez de valeurs pour `cols` commandes
            if len(tail_tokens) < cols:
                raise ValueError("Fichier incomplet : pas assez de valeurs pour les commandes")
            commande = tail_tokens[:cols]
            return tab, provision, commande

    # Si on n'a pas choisi le format ligne-par-ligne, on tente le format groupé :
    # matrice complète (rows*cols), puis provisions (rows), puis commandes (cols).
    # Aplatir toutes les lignes restantes en une seule liste de tokens pour lecture séquentielle.
    flat: List[int] = []
    for line in remaining_lines:
        flat.extend(line)

    expected = rows * cols + rows + cols
    # Vérifier qu'on a le nombre minimal d'entiers attendus dans le format groupé
    if len(flat) < expected:
        raise ValueError(f"Fichier incomplet : attendu {expected} valeurs après la ligne de dimensions, trouvé {len(flat)}")

    print("Remplissage du tableau principal (format groupé : matrice puis provision puis commande)")
    index = 0
    # Lire la matrice (rows * cols) de manière séquentielle depuis flat
    for i in range(rows):
        for j in range(cols):
            tab[i][j] = flat[index]
            index += 1

    # Lire les `rows` provisions
    provision = []
    for i in range(rows):
        provision.append(flat[index])
        index += 1

    # Lire les `cols` commandes
    commande = []
    for j in range(cols):
        commande.append(flat[index])
        index += 1

    return tab, provision, commande


def afficher_tab(tab: List[List[int]], provision: List[int], commande: List[int]) -> None:
    # Affiche la matrice ligne par ligne puis les tableaux commande et provision
    for row in tab:
        print(" ".join(str(x) for x in row))
    print("Contenu du tableau commande :")
    print(commande)
    print("Contenu du tableau provision :")
    print(provision)