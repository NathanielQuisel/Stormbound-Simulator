import random
from ..Helper_Classes import Unit,Board,Player

class Bucks_of_Wasteland(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_survive(self, amount, player1: Player, player2: Player, b: Board):
        units = self.all_units(b)
        units.remove(self)
        good = []
        for unit in units:
            if unit.player == self.player and not unit.is_building:
                good.append(unit)
        count = 2
        while good != [] and count > 0:
            rand = random.randint(0, len(good) - 1)
            good[rand].change_power(amount)
            good.remove(good[rand])
            count -= 1