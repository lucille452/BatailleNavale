import numpy as np
from ai import AI

class Game:
    def __init__(self):
        self.board_size = 10
        self.ship_map = np.zeros((self.board_size, self.board_size), dtype=int)
        self.shot_map = np.zeros((self.board_size, self.board_size), dtype=int)
        self.ai = AI(self)
        self.ships = [(5, "porte-avions"), (4, "croiseur"), (3, "destroyer"), (3, "sous-marin"), (2, "torpilleur")]

    def start(self):
        self.place_ships()
        self.run_game()

    def place_ships(self):
        # Placeholder for ship placement logic
        for ship_size, _ in self.ships:
            self._place_ship_randomly(ship_size)
            
    def _place_ship_randomly(self, ship_size):
        # Simplified random placement logic
        placed = False
        while not placed:
            orientation = np.random.choice(["horizontal", "vertical"])
            row = np.random.randint(0, self.board_size)
            col = np.random.randint(0, self.board_size)
            if self._can_place_ship(row, col, ship_size, orientation):
                for i in range(ship_size):
                    if orientation == "horizontal":
                        self.ship_map[row, col + i] = 1
                    else:
                        self.ship_map[row + i, col] = 1
                placed = True


    def _can_place_ship(self, row, col, ship_size, orientation):
        if orientation == "horizontal":
            return col + ship_size <= self.board_size and np.all(self.ship_map[row, col:col + ship_size] == 0)
        else:
            return row + ship_size <= self.board_size and np.all(self.ship_map[row:row + ship_size, col] == 0)

    def run_game(self):
        game_over = False
        while not game_over:
            row, col = self.ai.make_move()
            result = self.check_move(row, col)
            if result == "hit":
                print(f"Hit at ({row}, {col})")
            elif result == "miss":
                print(f"Miss at ({row}, {col})")
            elif result == "sunk":
                print(f"Sunk at ({row}, {col})")
            game_over = self.check_game_over()

    def check_move(self, row, col):
        if self.ship_map[row][col] == 1:
            self.shot_map[row][col] = 1
            self.ship_map[row][col] = 0  # Mark ship part as hit
            if self.check_sunk(row, col):
                return "sunk"
            return "hit"
        else:
            self.shot_map[row][col] = -1
            return "miss"

    def check_sunk(self, row, col):
        # Check if any part of the ship remains in the surrounding cells
        return not np.any(self.ship_map == 1)

    def check_game_over(self):
        return np.all(self.ship_map == 0)