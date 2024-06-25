class Grille:
    grille = []

    def __init__(self):
        for i in range(10):
            self.grille.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # placement navire
    def place_navire_horizontal(self, line, start_column, length):
        for lineGrille in range(len(self.grille) + 1):
            if lineGrille == line:
                for column in range(start_column, start_column + length):
                    self.grille[line][column] = 1

    def place_navire_vertical(self, column, start_line, length):
        for line in range(start_line, start_line + length):
            self.grille[line][column] = 1

    def get_grille(self):
        return self.grille

    # istoucher
    def set_touche(self, position_line, position_column):
        self.grille[position_line][position_column] = 2

    def is_touche(self, position_line, position_column):
        if self.grille[position_line][position_column] == 1:
            return True
        else:
            return False

    # iscouler
    # def is_couler(self):


# grille = Grille(Type.NAVIRES)
# grille.place_navire_vertical(0, 0, 2)
# print(grille.get_grille())
