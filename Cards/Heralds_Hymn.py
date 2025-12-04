import random
from Helper_Classes import Unit,Board,Player,Spell

class Heralds_Hymn(Spell):
    def __init__(self, player, x, y):
        super().__init__(player, x, y)

    def valid_play(self, b):
        return b.is_unit_at(self.x,self.y) and b.board[self.y][self.x].player == self.player
        
    def on_play(self, player1: Player, player2: Player, b: Board):
        unit = b.board[self.y][self.x]
        unit.change_power(2)
        for i in range(4):
            cell = b.board[self.y][i]
            if cell is not None:
                if cell.player == unit.player:
                    #this needs to be changed bc move_unit function within the Game class
                    b.move_unit(unit.player, player1, player2, self.y, i, -1, 0)