import tkinter as tk
import random
from NavireFront import NavireFront
from GrilleFront import GrilleFront
from Gameb import Gameb
from ia import IA
from tkinter import ttk, messagebox


# Classe principale pour la gestion du jeu
class BatailleNavale:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")

        self.place_navires_mode = True
        self.navires_a_placer = [
            NavireFront(5, "Porte-avions (5)"),
            NavireFront(4, "Cuirassé (4)"),
            NavireFront(3, "Destroyer (3)"),
            NavireFront(3, "Sous-marin (3)"),
            NavireFront(2, "Patrouilleur (2)")
        ]
        self.navires_places = []
        self.tirs_effectues = []  # Positions des tirs effectués
        self.orientation = "horizontal"  # Orientation par défaut

        # Création des grilles visuelles
        self.grille_ia = GrilleFront(self.master, "Grille navires ia", 0, self.on_button_click)
        self.grille_joueur = GrilleFront(self.master, "grille Navires du joueur", 1, self.on_button_click)

        # Création des joueurs / Grilles / Navires back
        game = Gameb()
        self.ia_joueur = game.get_ia()
        self.joueur = game.get_joueur()

        # Initialisation de l'ia
        self.ia = IA(10)

        # Création d'un cadre pour afficher les informations sur l'état du jeu
        self.info_frame = tk.Frame(self.master)
        self.info_frame.grid(row=0, column=1, padx=20, pady=20)

        # Création des étiquettes pour afficher les informations sur l'état du jeu
        self.navires_restants_joueur_label = tk.Label(self.info_frame, text="Navires restants (joueur): 5")
        self.navires_restants_joueur_label.pack(pady=5)
        self.navires_restants_joueur = 5

        self.navires_restants_adversaire_label = tk.Label(self.info_frame, text="Navires restants (adversaire): 5")
        self.navires_restants_adversaire_label.pack(pady=5)
        self.navires_restants_adversaire = 5

        self.tirs_reussis_label = tk.Label(self.info_frame, text="Tirs réussis: 0")
        self.tirs_reussis_label.pack(pady=5)
        self.tirs_reussis = 0

        # Option pour choisir l'orientation
        self.orientation_var = tk.StringVar(self.master, "horizontal")
        self.orientation_menu = tk.OptionMenu(self.master, self.orientation_var, "horizontal", "vertical")
        self.orientation_menu.grid(row=6, column=1, padx=20, pady=10)

        # Combobox pour choisir le navire à placer
        self.navire_var = tk.StringVar(self.master)
        self.navire_combobox = ttk.Combobox(self.master, textvariable=self.navire_var)
        self.navire_combobox.grid(row=7, column=1, padx=20, pady=10)

        # Mettre à jour la combobox avec les navires disponibles
        self.update_navire_combobox()

    def update_navire_combobox(self):
        self.navire_combobox['values'] = [navire.nom for navire in self.navires_a_placer]
        self.navire_var.set('')

    def on_button_click(self, grille, row, col):
        if self.place_navires_mode and grille == self.grille_joueur:
            self.place_navire_joueur(grille, row, col)
        elif grille == self.grille_ia:
            self.tir_joueur(row, col)

    def place_navire_joueur(self, grille, row, col):
        navire_selectionne = self.navire_var.get()
        if navire_selectionne:
            navire = next((navire for navire in self.navires_a_placer if navire.nom == navire_selectionne), None)
            if navire and navire.placement_valide(row, col, self.orientation_var.get()):
                if self.orientation_var.get() == 'horizontal':
                    self.joueur.get_grille().place_navire_horizontal(row, col, navire.taille)
                elif self.orientation_var.get() == 'vertical':
                    self.joueur.get_grille().place_navire_vertical(col, row, navire.taille)
                self.update_grille(grille, self.joueur.get_grille(), navire)

        if len(self.navires_a_placer) == 0:
            self.place_navires_ia()

    def place_navires_ia(self):
        # Exemple d'utilisation de weighted_map pour le placement des navires de l'IA
        for navire in self.ia_joueur.list_navires:
            placed = False
            while not placed:
                row, col = self.ia.guess_random()
                orientation = random.choice(["horizontal", "vertical"])
                if navire.placement_valide(row, col, orientation):
                    if orientation == "horizontal":
                        self.ia_joueur.get_grille().place_navire_horizontal(row, col, navire.taille)
                    else:
                        self.ia_joueur.get_grille().place_navire_vertical(col, row, navire.taille)
                    placed = True

    def update_grille(self, grille_front, grille_joueur, navire):
        for row in range(len(grille_joueur.grille)):
            for col in range(len(grille_joueur.grille[row])):
                if grille_joueur.grille[row][col] == 1:
                    grille_front.update_button(row, col, "grey")
                    grille_front.disable_button(row, col)

        self.navires_a_placer.remove(navire)
        self.update_navire_combobox()
        if not self.navires_a_placer:
            self.place_navires_mode = False
            messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")

    def tir_joueur(self, row, col):
        if (row, col) in self.tirs_effectues:
            messagebox.showinfo("Tir", "Vous avez déjà tiré sur cette case.")
            return

        self.tirs_effectues.append((row, col))
        button = self.grille_ia.buttons[row][col]
        if self.ia_joueur.grille.is_touche(row, col):
            self.ia_joueur.grille.set_touche()
            button.config(bg="red")
            self.tirs_reussis += 1
            self.tirs_reussis_label.config(text=f"Tirs réussis: {self.tirs_reussis}")
            if self.ia_joueur.grille.is_couler(row, col):
                messagebox.showinfo("Tir", "Touché coulé !")
                self.navires_restants_joueur -= 1
                self.navires_restants_joueur_label.config(text=f"Tirs réussis: {self.navires_restants_joueur}")

        else:
            button.config(bg="white")
            messagebox.showinfo("Tir", "Manqué !")
        self.tir_ia()

    def tir_ia(self):
        row, col = self.ia.make_move(hit=False)
        hit = self.ia_joueur.tirer(row, col)
        self.ia.update_shot_map((row, col))
        self.ia.update_history((row, col), hit)

        if hit:
            self.grille_joueur.update_button(row, col, "red")
            if self.joueur.is_coule():
                messagebox.showinfo("Défaite", "L'IA a gagné !")


# Point d'entrée principal
if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
