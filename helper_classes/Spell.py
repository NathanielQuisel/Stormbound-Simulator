from .Board import Board
from .Player import Player

class Spell:
    target_type = None #this is just used for AI training to not add too many copies of essentially
    # the same action within Game.get_legal_actions

    def __init__(self, player, x=-1, y=-1):
        self.player = player #this is an int, representing the player who controls the spell
        self.x = x
        self.y = y
    
    def valid_play(self, b: Board): #returns boolean
        # each spell responsible for overwriting this function
        return True
    
    def on_play(self, player1: Player, player2: Player, b: Board):
        return
