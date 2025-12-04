import random
from Helper_Classes import Unit,Board,Player

class Dreadfauns(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        good = []
        for (x_dir, y_dir) in directions:
            if self.x + x_dir < 0 or self.x + x_dir > 3 or self.y + y_dir < 0 or self.y + y_dir > 4:
                pass
            elif b.board[self.y + y_dir][self.x + x_dir] is None:
                good.append((x_dir, y_dir))

        count = 2
        while good != [] and count > 0:
            rand = random.randint(0, len(good) - 1)
            (x_dir, y_dir) = good[rand]
            b.board[self.y + y_dir][self.x + x_dir] = Unit(2, self.player, self.x + x_dir, self.y + y_dir, "satyr")
            if self.y + y_dir < player1.limit:
                player1.set_limit(self.y + y_dir)
            good.remove(good[rand])
            count -= 1