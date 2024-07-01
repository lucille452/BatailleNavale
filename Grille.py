from Navire import Navire


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
                # Vérifie si toutes les positions du navire sont touchées
                for pos in navire.positions:
                    line, col = pos
                    if self.grille[line][col] != 2:  # 2 représente une position touchée
                        return False
                return True
        return False

    def placement_valide(self, line, start_column, length, orientation):
        if orientation == 'horizontal':
            if start_column + length > len(self.grille):
                return False
            for col in range(start_column, start_column + length):
                if self.grille[line][col] != 0:
                    return False
        elif orientation == 'vertical':
            if line + length > len(self.grille):
                return False
            for row in range(line, line + length):
                if self.grille[row][start_column] != 0:
                    return False
        return True