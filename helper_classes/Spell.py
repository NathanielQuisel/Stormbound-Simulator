from .Board import Board
from .Player import Player

class Spell:
    # target_type = None #for each spell that targets something, make sure to define if it targets a
    # #friendly or enemy unit and whether or not it targets a specific type of unit
    # target_player = None

    def __init__(self, player, x=-1, y=-1):
        self.player = player #this is an int, representing the player who controls the spell
        self.x = x
        self.y = y
    
    def valid_play(self, b: Board): #returns boolean
        # each spell responsible for overwriting this function
        return True
    
        # if self.x == -1: #for spells without a target, just put x=-1 and it will be valid
        #     return True
        # cell = b.board[self.x][self.y]
        # #make sure this if statement works
        # return cell is not None and cell.player == self.target_player and (cell.tribe == self.target_type or (cell.tribe != "building" and self.target_type == "unit"))

    def on_play(self, player1: Player, player2: Player, b: Board):
        return
