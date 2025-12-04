from .Board import Board
from .Player import Player

class Unit:
    def __init__(self, power, player, x, y, tribe):
        self.power = power
        self.player = player
        self.x = x
        self.y = y
        self.tribe = tribe
        self.poisoned = False
        self.frozen = False
        self.confused = False
        self.vitalized = False
        self.is_building = False

    def change_power(self, amount):
        self.power += amount

    def set_coors(self, x, y):
        self.x = x
        self.y = y

    #these functions should really belong in the Board class
    def is_unit_at(self, x, y, b: Board):
        # returns false if out of bounds
        # returns false if something is not there
        if x > 3 or x < 0 or y > 4 or y < 0:
            return False
        return b.board[y][x] is not None

    def adjacent_units(self, b: Board):
        units = []
        if self.is_unit_at(self.x - 1, self.y, b):
            units.append(b.board[self.y][self.x - 1])
        if self.is_unit_at(self.x + 1, self.y, b):
            units.append(b.board[self.y][self.x + 1])
        if self.is_unit_at(self.x, self.y - 1, b):
            units.append(b.board[self.y - 1][self.x])
        if self.is_unit_at(self.x, self.y + 1, b):
            units.append(b.board[self.y + 1][self.x])
        return units

    def surrounding_units(self, b: Board):
        units = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (i != 0 or j != 0) and self.is_unit_at(self.x + j, self.y + i, b):
                    units.append(b.board[self.y + i][self.x + j])
        return units

    def all_units(self, b: Board):
        units = []
        for row in b.board:
            for cell in row:
                if cell is not None:
                    units.append(cell)
        return units

    def start_turn(self, player1: Player, player2: Player, b: Board):  # for buildings only
        return

    def on_play(self, player1: Player, player2: Player, b: Board):
        return

    def before_move(self, player1: Player, player2: Player, b: Board):
        return

    def after_move(self, player1: Player, player2: Player, b: Board):
        return

    def on_attack(self, enemy, player1: Player, player2: Player, b: Board):
        return

    def after_attack(self, player1: Player, player2: Player, b: Board):
        return

    def on_death(self, player1: Player, player2: Player, b: Board):
        return

    def on_survive(self, amount, player1: Player, player2: Player, b: Board):
        return
