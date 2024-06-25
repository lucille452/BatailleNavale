from gui import BattleShipGUI
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.title("BattleShip Game")
    app = BattleShipGUI(root)
    root.mainloop()