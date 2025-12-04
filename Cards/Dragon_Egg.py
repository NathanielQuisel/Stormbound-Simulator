import random
from Helper_Classes import Unit,Board,Player

class Dragon_Egg(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)
        self.is_building = True

    def start_turn(self, player1: Player, player2: Player, b: Board):
        b.board[self.y][self.x] = Unit(2, self.player, self.x, self.y, "dragon")