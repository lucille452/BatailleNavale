import tkinter as tk
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from game import Game


class AI:
    def __init__(self, game):
        self.game = game
        self.targets = []
        self.prob_map = np.zeros((game.board_size, game.board_size))
        self.history = np.zeros((game.board_size, game.board_size))
        self.df = pd.DataFrame(columns=['game', 'move', 'result'])
        self.weighted_map = self.create_weighted_map()

    def create_weighted_map(self):
        weighted_map = np.ones((self.game.board_size, self.game.board_size))
        for i in range(self.game.board_size):
            for j in range(self.game.board_size):
                if i == 0 or i == self.game.board_size - 1 or j == 0 or j == self.game.board_size - 1:
                    weighted_map[i][j] += 1  # Edges
                if (i == 0 or i == self.game.board_size - 1) and (j == 0 or j == self.game.board_size - 1):
                    weighted_map[i][j] += 1  # Corners
        return weighted_map

    def make_move(self):
        if not self.targets:
            guess_row, guess_col = self.guess_random()
        else:
            guess_row, guess_col = self.targets.pop()

        hit = self.game.check_hit(guess_row, guess_col)
        self.update_history((guess_row, guess_col), hit)
        if hit:
            self.add_adjacent_targets(guess_row, guess_col)

        return guess_row, guess_col

    def guess_random(self):
        flat_indices = np.argwhere(self.game.shot_map == 0)
        weighted_indices = [index for index in flat_indices if self.weighted_map[index[0], index[1]] > 1]
        if weighted_indices:
            guess_row, guess_col = random.choice(weighted_indices)
        else:
            guess_row, guess_col = random.choice(flat_indices)
        return guess_row, guess_col

    def add_adjacent_targets(self, guess_row, guess_col):
        potential_targets = [(guess_row + 1, guess_col), (guess_row, guess_col + 1),
                             (guess_row - 1, guess_col), (guess_row, guess_col - 1)]
        for target_row, target_col in potential_targets:
            if (0 <= target_row < self.game.board_size) and \
                    (0 <= target_col < self.game.board_size) and \
                    (self.game.shot_map[target_row][target_col] == 0) and \
                    ((target_row, target_col) not in self.targets):
                self.targets.append((target_row, target_col))

    def update_history(self, move, hit):
        self.df = self.df.append({'game': len(self.df) // 100, 'move': move, 'result': hit}, ignore_index=True)

    def analyze_history(self):
        game_outcomes = self.df.groupby('game')['result'].sum()
        plt.plot(game_outcomes)
        plt.title('AI Performance Over Time')
        plt.xlabel('Game')
        plt.ylabel('Hits')
        plt.show()

    def adjust_weighted_map(self):
        self.weighted_map += self.history / np.max(self.history)  # Normalize history to [0, 1]
