import random
from ..Helper_Classes import Unit,Board,Player

class Siren_of_the_Seas(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_attack(self, enemy, player1: Player, player2: Player, b: Board):
        if enemy is not None:
            if enemy.power > 3 and not enemy.is_building:
                enemy.change_power(3 - enemy.power)