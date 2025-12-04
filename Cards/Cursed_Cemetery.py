import random
from Helper_Classes import Unit,Board,Player

class Cursed_Cemetery(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)
        self.is_building = True

    def start_turn(self, player1: Player, player2: Player, b: Board):
        if self.x - 1 > -1 and not b.is_unit_at(self.x - 1, self.y):
            b.board[self.y][self.x - 1] = Unit(1, self.player, self.x - 1, self.y, "undead")
        if self.x + 1 < 4 and not b.is_unit_at(self.x + 1, self.y):
            b.board[self.y][self.x + 1] = Unit(1, self.player, self.x + 1, self.y, "undead")