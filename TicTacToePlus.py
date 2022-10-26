class Sector:
    symbols = ['o', 'x', '-']
    turn_symbol = symbols[0]
    blank = symbols[2]

    board_turn = 0

    symbols_written = {}

    def __init__(self, sector_id):
        self.id = sector_id
        Sector.symbols_written[self.id] = {}
        self.turn = 0
        # last potrzebny do skróconego sprawdzania, czy ktoś wygrał
        self.last_col = 0
        self.last_row = 0

    def write_board(self):
        for row in range(3):
            for col in range(3):
                if (col, row) in Sector.symbols_written[self.id]:
                    symbol = Sector.symbols_written[self.id][(col, row)]
                else:
                    symbol = Sector.blank
                # print(symbol, end=' ')
            # print()
        return True

    def write_symbol(self, col, row, symbol=None):
        if symbol is None:
            symbol = Sector.turn_symbol

        col, row = int(col), int(row)
        status = True

        try:
            if Sector.symbols_written[self.id][(col, row)]:
                status = False
        except KeyError:
            Sector.symbols_written[self.id][(col, row)] = symbol
            self.turn += 1
            self.last_col, self.last_row = col, row

        self.write_board()
        return status

    def check_winner(self):
        status = 0

        # dla planszy, jeśli w sektorze był remis (żeby 3 remisy nie mogły wygrać)
        if self.id in Sector.symbols_written and (self.last_col, self.last_row) in Sector.symbols_written[self.id]:
            if Sector.symbols_written[self.id][(self.last_col, self.last_row)] == 'draw':
                return status
        # sprawdzanie skosów
        diagonals = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        for diagonal in diagonals:
            if (self.last_col, self.last_row) in diagonal:
                diagonal.remove((self.last_col, self.last_row))
                are_in_dic = diagonal[0] in Sector.symbols_written[self.id] and \
                             diagonal[1] in Sector.symbols_written[self.id]
                if are_in_dic:
                    is_winner = Sector.symbols_written[self.id][diagonal[0]] == \
                                Sector.symbols_written[self.id][diagonal[1]] == \
                                Sector.symbols_written[self.id][(self.last_col, self.last_row)]
                    if is_winner:
                        return 1

        grid_a = [0, 1, 2]

        # sprawdzanie rzędu
        temp_range = grid_a.copy()  # temporary list
        temp_range.remove(self.last_row)
        are_in_dic = (self.last_col, temp_range[0]) in Sector.symbols_written[self.id] and \
                     (self.last_col, temp_range[1]) in Sector.symbols_written[self.id]
        if are_in_dic:
            is_winner = \
                Sector.symbols_written[self.id][(self.last_col, 0)] == \
                Sector.symbols_written[self.id][(self.last_col, 1)] == \
                Sector.symbols_written[self.id][(self.last_col, 2)]
            if is_winner:
                return 1

        # sprawdzanie kolumny
        temp_range = grid_a.copy()  # temporary list
        temp_range.remove(self.last_col)
        are_in_dic = (temp_range[0], self.last_row) in Sector.symbols_written[self.id] and \
                     (temp_range[1], self.last_row) in Sector.symbols_written[self.id]
        if are_in_dic:
            is_winner = \
                Sector.symbols_written[self.id][(0, self.last_row)] == \
                Sector.symbols_written[self.id][(1, self.last_row)] == \
                Sector.symbols_written[self.id][(2, self.last_row)]
            if is_winner:
                return 1

        # remis dla pełnej planszy
        if self.turn == 9:
            status = -1
        # zwróć status: 0 = nikt nie wygrał; 1 = ktoś wygrał; -1 = remis
        return status


class Board(Sector):
    def __init__(self):
        super().__init__((3, 3))
        # next_sector -> sektor wskazany przez ostatnio wybrane pole
        # potrzebny do sprawdzenia zgodności aktualnie wybranego sektora
        self.next_sector = 4, 4  # 4, 4 -> freetake

    def check_sector(self, sector_col, sector_row, next_sector_to):
        status = True
        if self.next_sector != (4, 4):
            # jeśli nie freetake
            # wybrany sektor i next_sector muszą być te same
            status = self.next_sector == (sector_col, sector_row)
        else:
            # jeśli freetake
            # mid-block
            if Sector.board_turn == 0:
                status = (sector_col, sector_row) != (1, 1)
            # skończony sektor
            else:
                status = self.id not in Sector.symbols_written[(3, 3)]

        if status:
            Sector.next_sector = next_sector_to
        return status

    def next_turn(self, tile_col, tile_row):
        Sector.board_turn += 1
        Sector.turn_symbol = Sector.symbols[Sector.board_turn % 2]

        if (tile_col, tile_row) in Sector.symbols_written[3, 3]:
            self.next_sector = 4, 4
        else:
            self.next_sector = tile_col, tile_row
        return self.next_sector


if __name__ == '__main__':
    pass
