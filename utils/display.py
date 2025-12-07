class DisplayTable:

    # Structure contenant :
    # - la matrice affichée (coûts ou quantités)
    # - les provisions de chaque fournisseur
    # - les commandes de chaque client
    class DonneesTest:
        def __init__(self, couts, provision, commande):
            self.couts = couts
            self.provision = provision
            self.commande = commande

    # Retourne la longueur maximale des valeurs d’un tableau.
    # Sert à calculer automatiquement la largeur des colonnes.
    def get_max_length(self, arr):
        return max(len(str(v)) for v in arr)

    # Affiche un texte centré dans une largeur donnée.
    def print_padding(self, s, width):
        padding = (width - len(s)) // 2
        print(" " * padding + s + " " * (width - len(s) - padding), end="")

    # Affiche une ligne de séparation horizontale dans le tableau.
    def print_separator(self, row_width, col_width, nb_col):
        print("-" * row_width, end="+")
        for _ in range(nb_col):
            print("-" * col_width + "+", end="")
        print("-" * row_width)

    # Retourne le total transporté si le problème est équilibré,
    # sinon retourne 0.
    def compute_total(self, data):
        if sum(data.provision) == sum(data.commande):
            return sum(data.provision)
        return 0

    # Affiche la matrice sous forme de tableau avec entête, séparateurs,
    # lignes des fournisseurs, et ligne des commandes.
    def afficher_table(self, data):
        m = len(data.provision)
        n = len(data.commande)

        col_width = max(self.get_max_length(data.commande), len("Commandes")) + 2
        row_width = max(self.get_max_length(data.provision), len("Provisions")) + 2

        # En-tête
        self.print_padding("", row_width)
        print("|", end="")
        for j in range(n):
            self.print_padding(f"C{j+1}", col_width)
            print("|", end="")
        self.print_padding("Provisions", row_width)
        print()

        self.print_separator(row_width, col_width, n)

        # Lignes fournisseurs
        for i in range(m):
            self.print_padding(f"P{i+1}", row_width)
            print("|", end="")
            for j in range(n):
                self.print_padding(str(data.couts[i][j]), col_width)
                print("|", end="")
            self.print_padding(str(data.provision[i]), row_width)
            print()
            self.print_separator(row_width, col_width, n)

        # Ligne commandes + total
        self.print_padding("Commandes", row_width)
        print("|", end="")
        for j in range(n):
            self.print_padding(str(data.commande[j]), col_width)
            print("|", end="")

        total = self.compute_total(data)
        self.print_padding(str(total), row_width)
        print()
