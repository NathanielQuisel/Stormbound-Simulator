import random
from Helper_Classes import Unit,Board,Player

class Moonlit_Aerie(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)
        self.is_building = True

    def start_turn(self, player1: Player, player2: Player, b: Board):
        units = b.all_units()
        good = []
        for unit in units:
            if unit.player == self.player and unit.tribe == "satyr":
                good.append(unit)
        for unit in good:
            unit.change_power(1)