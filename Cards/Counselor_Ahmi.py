import random
from ..Helper_Classes import Unit,Board,Player,Card

class Counselor_Ahmi(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        check = True
        for unit in self.surrounding_units(b):
            check = check and unit.is_building
        player1.deck.cards.pop(len(player1.deck.cards) - 1)
        if check:
            player1.hand.append(Card(3, self.power + 1, 1, "satyr", "Counselor_Ahmi"))
        else:
            player1.deck.add_card(Card(3, 1, 1, "satyr", "Counselor_Ahmi"))
            # player1.deck.cards.remove(Card(3, self.power, 1, "satyr", "Counselor_Ahmi"))