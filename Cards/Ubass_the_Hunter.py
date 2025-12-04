import random
from Helper_Classes import Unit,Board,Player

class Ubass_the_Hunter(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        units = b.surrounding_units(self.x,self.y)
        tribes = []
        for unit in units:
            if unit.tribe not in tribes and not unit.is_building:
                tribes.append(unit.tribe)
        enemies = []
        for row in b.board:
            for cell in row:
                if cell is not None:
                    if cell.player != self.player:
                        enemies.append(cell)
        num = len(tribes)
        while enemies != [] and num > 0:
            rand = random.randint(0, len(enemies) - 1)
            enemies[rand].change_power(-1)
            if enemies[rand].power <= 0:
                b.board[enemies[rand].y][enemies[rand].x] = None
                enemies[rand].on_death(player2, player1, b)
                enemies.remove(enemies[rand])
            num -= 1