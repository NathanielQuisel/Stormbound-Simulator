import random
from Helper_Classes import Unit,Board,Player

class Swarmcallers(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        for unit in self.adjacent_units(b):
            if unit.tribe == "satyr" and self.player == unit.player:
                self.change_power(2)