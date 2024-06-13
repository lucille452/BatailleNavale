from Navire import Navire
from Grille import Grille, Type


class Joueur:
    grille_navires = Grille(Type.NAVIRES)
    grille_tirs = Grille(Type.TIRS)
    list_navires = []

    def __init__(self):
        navire1 = Navire(2)
        navire2 = Navire(3)
        navire3 = Navire(4)
        navire4 = Navire(5)
        self.list_navires.append(navire1)
        self.list_navires.append(navire2)
        self.list_navires.append(navire3)
        self.list_navires.append(navire4)

