import tkinter as tk
from tkinter import ttk, messagebox

# Classe Navire
class Navire:
    def __init__(self, taille, nom):
        self.taille = taille
        self.nom = nom
        self.positions = []

    def placer(self, row, col, orientation):
        positions = []
        if orientation == "horizontal":
            positions = [(row, col + i) for i in range(self.taille)]
        else:  # Vertical
            positions = [(row + i, col) for i in range(self.taille)]
        
        self.positions = positions
        return positions

    def placement_valide(self, row, col, orientation):
        if orientation == "horizontal":
            return all(0 <= col + i < 10 for i in range(self.taille))
        else:  # Vertical
            return all(0 <= row + i < 10 for i in range(self.taille))

    def coule(self, tirs_effectues):
        return all(pos in tirs_effectues for pos in self.positions)

# Classe Grille
class Grille:
    def __init__(self, parent, label_text, row_offset, click_handler):
        self.buttons = []
        self.frame = None
        self.parent = parent
        self.label_text = label_text
        self.row_offset = row_offset
        self.click_handler = click_handler
        self.create_grille()

    def create_grille(self):
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=self.row_offset, column=0, padx=20, pady=20)

        tk.Label(self.frame, text=self.label_text).grid(row=0, columnspan=11)

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for col, letter in enumerate(letters):
            tk.Label(self.frame, text=letter).grid(row=1, column=col+1)

        for row in range(10):
            tk.Label(self.frame, text=str(row+1)).grid(row=row+2, column=0)

        self.buttons = [[tk.Button(self.frame, text=' ', width=2, height=1, bg='light blue', command=lambda r=row, c=col: self.click_handler(self, r, c)) for col in range(10)] for row in range(10)]
        for row in range(10):
            for col in range(10):
                self.buttons[row][col].grid(row=row+2, column=col+1)

    def update_button(self, row, col, color):
        button = self.buttons[row][col]
        button.config(bg=color)

    def disable_button(self, row, col):
        button = self.buttons[row][col]
        button.config(state="disabled")

# Classe principale pour la gestion du jeu
class BatailleNavale:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")
        
        self.place_navires_mode = False
        self.navires_a_placer = [
            Navire(5, "Porte-avions"),
            Navire(4, "Cuirassé"),
            Navire(3, "Destroyer"),
            Navire(3, "Sous-marin"),
            Navire(2, "Patrouilleur")
        ]
        self.navires_places = []
        self.tirs_effectues = []  # Positions des tirs effectués
        self.orientation = "horizontal"  # Orientation par défaut

        # Création des grilles visuelles
        self.grille_tirs = Grille(self.master, "Tirs sur l'adversaire", 0, self.on_button_click)
        self.grille_navires_joueur = Grille(self.master, "Navires du joueur", 1, self.on_button_click)

        # Création d'un cadre pour les boutons des navires du joueur
        self.navires_frame = tk.Frame(self.master)
        self.navires_frame.grid(row=1, column=1, padx=20, pady=20)

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

        # Bouton pour passer en mode placement de navires
        self.place_navires_button = tk.Button(self.master, text="Placer Navires", command=self.toggle_place_navires_mode)
        self.place_navires_button.grid(row=2, column=0, padx=20, pady=10)

        # Option pour choisir l'orientation
        self.orientation_var = tk.StringVar(self.master, "horizontal")
        self.orientation_menu = tk.OptionMenu(self.master, self.orientation_var, "horizontal", "vertical")
        self.orientation_menu.grid(row=3, column=0, padx=20, pady=10)

        # Combobox pour choisir le navire à placer
        self.navire_var = tk.StringVar(self.master)
        self.navire_combobox = ttk.Combobox(self.master, textvariable=self.navire_var)
        self.navire_combobox.grid(row=4, column=0, padx=20, pady=10)

    def toggle_place_navires_mode(self):
        self.place_navires_mode = not self.place_navires_mode
        if self.place_navires_mode:
            # messagebox.showinfo("Placement de Navires", "Cliquez sur la grille pour placer vos navires.")
            self.update_navire_combobox()
        # else:
        #     messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")

    def update_navire_combobox(self):
        self.navire_combobox['values'] = [navire.nom for navire in self.navires_a_placer]
        self.navire_var.set('')

    def on_button_click(self, grille, row, col):
        if self.place_navires_mode and grille == self.grille_navires_joueur:
            self.place_navire(grille, row, col)
        elif grille == self.grille_tirs:
            self.tirer(row, col)
        # else:
        #     messagebox.showinfo("Clic", f"Vous avez cliqué sur la case ({row + 1}, {chr(ord('A') + col)})")

    def place_navire(self, grille, row, col):
        navire_selectionne = self.navire_var.get()
        if navire_selectionne:
            navire = next((navire for navire in self.navires_a_placer if navire.nom == navire_selectionne), None)
            if navire and navire.placement_valide(row, col, self.orientation_var.get()):
                positions = navire.placer(row, col, self.orientation_var.get())
                self.navires_places.extend(positions)
                self.update_grille(grille, positions, navire)
        #     else:
        #         messagebox.showinfo("Placement", "Placement invalide. Choisissez une autre case.")
        # else:
        #     messagebox.showinfo("Placement", "Veuillez sélectionner un navire à placer.")

    def update_grille(self, grille, positions, navire):
        for row, col in positions:
            grille.update_button(row, col, "grey")
            grille.disable_button(row, col)
        
        # messagebox.showinfo("Placement", f"Vous avez placé un {navire.nom}.")
        self.navires_a_placer.remove(navire)
        self.update_navire_combobox()
        if not self.navires_a_placer:
            self.place_navires_mode = False
            # messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")
            self.place_navires_button.config(state="disabled")

    def tirer(self, row, col):
        if (row, col) in self.tirs_effectues:
            # messagebox.showinfo("Tir", "Vous avez déjà tiré sur cette case.")
            return

        self.tirs_effectues.append((row, col))
        button = self.grille_tirs.buttons[row][col]
        if (row, col) in self.navires_places:
            button.config(bg="red")
            # messagebox.showinfo("Tir", "Touché !")
        else:
            button.config(bg="white")
            # messagebox.showinfo("Tir", "Manqué !")

# Point d'entrée principal
if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
