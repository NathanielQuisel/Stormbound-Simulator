import random
from Helper_Classes import Unit,Board,Player

class Northsea_Dog(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        if player1.hand == []:
            self.change_power(6)