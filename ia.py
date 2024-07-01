import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class IA:
    def __init__(self, board_size):
        self.board_size = board_size
        self.targets = []
        self.prob_map = np.zeros((board_size, board_size))
        self.history = np.zeros((board_size, board_size))
        self.df = pd.DataFrame(columns=['game', 'move', 'result'])
        self.weighted_map = self.create_weighted_map()
        self.shot_map = np.zeros((self.board_size, self.board_size))
        self.tir = []

    def create_weighted_map(self):
        size = self.board_size
        weighted_map = np.ones((size, size))
        weighted_map[0, :] += 1
        weighted_map[-1, :] += 1
        weighted_map[:, 0] += 1
        weighted_map[:, -1] += 1
        weighted_map[0, 0] += 1
        weighted_map[0, -1] += 1
        weighted_map[-1, 0] += 1
        weighted_map[-1, -1] += 1
        return weighted_map

    def make_move(self, hit):
        if not self.targets or not hit:
            guess_row, guess_col = self.guess_random2()
        else:
            guess_row, guess_col = self.targets.pop()

        self.update_history((guess_row, guess_col), hit)
        if hit:
            self.add_adjacent_targets(guess_row, guess_col)
            if self.targets:
                guess_row, guess_col = self.targets.pop()

        return guess_row, guess_col

    def guess_random(self):
        available_moves = np.argwhere(self.shot_map == 0)
        weighted_moves = [move for move in available_moves if self.weighted_map[tuple(move)] > 1]
        if weighted_moves:
            guess = random.choice(weighted_moves)
        else:
            guess = random.choice(available_moves)
        self.tir.append(tuple(guess))
        return tuple(guess)

    def guess_random2(self):
        available_moves = np.argwhere(self.shot_map == 0)
        if available_moves.size == 0:
            raise RuntimeError("No available moves left.")  # Handle no available moves scenario

        guess = random.choice(available_moves)
        self.tir.append(tuple(guess))
        return tuple(guess)

    def add_adjacent_targets(self, row, col):
        potential_targets = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for r, c in potential_targets:
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.shot_map[r, c] == 0:
                self.targets.append((r, c))
                self.update_shot_map((r, c))  # Mettre à jour la carte des tirs pour marquer cette case

    def update_shot_map(self, move):
        row, col = move
        self.shot_map[row, col] = 1

    def update_history(self, move, hit):
        new_row = pd.DataFrame({'game': [len(self.df) // 100], 'move': [move], 'result': [hit]})
        self.df = pd.concat([self.df, new_row], ignore_index=True)

    def analyze_history(self):
        hits_per_game = self.df.groupby('game')['result'].sum()
        plt.plot(hits_per_game)
        plt.title('AI Performance Over Time')
        plt.xlabel('Game')
        plt.ylabel('Hits')
        plt.show()
