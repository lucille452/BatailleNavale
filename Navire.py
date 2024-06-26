from enum import Enum


class Etat(Enum):
    PLACER = 1
    TOUCHER = 2
    COULER = 3


class Navire:
    taille = 0
    etat = Etat.PLACER
    nbr_toucher = 0
    positions = []

    def __init__(self, taille):
        self.taille = taille

    def change_etat(self):
        self.etat = Etat.TOUCHER
        self.nbr_toucher += 1
        if self.nbr_toucher == self.taille:
            self.etat = Etat.COULER

    def get_etat(self):
        return self.etat

    def get_taille(self):
        return self.taille

    def add_position(self, position):
        self.positions.append(position)