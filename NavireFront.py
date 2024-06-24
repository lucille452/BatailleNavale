class NavireFront:
    def __init__(self, taille, nom):
        self.taille = taille
        self.nom = nom
        self.positions = []

    def placer(self, row, col, orientation):
        positions = []
        if orientation == "horizontal":
            positions = [(row, col + i) for i in range(self.taille)]
        else:  # Vertical
            positions = [(row + i, col) for i in range(self.taille)]

        self.positions = positions
        return positions

    def placement_valide(self, row, col, orientation):
        if orientation == "horizontal":
            return all(0 <= col + i < 10 for i in range(self.taille))
        else:  # Vertical
            return all(0 <= row + i < 10 for i in range(self.taille))

    def coule(self, tirs_effectues):
        return all(pos in tirs_effectues for pos in self.positions)

