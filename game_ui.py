import tkinter as tk
from tkinter import ttk, messagebox
import random

class Grille:
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

class NavireWidget(tk.Frame):
    def __init__(self, master, navire_type, navire_length):
        tk.Frame.__init__(self, master)
        self.navire_type = navire_type
        self.navire_length = navire_length
        self.configure(width=100, height=35)
        self.pack_propagate(False)

        self.button = tk.Button(self, text=f"{navire_type} ({navire_length})", width=15, height=1, bg='darkgray', fg='black', font=('Roboto', 10))
        self.button.configure(command=self.place_ship)
        self.button.pack(expand=True, fill=tk.BOTH)

    def place_ship(self):
        print(f"Vous avez sélectionné le {self.navire_type} ({self.navire_length})")
        # Vous pouvez ajouter ici le code pour placer le navire sur la grille de jeu.

class JoueurNavires(Navires):
    def __init__(self):
        super().__init__()

class AdversaireNavires(Navires):
    def __init__(self):
        super().__init__()

class NaviresManager:
    @staticmethod
    def create_navire_buttons(parent_frame):
        navires = JoueurNavires().navires_a_placer
        for navire_type, navire_length in navires.items():
            navire_widget = NavireWidget(parent_frame, navire_type, navire_length)
            navire_widget.pack(pady=5)

class GameStateManager:
    @staticmethod
    def update_navires_restants(label, navires_restants):
        label.config(text=f"Navires restants: {navires_restants}")

    @staticmethod
    def update_tirs_reussis(label, tirs_reussis):
        label.config(text=f"Tirs réussis: {tirs_reussis}")

class BatailleNavale:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")
        
        # Création des grilles
        self.grille_tirs = Grille(self.master, "Tirs sur l'adversaire", 0)
        self.grille_navires_joueur = Grille(self.master, "Navires du joueur", 1)

        # Création d'un cadre pour les boutons des navires du joueur
        self.navires_frame = tk.Frame(self.master)
        self.navires_frame.grid(row=1, column=1, padx=20, pady=20)

        NaviresManager.create_navire_buttons(self.navires_frame)

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

    def update_navires_restants_joueur(self, navires_restants):
        GameStateManager.update_navires_restants(self.navires_restants_joueur_label, navires_restants)

    def update_navires_restants_adversaire(self, navires_restants):
        GameStateManager.update_navires_restants(self.navires_restants_adversaire_label, navires_restants)

    def update_tirs_reussis(self, tirs_reussis):
        GameStateManager.update_tirs_reussis(self.tirs_reussis_label, tirs_reussis)

if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
