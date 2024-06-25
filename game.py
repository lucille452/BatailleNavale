import tkinter as tk
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ai import AI

class Game:
    def __init__(self, board_size=10):
        self.board_size = board_size
        self.ship_sizes = [2, 3, 3, 4, 5]
        self.ship_map = np.zeros((board_size, board_size), dtype=int)
        self.shot_map = np.zeros((board_size, board_size), dtype=int)
        self.ai = AI(self)

    def place_ships(self):
        for ship_size in self.ship_sizes:
            placed = False
            while not placed:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                horizontal = random.choice([True, False])
                if self.can_place_ship(row, col, ship_size, horizontal):
                    self.set_ship(row, col, ship_size, horizontal)
                    placed = True

    def can_place_ship(self, row, col, ship_size, horizontal):
        if horizontal:
            if col + ship_size > self.board_size:
                return False
            return np.all(self.ship_map[row, col:col + ship_size] == 0)
        else:
            if row + ship_size > self.board_size:
                return False
            return np.all(self.ship_map[row:row + ship_size, col] == 0)

    def set_ship(self, row, col, ship_size, horizontal):
        if horizontal:
            self.ship_map[row, col:col + ship_size] = 1
        else:
            self.ship_map[row:row + ship_size, col] = 1

    def check_hit(self, row, col):
        if self.ship_map[row, col] == 1:
            self.shot_map[row, col] = 1
            return True
        else:
            self.shot_map[row, col] = -1
            return False

    def is_game_over(self):
        return np.all(self.ship_map == self.shot_map)