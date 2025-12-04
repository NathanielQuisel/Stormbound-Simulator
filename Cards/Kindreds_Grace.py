import random
from Helper_Classes import Unit,Board,Player,Spell

class Kindreds_Grace(Spell):
    def __init__(self, player, x, y):
        super().__init__(player, x, y)
        
    def valid_play(self, b):
        return b.is_unit_at(self.x,self.y) and b.board[self.y][self.x].player == self.player

    def on_play(self, player1: Player, player2: Player, b: Board):
        unit = b.board[self.y][self.x]
        unit.change_power(5)
        for u in b.all_units():
            if u.tribe == unit.tribe and u.player == unit.player:
                u.change_power(2)