import tkinter as tk
from tkinter import ttk, messagebox
import random

class GrilleUI:
    def __init__(self, parent, label_text, row_offset):
        self.parent = parent
        self.label_text = label_text
        self.row_offset = row_offset
        self.create_grille()

    def create_grille(self):
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=self.row_offset, column=0, padx=20, pady=20)

        # Ajout du texte au-dessus de la grille
        self.label = tk.Label(self.frame, text=self.label_text)
        self.label.grid(row=0, columnspan=11)

        # Ajout des étiquettes pour les abscisses (lettres)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for col, letter in enumerate(letters):
            label = tk.Label(self.frame, text=letter)
            label.grid(row=1, column=col+1)

        # Ajout des étiquettes pour les ordonnées (chiffres)
        for row in range(10):
            label = tk.Label(self.frame, text=str(row+1))
            label.grid(row=row+2, column=0)

        self.buttons = []
        for row in range(10):
            button_row = []
            for col in range(10):
                button = tk.Button(self.frame, text=' ', width=2, height=1, bg='light blue')
                button.grid(row=row+2, column=col+1)
                button_row.append(button)
            self.buttons.append(button_row)

class Navires:
    def __init__(self):
        self.navires_a_placer = {
            "Porte-avions": 5,
            "Cuirassé": 4,
            "Destroyer": 3,
            "Sous-marin": 3,
            "Patrouilleur": 2
        }

class NavireButton(tk.Button):
    def __init__(self, master, navire_type, navire_length):
        self.navire_type = navire_type
        self.navire_length = navire_length
        tk.Button.__init__(self, master, text=f"{navire_type} ({navire_length})", width=15, height=1, bg='darkgray', fg='white', font=('Times New Roman', 10))
        self.configure(command=self.place_ship)

    def place_ship(self):
        print(f"Vous avez sélectionné le {self.navire_type} ({self.navire_length})")
        # Vous pouvez ajouter ici le code pour placer le navire sur la grille de jeu.

class NavireFrame(tk.Frame):
    def __init__(self, master, navire_type, navire_length):
        tk.Frame.__init__(self, master)
        self.navire_type = navire_type
        self.navire_length = navire_length
        self.configure(width=100, height=40)  # Ajustez la taille selon vos besoins
        self.pack_propagate(False)  # Empêcher le cadre de changer de taille automatiquement

        self.button = NavireButton(self, navire_type, navire_length)
        self.button.pack(expand=True, fill=tk.BOTH)  # Remplir le cadre avec le bouton

class BatailleNavaleUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")
        self.grille_tirs = GrilleUI(self.master, "Tirs sur l'adversaire", 0)
        self.grille_navires_joueur = GrilleUI(self.master, "Navires du joueur", 1)

        # Création d'un cadre pour les boutons des navires du joueur
        self.navires_frame = tk.Frame(self.master)
        self.navires_frame.grid(row=1, column=1, padx=20, pady=20)

        self.create_navire_buttons()

    def create_navire_buttons(self):
        navires = Navires().navires_a_placer
        for navire_type, navire_length in navires.items():
            navire_frame = NavireFrame(self.navires_frame, navire_type, navire_length)
            navire_frame.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavaleUI(root)
    root.mainloop()
