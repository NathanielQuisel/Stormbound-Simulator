import random
from ..Helper_Classes import Unit,Board,Player,Spell

class Summon_Militia(Spell):
    def __init__(self, player):
        super().__init__(player)
        

    def on_play(self, player1: Player, player2: Player, b: Board):
        good = []
        for i in range(5):
            for j in range(4):
                if self.b.board[i][j] is None and i >= player1.limit:
                    good.append((i, j))
        if good != []:
            rand = random.randint(0, len(good) - 1)
            (y, x) = good[rand]
            b.board[y][x] = Unit(1, self.player, x, y, "knight")
