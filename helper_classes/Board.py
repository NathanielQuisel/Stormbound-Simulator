from .Unit import Unit
from typing import Optional

class Board:
    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(5)]

    #not at all done fixing yet
    def move_unit(self, cur_player, player, enemy, y, x, y_dir, x_dir):
        unit: Optional[Unit] = self.board[y][x]
        power = unit.power
        row = y + y_dir
        col = x + x_dir
        if row < 0:  # only happens forward
            if unit.vitalized:
                unit.change_power(1)
            unit.on_attack(None, player, enemy, self.board)
            unit.before_move(player, enemy, self.board)
            self.board[y][x] = None
            player.change_life(-power)
            unit.change_power(-power)
            unit.on_death(player, enemy, self.board)
            return

        ahead: Optional[Unit] = self.board[row][col]
        if ahead is None:  # only happens when moving forward
            unit.before_move(player, enemy, self.board)
            self.board[y][x] = None
            self.board[row][col] = unit
            unit.set_coors(col, row)
            unit.after_move(player, enemy, self.board)
            self.simple_set_limit(row, player)
        elif ahead.player == cur_player:  # only happens when moving forward
            return
        else:  # omnidirectional
            unit.on_attack(ahead, player, enemy, self.board)
            unit.before_move(player, enemy, self.board)
            if power > ahead.power:
                unit.change_power(-ahead.power)
                self.board[row][col] = None
                ahead.change_power(-ahead.power)
                ahead.on_death(enemy, player, self.board)
                self.board[row][col] = unit
                unit.on_survive(ahead.power, player, enemy, self.board)
                self.board[y][x] = None
                unit.set_coors(col, row)
                unit.after_move(player, enemy, self.board)
                unit.after_attack(player, enemy, self.board)
                self.simple_set_limit(row,player)
            elif ahead.power > power:
                ahead.change_power(-power)
                self.board[y][x] = None
                unit.change_power(-power)
                unit.on_death(player, enemy, self.board)
                ahead.on_survive(power, enemy, player, self.board)
            else:
                self.board[row][col] = None
                self.board[y][x] = None
                ahead.change_power(-ahead.power)
                unit.change_power(-power)
                ahead.on_death(enemy, player, self.board)
                unit.on_death(player, enemy, self.board)

    def simple_set_limit(self, y, player):
        if y < player.limit and y != 0:
            player.set_limit(y)

    def is_unit_at(self, x, y):
        # returns false if out of bounds
        # returns false if something is not there
        if x > 3 or x < 0 or y > 4 or y < 0:
            return False
        return self.board[y][x] is not None

    def adjacent_units(self, x, y):
        units = []
        if self.is_unit_at(x - 1, y):
            units.append(self.board[y][x - 1])
        if self.is_unit_at(x + 1, y):
            units.append(self.board[y][x + 1])
        if self.is_unit_at(x, y - 1):
            units.append(self.board[y - 1][x])
        if self.is_unit_at(x, y + 1):
            units.append(self.board[y + 1][x])
        return units

    def surrounding_units(self, x, y):
        units = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if (i != 0 or j != 0) and self.is_unit_at(x + j, y + i):
                    units.append(self.board[y + i][x + j])
        return units

    def all_units(self):
        units = []
        for row in self.board:
            for cell in row:
                if cell is not None:
                    units.append(cell)
        return units

    def display(self):
        for row in self.board:
            for cell in row:
                if cell is not None:
                    print(cell.power, cell.player, end=" ")
                else:
                    print("______", end=" ")
            print()