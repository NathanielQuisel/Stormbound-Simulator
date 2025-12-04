import random
from Helper_Classes import Unit,Board,Player,Spell

class Kindreds_Grace(Spell):
    def __init__(self, player, x, y):
        super().__init__(player, x, y)
        self.target_type = "unit"
        self.target_player = player
        

    def on_play(self, player1: Player, player2: Player, b: Board):
        unit = b.board[self.y][self.x]
        unit.change_power(5)
        for u in Unit.all_units(Unit,self.b):
            if u.tribe == unit.tribe and u.player == unit.player:
                u.change_power(2)