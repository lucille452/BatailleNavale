import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class AI:
    def __init__(self, game):
        self.game = game
        self.targets = []
        self.prob_map = np.zeros((game.board_size, game.board_size))
        self.history = np.zeros((game.board_size, game.board_size))
        self.df = pd.DataFrame(columns=['game', 'move', 'result'])
        self.weighted_map = self.create_weighted_map()

    #Crée une carte pondérée pour prioriser les bords et les coins du plateau de jeu.
    def create_weighted_map(self):
        size = self.game.board_size
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

    #Si l'IA n'a pas de cibles, elle fait un mouvement aléatoire. Sinon, elle attaque les cibles adjacentes.
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

    #Sélectionne un mouvement aléatoire parmi ceux disponibles, avec une préférence pour les positions pondérées.
    def guess_random(self):
        available_moves = np.argwhere(self.game.shot_map == 0)
        weighted_moves = [move for move in available_moves if self.weighted_map[tuple(move)] > 1]
        if weighted_moves:
            guess = random.choice(weighted_moves)
        else:
            guess = random.choice(available_moves)
        return tuple(guess)

    #Ajoute les cases adjacentes d'un coup réussi à la liste des cibles
    def add_adjacent_targets(self, row, col):
        potential_targets = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        self.targets.extend(
            (r, c) for r, c in potential_targets
            if 0 <= r < self.game.board_size and 0 <= c < self.game.board_size and self.game.shot_map[r, c] == 0
        )

    #Enregistre chaque mouvement et son résultat dans un DataFrame pour analyse ultérieure.
    def update_history(self, move, hit):
        self.df = self.df.append({'game': len(self.df) // 100, 'move': move, 'result': hit}, ignore_index=True)

    #Génère un graphique des performances de l'IA au fil des jeux
    def analyze_history(self):
        hits_per_game = self.df.groupby('game')['result'].sum()
        plt.plot(hits_per_game)
        plt.title('AI Performance Over Time')
        plt.xlabel('Game')
        plt.ylabel('Hits')
        plt.show()
