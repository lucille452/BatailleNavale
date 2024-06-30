class NavireFront:
    def __init__(self, taille, nom):
        self.taille = taille
        self.nom = nom
        self.positions = []

    def placement_valide(self, row, col, orientation):
        if orientation == "horizontal":
            return all(0 <= col + i < 10 for i in range(self.taille))
        else:  # Vertical
            return all(0 <= row + i < 10 for i in range(self.taille))

