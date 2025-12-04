import random
from Helper_Classes import Unit,Board,Player

class Crimson_Sentry(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_death(self, player1: Player, player2: Player, b: Board):
        units = self.adjacent_units(b)
        for unit in units:
            if not unit.is_building:
                unit.change_power(-1)
                unit.poisoned = True
                if unit.power <= 0:
                    b.board[unit.y][unit.x] = None
                    unit.on_death(player2, player1, b)