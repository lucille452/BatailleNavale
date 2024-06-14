from enum import Enum


class Type(Enum):
    NAVIRES = 1
    TIRS = 2


class Grille:
    grille = []
    type_grille = Type.NAVIRES

    def __init__(self, type_grille):
        for i in range(10):
            self.grille.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.type_grille = type_grille

    # placement navire
    def place_navire_horizontal(self, line, start_column, end_column):
        for lineGrille in range(len(self.grille) + 1):
            if lineGrille == line:
                for column in range(start_column, end_column + 1):
                    self.grille[line][column] = 1

    def place_navire_vertical(self, column, start_line, end_line):
        for line in range(start_line, end_line + 1):
            self.grille[line][column] = 1

    def get_grille(self):
        return self.grille

    def get_type_grille(self):
        return self.type_grille

    # istoucher
    def is_touche(self, position_line, position_column):
        self.grille[position_line][position_column] = 2

    # iscouler
    # def is_couler(self):


# grille = Grille(Type.NAVIRES)
# grille.place_navire_vertical(0, 0, 2)
# print(grille.get_grille())
