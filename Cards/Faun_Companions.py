import random
from Helper_Classes import Unit,Board,Player

class Faun_Companions(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        units = b.adjacent_units(self.x,self.y)
        good = []
        for unit in units:
            if unit.player == self.player and unit.tribe == "satyr":
                good.append(unit)
        if good != []:
            rand = random.randint(0, len(good) - 1)
            good[rand].change_power(3)