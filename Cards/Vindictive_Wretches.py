import random
from typing import Optional
from ..Helper_Classes import Unit,Board,Player

class Vindictive_Wretches(Unit):  # has not been tested in a bit/updated
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_death(self, player1: Player, player2: Player, b: Board):
        units: [(int, int)] = []
        lowest = 2
        for i in range(5):
            for j in range(4):
                cell: Optional[Unit] = b.board[i][j]
                if cell is not None:
                    if cell.player != self.player and cell.power <= lowest:
                        if cell.power < lowest:
                            units.clear()
                            lowest = cell.power
                            units.append((i, j))
                        else:
                            units.append((i, j))
        if units != []:
            remove = random.randint(0, len(units) - 1)
            (y, x) = units[remove]
            unit: Unit = b.board[y][x]
            b.board[y][x] = None
            unit.change_power(-unit.power)
            unit.on_death(player2, player1, b)