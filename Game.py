from Joueur import Joueur


class Game:
    def __init__(self):
        self.ia = Joueur()
        self.joueur = Joueur()

    def get_ia(self):
        return self.ia

    def get_joueur(self):
        return self.joueur
