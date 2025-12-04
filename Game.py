import random
import copy
import numpy as np
from typing import List, Tuple, Dict, Optional, Union
from Helper_Classes import Deck,Player,Board,Unit,Card,Spell
import Cards

Coord      = Tuple[int, int]          # (x, y) board position
PlayAction = Tuple[int, Coord]        # (card_idx, (x, y))
CycleAction= Tuple[int]               # (card_idx,)  — cycle a card
PassAction = Tuple[()]                # ()           — end turn
Action     = Union[PlayAction, CycleAction, PassAction]

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

    #returns true if card_num is a spell and player has the mana to play it
    def check_spell(self, card_num):
        (player, _) = self.find_players()
        cost = player.hand[card_num].cost
        return cost <= player.remain_mana and player.hand[card_num].tribe == "spell"

    def check_play(self, card_num, x, y):
        (player, _) = self.find_players()
        cost = player.hand[card_num].cost
        return player.limit <= y and self.b.board[y][x] is None and cost <= player.remain_mana

    #currently only checks if the thing is a unit and is owned by the active player
    #will need to change for spells that target enemies or buildings
    def check_single_target(self, x, y, player):
        if self.b.board[y][x] is not None:
            return player == 3 or (self.b.board[y][x].player == player and not self.b.board[y][x].is_building)

    def play(self, card_num, x, y):
        (player, enemy) = self.find_players()
        card: Card = player.hand[card_num]
        if self.check_spell(card_num):
            spell = getattr(Cards, card.name, Spell) (self.cur_player,x,y)
            if spell.valid_play(self.b):
                player.play_card(card_num)
                spell.on_play(player,enemy, self.b)

        elif self.check_play(card_num, x, y):
            player.play_card(card_num)
            if card.name == "Generic":
                self.b.board[y][x] = Unit(card.power, self.cur_player, x, y, card.tribe)
            else:
                self.b.board[y][x] = getattr(Cards, card.name, Unit)(
                    card.power, self.cur_player, x, y, card.tribe
                )

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
        (player, enemy) = self.find_players()
        self.b.move_unit(self.cur_player, player,enemy,y,x,y_dir,x_dir)

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

    def end_turn(self):
        (player, _) = self.find_players()
        player.end_turn()
        self.reverse_board()
        self.cur_player = self.cur_player % 2 + 1
        self.trigger_buildings()
        self.advance_units()
        self.set_p_limit()

    
    def _flatten_board(board) -> np.ndarray:
        """
        Encode the 5×4 board into a vector of ints.

        Each cell → 0 (empty) | ±pow   (sign = owner)  | 100+   for buildings.
        Feel free to swap in one-hot or more elaborate encodings later.
        """
        #need to change the above encodings to manage buildings better
        #buildings will need to also represent their power, that they are a building,
        #and who owns them

        #also units will need to represent what unit type they are and what active abilities they have
        vec = np.zeros(5 * 4, dtype=np.int16)
        k = 0
        for y in range(5):
            for x in range(4):
                unit = board[y][x]
                if unit is None:
                    vec[k] = 0
                elif unit.is_building:
                    vec[k] = 100 + unit.player     # buildings are ≥100
                else:
                    vec[k] = unit.power if unit.player == 1 else -unit.power
                k += 1
        return vec
    
    def reset(self, deck1: Deck, deck2: Deck):
        """
        Re-instantiate the game and return the starting observation.
        """
        self.__init__(deck1, deck2)
        return self._get_observation()

    def _get_observation(self) -> np.ndarray:
        """
        Concatenate
        • board vector (20 ints)
        • P1 hand (4 card ids)   – use 0 if slot empty
        • P2 hand (4 card ids)
        • current player flag
        • remaining mana of both players
        Produces a 20 + 4 + 4 + 1 + 2 = 31-element vector.
        """
        board_vec      = self._flatten_board(self.b.board)
        p1_hand_ids    = [c.card_id for c in self.player1.hand] + [0]*(4-len(self.player1.hand))
        p2_hand_ids    = [c.card_id for c in self.player2.hand] + [0]*(4-len(self.player2.hand))
        obs = np.array(list(board_vec) +
                    p1_hand_ids +
                    p2_hand_ids +
                    [self.cur_player] +
                    [self.player1.remain_mana,
                        self.player2.remain_mana],
                    dtype=np.int16)
        return obs

    def get_legal_actions(self) -> List[Action]:
        """
        Enumerate every legal move for the *current* player and
        return them as tuples the `step` method can consume.

        • Play  -> (card_idx, (x, y))
        • Cycle -> (card_idx,)
        • Pass  -> ()
        """
        legal: List[Action] = []

        player, _ = self.find_players()

        # -- cycle any hand card (Stormbound rule permits cycling once per turn)
        if player.can_cycle:
            for idx in range(len(player.hand)):
                legal.append((idx,))            # CycleAction

        # -- play any card that can be afforded / placed
        for idx, card in enumerate(player.hand):
            # Spell?
            if self.check_spell(idx):
                # single-target spells need targets; otherwise () target
                # Here we allow any board cell that satisfies check_single_target
                # is not right for spells that do not target
                for y in range(5):
                    for x in range(4):
                        if self.check_single_target(x, y, self.cur_player):
                            legal.append((idx, (x, y)))
            else:  # Unit / building cards
                for y in range(player.limit, 5):
                    for x in range(4):
                        if self.check_play(idx, x, y):
                            legal.append((idx, (x, y)))

        # -- optional pass
        legal.append(tuple())               # PassAction

        return legal

    def step(self, action: Action):
        """
        Apply an Action and advance the environment by **one
        *player* turn** (i.e., includes end_turn call).

        Returns: (obs, reward, done, info)
        """
        player, enemy = self.find_players()

        # --- decode action --------------------------------------
        if action == tuple():                       # Pass
            self.end_turn()
        elif len(action) == 1:                      # Cycle
            card_idx, = action
            self.cycle(card_idx)
        else:                                       # Play
            card_idx, (x, y) = action
            self.play(card_idx, x, y)

        # End of turn: let automatic effects trigger
        

        # --- compute reward -------------------------------------
        # Simple zero-sum: +1 if current player reduced enemy life to 0
        #                  -1 if they lost
        #                  0 otherwise.
        reward = 0
        done   = False
        if enemy.life <= 0 and player.life > 0:
            reward = 1
            done   = True
        elif player.life <= 0 and enemy.life > 0:
            reward = -1
            done   = True

        obs  = self._get_observation()
        info = {}                       # add diagnostics here
        return obs, reward, done, info


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
    deck1.add_card(Card(6, 0, 0, "spell", "Kindreds_Grace"))
    deck1.add_card(Card(7, 0, 0, "spell", "Heralds_Hymn"))
    deck1.add_card(Card(3, 1, 1, "satyr", "Counselor_Ahmi"))
    deck1.add_card(Card(3, 2, 1, "satyr", "Faun_Companions"))
    deck1.add_card(Card(3, 1, 1, "satyr", "Swarmcallers"))
    deck1.add_card(Card(5, 3, 0, "satyr", "Dreadfauns"))
    deck1.add_card(Card(6, 6, 0, "satyr", "Bucks_of_Wasteland"))
    deck1.add_card(Card(3, 4, 0, "satyr", "Generic"))
    deck1.add_card(Card(2, 2, 0, "satyr", "Generic"))
    # deck1.shuffle()
    g = Game(deck, deck1)
    g.display()
    g.play(0,-1,4)
    g.end_turn()
    g.play(1,2,4)
    g.end_turn()
    g.end_turn()
    g.display()


run()
