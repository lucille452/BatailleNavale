from Joueur import Joueur


class Gameb:
    def __init__(self):
        self.ia = Joueur()
        self.joueur = Joueur()

    def get_joueur(self):
        return self.joueur

    def get_ia(self):
        return self.ia

