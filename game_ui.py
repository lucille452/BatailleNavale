import tkinter as tk
from tkinter import ttk, messagebox
from game_logic import BatailleNavaleGame  # Import sans l'extension .py

class BatailleNavaleUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bataille Navale")
        self.game = BatailleNavaleGame()
        self.create_grilles()

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
        self.game.toggle_place_navires_mode()
        if self.game.place_navires_mode:
            messagebox.showinfo("Placement de Navires", "Cliquez sur la grille pour placer vos navires.")
            # Mettre à jour les options de la combobox
            self.update_navire_combobox()
        else:
            messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")

    def update_navire_combobox(self):
        self.navire_combobox['values'] = self.game.update_navire_combobox()
        self.navire_var.set('')

    def on_button_click(self, parent, row, col):
        if self.game.place_navires_mode and parent == self.navires_joueur_frame:
            self.place_navire(parent, row, col)
        elif parent == self.tir_frame:
            self.tirer(row, col)
            self.adversaire_tirer()  # L'IA tire après le joueur

    def place_navire(self, parent, row, col):
        navire_selectionne = self.navire_var.get()
        if not navire_selectionne:
            messagebox.showinfo("Placement", "Veuillez sélectionner un navire à placer.")
            return

        taille = next((item[0] for item in self.game.navires_a_placer if item[1] == navire_selectionne), None)
        if taille is None:
            messagebox.showinfo("Placement", "Navire sélectionné non valide.")
            return

        success, message = self.game.place_navire(row, col, navire_selectionne)
        if success:
            orientation = self.orientation_var.get()
            if orientation == "horizontal":
                for i in range(taille):
                    button = parent.grid_slaves(row=row + 2, column=col + i + 1)[0]
                    button.config(bg="grey")
                    button.config(state="disabled")
            else:  # Vertical
                for i in range(taille):
                    button = parent.grid_slaves(row=row + i + 2, column=col + 1)[0]
                    button.config(bg="grey")
                    button.config(state="disabled")
            self.update_navire_combobox()  # Mettre à jour les options de la combobox
            if not self.game.navires_a_placer:
                self.game.place_navires_mode = False
                messagebox.showinfo("Fin du Placement", "Tous les navires ont été placés.")
                self.place_navires_button.config(state="disabled")
        else:
            messagebox.showinfo("Placement", message)

    def tirer(self, row, col):
        success, message = self.game.tirer(row, col)
        if success:
            button = self.tir_buttons[row][col]
            if message == "Touché !":
                button.config(bg="red")
            else:
                button.config(bg="white")
            messagebox.showinfo("Tir", message)

    def adversaire_tirer(self):
        row, col, message = self.game.adversaire_tirer()
        button = self.navires_joueur_buttons[row][col]
        if "touché" in message:
            button.config(bg="red")
        else:
            button.config(bg="white")
        messagebox.showinfo("Alerte", f"L'adversaire a tiré en ({row + 1}, {chr(ord('A') + col)}) et a {message.lower()}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BatailleNavaleUI(root)
    root.mainloop()
