import random
from ..Helper_Classes import Unit,Board,Player

class Dopplebocks(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        if b.board[self.y - 1][self.x] is None:
            b.board[self.y - 1][self.x] = Unit(1, self.player, self.y - 1, self.x, "satyr")
            if player1.limit > self.y - 1:
                player1.set_limit(self.y - 1)