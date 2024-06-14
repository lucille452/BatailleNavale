import tkinter as tk
from Game import Game


# Classe pour créer et gérer une grille de jeu
class Grille:
    def __init__(self, parent, label_text, row_offset):
        self.buttons = None
        self.frame = None
        self.parent = parent
        self.label_text = label_text
        self.row_offset = row_offset
        self.create_grille()

    # Méthode pour créer la grille
    def create_grille(self):
        self.frame = tk.Frame(self.parent)
        self.frame.grid(row=self.row_offset, column=0, padx=20, pady=20)

        # Ajout d'un label au-dessus de la grille
        tk.Label(self.frame, text=self.label_text).grid(row=0, columnspan=11)

        # Ajout des étiquettes pour les colonnes (A-J)
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for col, letter in enumerate(letters):
            tk.Label(self.frame, text=letter).grid(row=1, column=col + 1)

        # Ajout des étiquettes pour les lignes (1-10)
        for row in range(10):
            tk.Label(self.frame, text=str(row + 1)).grid(row=row + 2, column=0)

        # Création des boutons de la grille
        self.buttons = [
            [tk.Button(self.frame, text=' ', width=2, height=1, bg='light blue').grid(row=row + 2, column=col + 1)
             for col in range(10)] for row in range(10)]


# Classe pour gérer les navires à placer
class Navires:
    def __init__(self):
        self.navires_a_placer = {
            "Porte-avions": 5,
            "Cuirassé": 4,
            "Destroyer": 3,
            "Sous-marin": 3,
            "Patrouilleur": 2
        }


# Widget pour chaque navire
class NavireWidget(tk.Frame):
    def __init__(self, master, navire_type, navire_length):
        super().__init__(master, width=100, height=35)
        self.navire_type = navire_type
        self.navire_length = navire_length
        self.pack_propagate(False)
        self.button = tk.Button(self, text=f"{navire_type} ({navire_length})", width=15, height=1, bg='darkgray',
                                fg='black', font=('Roboto', 10), command=self.place_ship)
        self.button.pack(expand=True, fill=tk.BOTH)

    # Méthode appelée lors de la sélection d'un navire
    def place_ship(self):
        print(f"Vous avez sélectionné le {self.navire_type} ({self.navire_length})")
        # Vous pouvez ajouter ici le code pour placer le navire sur la grille de jeu.


# Classe pour gérer les navires du joueur
class NaviresManager:
    @staticmethod
    def create_navire_buttons(parent_frame):
        navires = Navires().navires_a_placer
        for navire_type, navire_length in navires.items():
            NavireWidget(parent_frame, navire_type, navire_length).pack(pady=5)


# Classe pour gérer l'état du jeu
class GameStateManager:
    @staticmethod
    def update_label(label, text):
        label.config(text=text)


# Classe principale pour la gestion du jeu
class BatailleNavale:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")

        # Création des grilles visuelles
        self.grille_tirs = Grille(self.master, "Tirs sur l'adversaire", 0)
        self.grille_navires_joueur = Grille(self.master, "Navires du joueur", 1)

        # création des joueurs / grilles / navires back
        self.game = Game()
        self.game.get_ia().get_grille_tirs().get_grille()

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

    # Méthodes pour mettre à jour les informations sur l'état du jeu
    def update_navires_restants_joueur(self, navires_restants):
        GameStateManager.update_label(self.navires_restants_joueur_label, f"Navires restants: {navires_restants}")

    def update_navires_restants_adversaire(self, navires_restants):
        GameStateManager.update_label(self.navires_restants_adversaire_label, f"Navires restants: {navires_restants}")

    def update_tirs_reussis(self, tirs_reussis):
        GameStateManager.update_label(self.tirs_reussis_label, f"Tirs réussis: {tirs_reussis}")


if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavale(root)
    root.mainloop()
