from .Player import Player

class Unit:
    def __init__(self, power, player, x, y, tribe):
        self.power = power
        self.player = player
        self.x = x
        self.y = y
        self.tribe = tribe
        self.poisoned = False
        self.frozen = False
        self.confused = False
        self.vitalized = False
        self.is_building = False

    def change_power(self, amount):
        self.power += amount

    def set_coors(self, x, y):
        self.x = x
        self.y = y

    def start_turn(self, player1: Player, player2: Player, b):  # for buildings only
        return

    def on_play(self, player1: Player, player2: Player, b):
        return

    def before_move(self, player1: Player, player2: Player, b):
        return

    def after_move(self, player1: Player, player2: Player, b):
        return

    def on_attack(self, enemy, player1: Player, player2: Player, b):
        return

    def after_attack(self, player1: Player, player2: Player, b):
        return

    def on_death(self, player1: Player, player2: Player, b):
        return

    def on_survive(self, amount, player1: Player, player2: Player, b):
        return
