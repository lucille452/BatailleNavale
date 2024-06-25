import tkinter as tk
from NavireFront import NavireFront
from GrilleFront import GrilleFront
from Game import Game
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
        self.grille_tirs = GrilleFront(self.master, "Tirs sur l'adversaire", 0, self.on_button_click)
        self.grille_navires_joueur = GrilleFront(self.master, "Navires du joueur", 1, self.on_button_click)

        # Création des joueurs / Grilles / Navires back
        game = Game()
        self.ia = game.get_ia()
        self.joueur = game.get_joueur()

        # Création d'un cadre pour afficher les informations sur l'état du jeu
        self.info_frame = tk.Frame(self.master)
        self.info_frame.grid(row=0, column=1, padx=20, pady=20)

        # Création des étiquettes pour afficher les informations sur l'état du jeu
        self.navires_restants_joueur_label = tk.Label(self.info_frame, text="Navires restants (joueur): 5")
        self.navires_restants_joueur_label.pack(pady=5)

        self.navires_restants_adversaire_label = tk.Label(self.info_frame, text="Navires restants (adversaire): 5")
        self.navires_restants_adversaire_label.pack(pady=5)

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
        if self.place_navires_mode and grille == self.grille_navires_joueur:
            self.place_navire(grille, row, col)
        elif grille == self.grille_tirs:
            self.tirer(row, col)

    def place_navire(self, grille, row, col):
        navire_selectionne = self.navire_var.get()
        if navire_selectionne:
            navire = next((navire for navire in self.navires_a_placer if navire.nom == navire_selectionne), None)
            if navire and navire.placement_valide(row, col, self.orientation_var.get()):
                if self.orientation_var.get() == 'horizontal':
                    self.joueur.grille_navires.place_navire_horizontal(row, col, navire.taille)
                elif self.orientation_var.get() == 'vertical':
                    self.joueur.grille_navires.place_navire_vertical(col, row, navire.taille)
                self.update_grille(grille, self.joueur.get_grille_navires(), navire)

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

    def tirer(self, row, col):
        if (row, col) in self.tirs_effectues:
            messagebox.showinfo("Tir", "Vous avez déjà tiré sur cette case.")
            return

        self.tirs_effectues.append((row, col))
        button = self.grille_tirs.buttons[row][col]
        if (row, col) in self.navires_places:
            button.config(bg="red")
            self.tirs_reussis += 1
            self.tirs_reussis_label.config(text=f"Tirs réussis: {self.tirs_reussis}")
            if self.is_coule(row, col):
                messagebox.showinfo("Tir", "Touché coulé !")
        else:
            button.config(bg="white")
            messagebox.showinfo("Tir", "Manqué !")

    def is_coule(self, row, col):
        for navire in self.navires_places:
            if (row, col) in navire.positions:
                if navire.coule(self.tirs_effectues):
                    return True
        return False


# Point d'entrée principal
if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
