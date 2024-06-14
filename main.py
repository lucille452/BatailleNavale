import tkinter as tk
from tkinter import ttk, messagebox
import random

class BatailleNavale:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")
        self.create_grilles()
        self.place_navires_mode = False
        self.navires_a_placer = [(5, "porte-avions"), (4, "croiseur"), (3, "destroyer"), (3, "sous-marin"), (2, "torpilleur")]
        self.navires_places = []
        self.navires_adversaire = self.generer_navires_adversaire()  # Positions des navires de l'adversaire
        self.tirs_effectues = []  # Positions des tirs effectués
        self.orientation = "horizontal"  # Orientation par défaut

    def create_grilles(self):
        # Grille des tirs
        self.tir_frame = tk.Frame(self.master)
        self.tir_frame.grid(row=0, column=0, padx=20, pady=20)
        self.tir_buttons = self.create_grille(self.tir_frame, "Tirs sur l'adversaire")

        # Grille des navires du joueur
        self.navires_joueur_frame = tk.Frame(self.master)
        self.navires_joueur_frame.grid(row=1, column=0, padx=20, pady=20)
        self.navires_joueur_buttons = self.create_grille(self.navires_joueur_frame, "Navires du joueur")

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

    def create_grille(self, parent, label_text):
        # Label de la grille
        label = tk.Label(parent, text=label_text)
        label.grid(row=0, column=1, columnspan=10)

        # Lettres sur l'axe des abscisses
        for col in range(10):
            letter = chr(ord('A') + col)
            tk.Label(parent, text=letter).grid(row=1, column=col+1)

        # Chiffres sur l'axe des ordonnées
        for row in range(10):
            tk.Label(parent, text=str(row + 1)).grid(row=row+2, column=0)

        # Création des boutons de la grille
        buttons = []
        for row in range(10):
            button_row = []
            for col in range(10):
                button = tk.Button(parent, text=' ', width=2, height=1, bg='light blue', command=lambda r=row, c=col: self.on_button_click(parent, r, c))
                button.grid(row=row+2, column=col+1)
                button_row.append(button)
            buttons.append(button_row)
        return buttons

    def toggle_place_navires_mode(self):
        self.place_navires_mode = not self.place_navires_mode
        if self.place_navires_mode:
            messagebox.showinfo("Placement de Navires", "Cliquez sur la grille pour placer vos navires.")
            # Mettre à jour les options de la combobox
            self.update_navire_combobox()
        else:
            messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")

    def update_navire_combobox(self):
        self.navire_combobox['values'] = [navire[1] for navire in self.navires_a_placer]
        self.navire_var.set('')

    def on_button_click(self, parent, row, col):
        if self.place_navires_mode and parent == self.navires_joueur_frame:
            self.place_navire(parent, row, col)
        elif parent == self.tir_frame:
            self.tirer(row, col)
        else:
            messagebox.showinfo("Clic", f"Vous avez cliqué sur la case ({row + 1}, {chr(ord('A') + col)})")

    def place_navire(self, parent, row, col):
        navire_selectionne = self.navire_var.get()
        if navire_selectionne:
            taille = next(item[0] for item in self.navires_a_placer if item[1] == navire_selectionne)
            if self.is_placement_possible(row, col, taille):
                self.update_grille(parent, row, col, taille, navire_selectionne)
            else:
                messagebox.showinfo("Placement", "Placement invalide. Choisissez une autre case.")
        else:
            messagebox.showinfo("Placement", "Veuillez sélectionner un navire à placer.")

    def is_placement_possible(self, row, col, taille):
        orientation = self.orientation_var.get()
        if orientation == "horizontal":
            return all(0 <= col + i < 10 and (row, col + i) not in self.navires_places for i in range(taille))
        else:  # Vertical
            return all(0 <= row + i < 10 and (row + i, col) not in self.navires_places for i in range(taille))

    def update_grille(self, parent, row, col, taille, navire_selectionne):
        orientation = self.orientation_var.get()
        if orientation == "horizontal":
            for i in range(taille):
                button = parent.grid_slaves(row=row + 2, column=col + i + 1)[0]
                button.config(bg="grey")
                button.config(state="disabled")
                self.navires_places.append((row, col + i))
        else:  # Vertical
            for i in range(taille):
                button = parent.grid_slaves(row=row + i + 2, column=col + 1)[0]
                button.config(bg="grey")
                button.config(state="disabled")
                self.navires_places.append((row + i, col))
        
        messagebox.showinfo("Placement", f"Vous avez placé un {navire_selectionne}.")
        self.navires_a_placer = [(t, n) for t, n in self.navires_a_placer if n != navire_selectionne]
        self.update_navire_combobox()  # Mettre à jour les options de la combobox
        if not self.navires_a_placer:
            self.place_navires_mode = False
            messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")
            self.place_navires_button.config(state="disabled")

    def tirer(self, row, col):
        if (row, col) in self.tirs_effectues:
            messagebox.showinfo("Tir", "Vous avez déjà tiré sur cette case.")
            return

        self.tirs_effectues.append((row, col))
        button = self.tir_buttons[row][col]
        if (row, col) in self.navires_adversaire:
            button.config(bg="red")
            messagebox.showinfo("Tir", "Touché !")
        else:
            button.config(bg="white")
            messagebox.showinfo("Tir", "Manqué !")

    def adversaire_tirer(self):
        while True:
            row, col = random.randint(0, 9), random.randint(0, 9)
            if (row, col) not in self.tirs_effectues:
                self.tirs_effectues.append((row, col))
                break

        button = self.navires_joueur_buttons[row][col]
        if (row, col) in self.navires_places:
            button.config(bg="red")
            messagebox.showinfo("Alerte", f"L'adversaire a touché votre navire en ({row + 1}, {chr(ord('A') + col)}) !")
        else:
            button.config(bg="white")
            messagebox.showinfo("Alerte", f"L'adversaire a tiré en ({row + 1}, {chr(ord('A') + col)}) et a manqué.")

    def generer_navires_adversaire(self):
        # Logique pour générer des navires pour l'adversaire (exemple simplifié)
        return [(random.randint(0, 9), random.randint(0, 9)) for _ in range(5)]

if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
