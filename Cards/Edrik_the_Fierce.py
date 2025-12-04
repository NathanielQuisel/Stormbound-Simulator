import random
from Helper_Classes import Unit,Board,Player

class Edrik_the_Fierce(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        units = b.surrounding_units(self.x,self.y)
        for unit in units:
            if unit.player != self.player and (
            not b.is_unit_at(unit.x, unit.y + 1)) and unit.y < 4 and not unit.is_building:
                b.board[unit.y + 1][unit.x] = Unit(2, self.player, unit.x, unit.y + 1)