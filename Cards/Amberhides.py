import random
from Helper_Classes import Unit,Board,Player


class Amberhides(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        units = b.surrounding_units(self.x,self.y)
        good = []
        for unit in units:
            if unit.poisoned:
                good.append(unit)
        if good != []:
            rand = random.randint(0, len(good) - 1)
            enemy = good[rand]
            if enemy.power <= 4:
                self.change_power(enemy.power)
                enemy.change_power(enemy.power)
                b.board[enemy.y][enemy.x] = None
                if enemy.player == self.player:
                    enemy.on_death(player1, player2, b)
                else:
                    enemy.on_death(player2, player1, b)
            else:
                self.change_power(4)
                enemy.change_power(-4)