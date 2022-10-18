class Sector:
    symbols = ['o', 'x', '-']
    turn_symbol = symbols[0]
    blank = symbols[2]

    board_turn = 0

    symbols_written = {}

    def __init__(self, sector_id):
        self.id = sector_id
        Sector.symbols_written[self.id] = {}
        # print(f'{self.id} dic: {Sector.symbols_written}')
        self.turn = 0
        # last potrzebny do skróconego sprawdzania, czy ktoś wygrał
        self.last_col = 0
        self.last_row = 0

    def write_board(self):
        print(self.id)
        for row in range(3):
            for col in range(3):
                if (col, row) in Sector.symbols_written[self.id]:
                    symbol = Sector.symbols_written[self.id][(col, row)]
                else:
                    symbol = '-'
                print(symbol, end=' ')
            print()
        return True

    def write_symbol(self, col, row, symbol=None):
        if symbol is None:
            symbol = Sector.turn_symbol
            print(f'\n{self} symbol {symbol}')

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
        try:
            nie_remis = Sector.symbols_written[self.id][(self.last_row, self.last_col)] != 'draw'
        except KeyError:
            nie_remis = True

        # sprawdź tylko dla rzędu i kolumny, w których został ostatnio postawiony znak
        try:
            print(f"last row: {self.last_row}")
            row_win = \
                Sector.symbols_written[self.id][(0, self.last_row)] \
                == Sector.symbols_written[self.id][(1, self.last_row)] \
                == Sector.symbols_written[self.id][(2, self.last_row)]
            if row_win and nie_remis:
                status = 1
        except KeyError:
            try:
                col_win = \
                    Sector.symbols_written[self.id][(self.last_col, 0)] \
                    == Sector.symbols_written[self.id][(self.last_col, 1)] \
                    == Sector.symbols_written[self.id][(self.last_col, 2)]
                if col_win and nie_remis:
                    status = 1
            except KeyError:
                # sprawdzanie skosów
                try:
                    if Sector.symbols_written[self.id][(1, 1)] != Sector.blank and nie_remis:
                        if Sector.symbols_written[self.id][(0, 0)] == Sector.symbols_written[self.id][(1, 1)] \
                                == Sector.symbols_written[self.id][(2, 2)]:
                            status = 1
                except KeyError:
                    try:
                        if Sector.symbols_written[self.id][(0, 2)] == Sector.symbols_written[self.id][(1, 1)] \
                                == Sector.symbols_written[self.id][(2, 0)]:
                            status = 1
                    except KeyError:
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
        # print(f"next sector while checking: {self.next_sector}")
        if self.next_sector != (4, 4):
            # jeśli nie freetake
            # wybrany sektor i next_sector muszą być te same
            if self.next_sector != (sector_col, sector_row):
                print('Incorrect sector has been chosen!')
                return False
        else:
            # jeśli freetake
            # mid-block
            if Sector.board_turn == 0 and (sector_col, sector_row) == (1, 1):
                print('mid-block!')
                return False
            # skończony sektor
            if self.id in Sector.symbols_written[(3, 3)]:
                print('Sector is already finished!')
                return False
        Sector.next_sector = next_sector_to
        return True

    def next_turn(self, tile_col, tile_row):
        Sector.board_turn += 1
        Sector.turn_symbol = Sector.symbols[Sector.board_turn % 2]
        # print(f'board turn: {Sector.board_turn}')

        # print(f"id: {self.id}; board symbols: {Sector.symbols_written[3, 3]}")

        if (tile_col, tile_row) in Sector.symbols_written[3, 3]:
            self.next_sector = 4, 4
        else:
            self.next_sector = tile_col, tile_row
        # print(f"next sector after drawing: {self.next_sector}")
        return


if __name__ == '__main__':
    pass
