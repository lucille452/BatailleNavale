import random

class BatailleNavaleGame:
    def __init__(self):
        self.place_navires_mode = False
        self.navires_a_placer = [(5, "porte-avions"), (4, "croiseur"), (3, "destroyer"), (3, "sous-marin"), (2, "torpilleur")]
        self.navires_places = []
        self.navires_adversaire = self.generer_navires_adversaire()
        self.tirs_effectues = []
        self.tirs_adversaire = []
        self.orientation = "horizontal"

    def toggle_place_navires_mode(self):
        self.place_navires_mode = not self.place_navires_mode

    def update_navire_combobox(self):
        return [navire[1] for navire in self.navires_a_placer]

    def place_navire(self, row, col, navire_selectionne):
        taille = next((item[0] for item in self.navires_a_placer if item[1] == navire_selectionne), None)
        if taille is None:
            return False, "Navire sélectionné non valide."

        if not self.is_placement_possible(row, col, taille):
            return False, "Placement invalide. Choisissez une autre case."

        self.update_grille(row, col, taille, navire_selectionne)
        return True, f"Vous avez placé un {navire_selectionne}."

    def is_placement_possible(self, row, col, taille):
        orientation = self.orientation
        if orientation == "horizontal":
            return all(0 <= col + i < 10 and (row, col + i) not in self.navires_places for i in range(taille))
        else:
            return all(0 <= row + i < 10 and (row + i, col) not in self.navires_places for i in range(taille))

    def update_grille(self, row, col, taille, navire_selectionne):
        orientation = self.orientation
        if orientation == "horizontal":
            for i in range(taille):
                self.navires_places.append((row, col + i))
        else:
            for i in range(taille):
                self.navires_places.append((row + i, col))
        
        self.navires_a_placer = [(t, n) for t, n in self.navires_a_placer if n != navire_selectionne]

    def tirer(self, row, col):
        if (row, col) in self.tirs_effectues:
            return False, "Vous avez déjà tiré sur cette case."

        self.tirs_effectues.append((row, col))
        if (row, col) in self.navires_adversaire:
            return True, "Touché !"
        else:
            return True, "Manqué !"

    def adversaire_tirer(self):
        while True:
            row, col = random.randint(0, 9), random.randint(0, 9)
            if (row, col) not in self.tirs_adversaire:
                self.tirs_adversaire.append((row, col))
                break

        if (row, col) in self.navires_places:
            return row, col, "L'adversaire a touché votre navire !"
        else:
            return row, col, "L'adversaire a manqué."

    def generer_navires_adversaire(self):
        # Exemple simplifié de génération de navires
        positions = []
        for taille, _ in self.navires_a_placer:
            while True:
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    row, col = random.randint(0, 9), random.randint(0, 9 - taille)
                else:
                    row, col = random.randint(0, 9 - taille), random.randint(0, 9)
                
                if self.is_placement_possible_adversaire(row, col, taille, orientation, positions):
                    self.update_positions_adversaire(row, col, taille, orientation, positions)
                    break
        return positions

    def is_placement_possible_adversaire(self, row, col, taille, orientation, positions):
        if orientation == "horizontal":
            return all((row, col + i) not in positions for i in range(taille))
        else:
            return all((row + i, col) not in positions for i in range(taille))

    def update_positions_adversaire(self, row, col, taille, orientation, positions):
        if orientation == "horizontal":
            for i in range(taille):
                positions.append((row, col + i))
        else:
            for i in range(taille):
                positions.append((row + i, col))
