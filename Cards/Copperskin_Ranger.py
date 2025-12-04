import random
from Helper_Classes import Unit,Board,Player

class Copperskin_Ranger(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        units: [Unit] = []
        for row in b.board:
            for cell in row:
                if cell is not None:
                    if cell.player != self.player and not cell.is_building:
                        units.append(cell)
        if units != []:
            rand = random.randint(0, len(units) - 1)
            units[rand].poisoned = True