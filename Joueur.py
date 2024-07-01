from Navire import Navire
from Grille import Grille


class Joueur:
    list_navires = []

    def __init__(self):
        self.navire1 = Navire(2)
        self.navire2 = Navire(3)
        self.navire21 = Navire(3)
        self.navire3 = Navire(4)
        self.navire4 = Navire(5)
        self.list_navires.append(self.navire1)
        self.list_navires.append(self.navire2)
        self.list_navires.append(self.navire21)
        self.list_navires.append(self.navire3)
        self.list_navires.append(self.navire4)
        self.grille = Grille()

    def get_grille(self):
        return self.grille

    def get_list_navires(self):
        return self.list_navires
