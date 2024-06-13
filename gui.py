import tkinter as tk
from tkinter import ttk, messagebox
from game import Game
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class BattleShipGUI:
    def __init__(self, master):
        self.master = master
        self.game = Game()
        self.game.place_ships()
        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.buttons = []
        for i in range(self.game.board_size):
            row = []
            for j in range(self.game.board_size):
                btn = tk.Button(self.master, text=' ', width=3, height=1, command=lambda i=i, j=j: self.on_click(i, j))
                btn.grid(row=i, column=j)
                row.append(btn)
            self.buttons.append(row)

    def on_click(self, row, col):
        if self.game.shot_map[row, col] == 0:
            hit = self.game.check_hit(row, col)
            self.update_button(row, col, hit)
            if self.game.is_game_over():
                self.end_game("You won!")
            else:
                ai_move = self.game.ai.make_move()
                self.update_button(ai_move[0], ai_move[1], self.game.check_hit(ai_move[0], ai_move[1]))
                if self.game.is_game_over():
                    self.end_game("AI won!")

    def update_button(self, row, col, hit):
        self.buttons[row][col].config(text='X' if hit else 'O', state='disabled')

    def update_board(self):
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if self.game.shot_map[i, j] == 1:
                    self.buttons[i][j].config(text='X', state='disabled')
                elif self.game.shot_map[i, j] == -1:
                    self.buttons[i][j].config(text='O', state='disabled')

    def end_game(self, message):
        for row in self.buttons:
            for btn in row:
                btn.config(state='disabled')
        print(message)
        self.game.ai.analyze_history()