import random
from .Card import Card

class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            num = random.randint(0, i)
            self.cards[i], self.cards[num] = self.cards[num], self.cards[i]

    def draw(self) -> Card:
        return self.cards.pop(0)