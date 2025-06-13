class Board:
    def __init__(self):
        self.board = [[None for _ in range(4)] for _ in range(5)]

    def display(self):
        for row in self.board:
            for cell in row:
                if cell is not None:
                    print(cell.power, cell.player, end=" ")
                else:
                    print("______", end=" ")
            print()