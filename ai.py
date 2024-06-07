import random

class AI:
    def __init__(self, game):
        self.game = game
        self.targets = []

    def make_move(self):
        if not self.targets:
            guess_row, guess_col = self.guess_random()
        else:
            guess_row, guess_col = self.targets.pop()

        if self.game.ship_map[guess_row][guess_col] == 1:
            self.add_adjacent_targets(guess_row, guess_col)

        return guess_row, guess_col

    def guess_random(self):
        while True:
            guess_row = random.randint(0, self.game.board_size - 1)
            guess_col = random.randint(0, self.game.board_size - 1)
            if self.game.shot_map[guess_row][guess_col] == 0:
                break
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