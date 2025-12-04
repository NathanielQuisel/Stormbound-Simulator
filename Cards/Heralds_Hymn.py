import random
from Helper_Classes import Unit,Board,Player,Spell

class Heralds_Hymn(Spell):
    def __init__(self, player, x, y):
        super().__init__(player, x, y)
        self.target_type = "unit"
        self.target_player = player
        

    def on_play(self, player1: Player, player2: Player, b: Board):
        unit = b.board[self.y][self.x]
        unit.change_power(2)
        for i in range(4):
            cell = b.board[self.y][i]
            if cell is not None:
                if cell.player == unit.player:
                    #this needs to be changed bc move_unit function within the Game class
                    self.move_unit(self.y, i, -1, 0)