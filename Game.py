import random
from typing import Optional

# y is first index, x is second, also top left is [0][0] for indexing, but for player bottom left is 0,0
class Game:
    def __init__(self, deck1: Deck, deck2: Deck):
        self.player1 = Player(deck1)
        self.player1.draw_hand()
        self.player2 = Player(deck2)
        self.player2.draw_hand()
        self.player2.inc_mana()
        self.cur_player = 1
        self.b: Board = Board()

    def display(self):
        self.b.display()
        self.player1.display()
        print()
        self.player2.display()
        print()

    def cycle(self, card_num):
        (player, _) = self.find_players()
        player.cycle(card_num)

    def find_players(self):
        if self.cur_player == 1:
            return self.player1, self.player2
        else:
            return self.player2, self.player1

    def check_spell(self, card_num):
        (player, _) = self.find_players()
        cost = player.hand[card_num].cost
        return cost <= player.remain_mana and player.hand[card_num].tribe == "spell"

    def check_play(self, card_num, x, y):
        (player, _) = self.find_players()
        cost = player.hand[card_num].cost
        return player.limit <= y and self.b.board[y][x] is None and cost <= player.remain_mana

    def check_single_target(self, x, y, player):
        if self.b.board[y][x] is not None:
            return player == 3 or (self.b.board[y][x].player == player and not self.b.board[y][x].is_building)

    def play(self, card_num, x, y):
        (player, enemy) = self.find_players()
        card: Card = player.hand[card_num]
        if self.check_spell(card_num):
            if card.name == "Summon_Militia":
                player.play_card(card_num)
                self.Summon_Militia(player)
            elif card.name == "Kindred's_Grace":
                if self.check_single_target(x, y, self.cur_player):
                    player.play_card(card_num)
                    self.Kindred_Grace(x, y)
            elif card.name == "Herald's_Hymn":
                if self.check_single_target(x, y, self.cur_player):
                    player.play_card(card_num)
                    self.Herald_Hymn(x, y)

        elif self.check_play(card_num, x, y):
            player.play_card(card_num)
            if card.name == "Generic":
                self.b.board[y][x] = Unit(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Copperskin_Ranger":
                self.b.board[y][x] = Copperskin_Ranger(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "First_Mutineer":
                self.b.board[y][x] = First_Mutineer(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Crimson_Sentry":
                self.b.board[y][x] = Crimson_Sentry(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Edrik_the_Fierce":
                self.b.board[y][x] = Edrik_the_Fierce(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Amberhides":
                self.b.board[y][x] = Amberhides(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Freebooters":
                self.b.board[y][x] = Freebooters(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Northsea_Dogs":
                self.b.board[y][x] = Northsea_Dog(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Siren_of_the_Seas":
                self.b.board[y][x] = Siren_of_the_Seas(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Ubass_the_Hunter":
                self.b.board[y][x] = Ubass_the_Hunter(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Vindictive_Wretches":
                self.b.board[y][x] = Vindictive_Wretches(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Dopplebocks":
                self.b.board[y][x] = Dopplebocks(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Counselor_Ahmi":
                self.b.board[y][x] = Counselor_Ahmi(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Faun_Companions":
                self.b.board[y][x] = Faun_Companions(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Swarmcallers":
                self.b.board[y][x] = Swarmcallers(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Dreadfauns":
                self.b.board[y][x] = Dreadfauns(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Bucks_of_Wasteland":
                self.b.board[y][x] = Bucks_of_Wasteland(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Broodmother_Qordia":
                self.b.board[y][x] = Broodmother_Qordia(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Moonlit_Aerie":
                self.b.board[y][x] = Moonlit_Aerie(card.power, self.cur_player, x, y, card.tribe)
            elif card.name == "Cursed_Cemetery":
                self.b.board[y][x] = Cursed_Cemetery(card.power, self.cur_player, x, y, card.tribe)

            unit: Unit = self.b.board[y][x]
            directions = self.find_move_path(y, x, card.move)
            unit.on_play(player, enemy, self.b)
            for (x_dir, y_dir) in directions:
                if unit.power <= 0:
                    return
                self.move_unit(unit.y, unit.x, y_dir, x_dir)

    def reverse_board(self):
        temp = [[None for _ in range(4)] for _ in range(5)]
        for i in range(5):
            for j in range(4):
                temp[i][j] = self.b.board[4 - i][3 - j]
                if self.b.board[4 - i][3 - j] is not None:
                    self.b.board[4 - i][3 - j].set_coors(j, i)
        self.b.board = temp

    def find_move_dir(self, y, x, temp: Board):
        if y - 1 < 0:
            return (0, -1)
        if temp.board[y - 1][x] is not None:
            if temp.board[y - 1][x].player != self.cur_player:
                return (0, -1)
        if x != 0:
            if temp.board[y][x - 1] is not None:
                if temp.board[y][x - 1].player != self.cur_player:
                    return (-1, 0)
        if x != 3:
            if temp.board[y][x + 1] is not None:
                if temp.board[y][x + 1].player != self.cur_player:
                    return (1, 0)
        return (0, -1)

    def find_move_path(self, y, x, move):
        temp: Board = Board()
        for i in range(5):
            for j in range(4):
                temp.board[i][j] = self.b.board[i][j]
        moves = []
        while move > 0 and y > 0:
            (x_dir, y_dir) = self.find_move_dir(y, x, temp)
            moves.append((x_dir, y_dir))
            x += x_dir
            y += y_dir
            temp.board[y][x] = None
            move -= 1
        return moves

    def move_unit(self, y, x, y_dir, x_dir):
        unit: Optional[Unit] = self.b.board[y][x]
        power = unit.power
        (player, enemy) = self.find_players()
        row = y + y_dir
        col = x + x_dir
        if row < 0:  # only happens forward
            if unit.vitalized:
                unit.change_power(1)
            unit.on_attack(None, player, enemy, self.b)
            unit.before_move(player, enemy, self.b)
            self.b.board[y][x] = None
            player.change_life(-power)
            unit.change_power(-power)
            unit.on_death(player, enemy, self.b)
            return

        ahead: Optional[Unit] = self.b.board[row][col]
        if ahead is None:  # only happens when moving forward
            unit.before_move(player, enemy, self.b)
            self.b.board[y][x] = None
            self.b.board[row][col] = unit
            unit.set_coors(col, row)
            unit.after_move(player, enemy, self.b)
            self.simple_set_limit(row)
        elif ahead.player == self.cur_player:  # only happens when moving forward
            return
        else:  # omnidirectional
            unit.on_attack(ahead, player, enemy, self.b)
            unit.before_move(player, enemy, self.b)
            if power > ahead.power:
                unit.change_power(-ahead.power)
                self.b.board[row][col] = None
                ahead.change_power(-ahead.power)
                ahead.on_death(enemy, player, self.b)
                self.b.board[row][col] = unit
                unit.on_survive(ahead.power, player, enemy, self.b)
                self.b.board[y][x] = None
                unit.set_coors(col, row)
                unit.after_move(player, enemy, self.b)
                unit.after_attack(player, enemy, self.b)
                self.simple_set_limit(row)
            elif ahead.power > power:
                ahead.change_power(-power)
                self.b.board[y][x] = None
                unit.change_power(-power)
                unit.on_death(player, enemy, self.b)
                ahead.on_survive(power, enemy, player, self.b)
            else:
                self.b.board[row][col] = None
                self.b.board[y][x] = None
                ahead.change_power(-ahead.power)
                unit.change_power(-power)
                ahead.on_death(enemy, player, self.b)
                unit.on_death(player, enemy, self.b)

    def advance_units(self):
        (player, enemy) = self.find_players()
        for i in range(5):
            for j in range(4):
                unit: Optional[Unit] = self.b.board[i][j]
                if unit is not None:
                    if not unit.is_building:
                        if unit.player == self.cur_player:
                            if unit.frozen:
                                unit.frozen = False
                            elif unit.vitalized:
                                unit.change_power(1)
                                self.move_unit(i, j, -1, 0)
                            elif unit.poisoned:
                                unit.change_power(-1)
                                if unit.power <= 0:
                                    self.b.board[unit.y][unit.x] = None
                                    unit.on_death(player, enemy, self.b)
                                else:
                                    self.move_unit(i, j, -1, 0)
                            else:
                                self.move_unit(i, j, -1, 0)

    def trigger_buildings(self):
        (player, enemy) = self.find_players()
        for i in range(5):
            for j in range(4):
                unit: Optional[Unit] = self.b.board[i][j]
                if unit is not None:
                    if unit.is_building and unit.player == self.cur_player:
                        unit.start_turn(player, enemy, self.b)

    def set_p_limit(self):
        greatest = 4
        for i in range(5):
            for j in range(4):
                unit: Optional[Unit] = self.b.board[i][j]
                if unit is not None:
                    if unit.player == self.cur_player and i < greatest and i != 0:
                        greatest = i
                    if unit.player == self.cur_player and i == 0:
                        greatest = 1
        if self.cur_player == 1:
            self.player1.set_limit(greatest)
        else:
            self.player2.set_limit(greatest)

    def simple_set_limit(self, y):
        (player, _) = self.find_players()
        if y < player.limit and y != 0:
            player.set_limit(y)

    def end_turn(self):
        (player, _) = self.find_players()
        player.end_turn()
        self.reverse_board()
        self.cur_player = self.cur_player % 2 + 1
        self.trigger_buildings()
        self.advance_units()
        self.set_p_limit()

    def Summon_Militia(self, player: Player):
        good = []
        for i in range(5):
            for j in range(4):
                if self.b.board[i][j] is None and i >= player.limit:
                    good.append((i, j))
        if good != []:
            rand = random.randint(0, len(good) - 1)
            (y, x) = good[rand]
            self.b.board[y][x] = Unit(1, self.cur_player, x, y, "knight")

    def Kindred_Grace(self, x, y):
        unit = self.b.board[y][x]
        unit.change_power(5)
        for u in Unit.all_units(Unit,self.b):
            if u.tribe == unit.tribe and u.player == unit.player:
                u.change_power(2)

    def Herald_Hymn(self, x, y):
        unit = self.b.board[y][x]
        unit.change_power(2)
        for i in range(4):
            cell = self.b.board[y][i]
            if cell is not None:
                if cell.player == unit.player:
                    self.move_unit(y, i, -1, 0)


def run():
    # Card(cost,power,move,tribe,name)
    deck: Deck = Deck()
    deck.add_card(Card(1, 0, 0, "spell", "Summon_Militia"))
    deck.add_card(Card(6, 4, 1, "dragon", "Broodmother_Qordia"))
    deck.add_card(Card(4, 3, 0, "knight", "Edrik_the_Fierce"))
    deck.add_card(Card(3, 1, 2, "pirate", "First_Mutineer"))
    deck.add_card(Card(2, 1, 0, "pirate", "Northsea_Dogs"))
    deck.add_card(Card(1, 6, 3, "hero", "Siren_of_the_Seas"))
    deck.add_card(Card(3, 2, 0, "pirate", "Freebooters"))
    deck.add_card(Card(2, 1, 0, "toad", "Copperskin_Ranger"))
    deck.add_card(Card(5, 4, 1, "toad", "Amberhides"))
    deck.add_card(Card(3, 1, 2, "toad", "Crimson_Sentry"))
    deck.add_card(Card(5, 5, 0, "hero", "Ubass_the_Hunter"))
    deck.add_card(Card(3, 3, 1, "pirate", "Generic"))
    # deck.shuffle()
    deck1: Deck = Deck()

    deck1.add_card(Card(2, 1, 0, "satyr", "Dopplebocks"))
    deck1.add_card(Card(3, 3, 0, "", "Moonlit_Aerie"))
    deck1.add_card(Card(4, 3, 0, "", "Cursed_Cemetery"))
    deck1.add_card(Card(6, 0, 0, "spell", "Kindred's_Grace"))
    deck1.add_card(Card(7, 0, 0, "spell", "Herald's_Hymn"))
    deck1.add_card(Card(3, 1, 1, "satyr", "Counselor_Ahmi"))
    deck1.add_card(Card(3, 2, 1, "satyr", "Faun_Companions"))
    deck1.add_card(Card(3, 1, 1, "satyr", "Swarmcallers"))
    deck1.add_card(Card(5, 3, 0, "satyr", "Dreadfauns"))
    deck1.add_card(Card(6, 6, 0, "satyr", "Bucks_of_Wasteland"))
    deck1.add_card(Card(3, 4, 0, "satyr", "Generic"))
    deck1.add_card(Card(2, 2, 0, "satyr", "Generic"))
    # deck1.shuffle()
    g = Game(deck, deck1)

run()
