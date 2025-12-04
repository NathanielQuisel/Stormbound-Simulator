from .Deck import Deck

class Player:
    def __init__(self, deck: Deck):
        self.hand = []
        self.can_cycle = True
        self.deck = deck
        self.limit = 4
        self.life = 10
        self.max_mana = 3
        self.remain_mana = 3

    def display(self):
        for card in self.hand:
            print(card.power, card.move, card.cost, card.name)

    def draw(self):
        self.hand.append(self.deck.draw())

    def draw_hand(self):
        while len(self.hand) < 4:
            self.draw()

    def cycle(self, card_num):
        if self.can_cycle:
            self.deck.add_card(self.hand[card_num])
            self.hand.remove(self.hand[card_num])
            self.draw()
            self.can_cycle = False

    def set_limit(self, row):
        self.limit = row

    def change_life(self, amount):
        # negative to decrease
        self.life += amount

    def inc_mana(self):
        self.max_mana += 1
        self.remain_mana = self.max_mana

    def play_card(self, card_num):
        card = self.hand[card_num]
        self.remain_mana -= card.cost
        self.hand.remove(card)
        self.deck.cards.append(card)

    def end_turn(self):
        self.draw_hand()
        self.inc_mana()
        self.can_cycle = True