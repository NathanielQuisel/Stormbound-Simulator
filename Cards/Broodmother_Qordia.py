import random
from Helper_Classes import Unit,Board,Player
from .Dragon_Egg import Dragon_Egg

class Broodmother_Qordia(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        good = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    pass
                if self.x + i < 4 and self.x + i > -1 and self.y + j < 5 and self.y + j > -1:
                    if b.board[self.y+j][self.x+i] is None:
                        good.append((self.x + i, self.y + j))
        count = 3
        while good != [] and count > 0:
            rand = random.randint(0, len(good) - 1)
            (x_cor, y_cor) = good[rand]
            b.board[y_cor][x_cor] = Dragon_Egg(1, self.player, x_cor, y_cor, "")
            good.remove((x_cor, y_cor))
            count -= 1