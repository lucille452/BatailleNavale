from Navire import Navire, Etat


class Grille:
    def __init__(self):
        self.grille = [[0]*10 for _ in range(10)]
        self.navires = []

    def place_navire_horizontal(self, line, start_column, length):
        navire = Navire(length)
        for column in range(start_column, start_column + length):
            self.grille[line][column] = 1
            navire.add_position((line, column))
        self.navires.append(navire)

    def place_navire_vertical(self, column, start_line, length):
        navire = Navire(length)
        for line in range(start_line, start_line + length):
            self.grille[line][column] = 1
            navire.add_position((line, column))
        self.navires.append(navire)

    def get_grille(self):
        return self.grille

    def set_touche(self, position_line, position_column):
        self.grille[position_line][position_column] = 2
        for navire in self.navires:
            if (position_line, position_column) in navire.positions:
                navire.change_etat()
                break

    def is_touche(self, position_line, position_column):
        return self.grille[position_line][position_column] == 1

    def is_couler(self, position_line, position_column):
        for navire in self.navires:
            if (position_line, position_column) in navire.positions:
                return navire.get_etat() == Etat.COULER
        return False
