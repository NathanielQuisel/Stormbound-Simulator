import random
from Helper_Classes import Unit,Board,Player

class First_Mutineer(Unit):
    def __init__(self, power, player, x, y, tribe):
        super().__init__(power, player, x, y, tribe)

    def on_play(self, player1: Player, player2: Player, b: Board):
        cards = []
        for card in player1.hand:
            if card.tribe != "pirate":
                cards.append(card)
        if cards != []:
            rand = random.randint(0, len(cards) - 1)
            player1.deck.add_card(cards[rand])
            player1.hand.remove(cards[rand])