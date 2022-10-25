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
        # print(self.id)
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
            # print(f'\n{self} symbol {symbol}')

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
        #print(f"last row: {self.last_row}")
        is_winner = False
        # TODO: instead of exceptions, check if keys are in dictionary (2 besides the one written just now)
        # TODO: draws don't work btw
        if nie_remis:
            try:
                # sprawdzanie wierszy
                is_winner = \
                    Sector.symbols_written[self.id][(0, self.last_row)] \
                    == Sector.symbols_written[self.id][(1, self.last_row)] \
                    == Sector.symbols_written[self.id][(2, self.last_row)]
            except KeyError:
                pass

            if not is_winner:
                # sprawdzanie kolumn
                try:
                    is_winner = \
                        Sector.symbols_written[self.id][(self.last_col, 0)] \
                        == Sector.symbols_written[self.id][(self.last_col, 1)] \
                        == Sector.symbols_written[self.id][(self.last_col, 2)]
                except KeyError:
                    pass

                if not is_winner:
                    # sprawdzanie skosów
                    try:
                        if Sector.symbols_written[self.id][(1, 1)] != Sector.blank and nie_remis:
                            # skos lewo-prawo
                            is_winner = Sector.symbols_written[self.id][(0, 0)] == Sector.symbols_written[self.id][(1, 1)] \
                                    == Sector.symbols_written[self.id][(2, 2)]
                    except KeyError:
                        pass

                    if not is_winner:
                        try:
                            if Sector.symbols_written[self.id][(1, 1)] != Sector.blank and nie_remis:
                                # skos prawo-lewo
                                is_winner = Sector.symbols_written[self.id][(0, 2)] == Sector.symbols_written[self.id][(1, 1)] \
                                        == Sector.symbols_written[self.id][(2, 0)]
                        except KeyError:
                            # remis dla pełnej planszy
                            if self.turn == 9:
                                status = -1
        if is_winner:
            status = 1
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
        status = True
        if self.next_sector != (4, 4):
            # jeśli nie freetake
            # wybrany sektor i next_sector muszą być te same
            # print('Incorrect sector has been chosen!')
            status = self.next_sector == (sector_col, sector_row)
        else:
            # jeśli freetake
            # mid-block
            # print('mid-block!')
            if Sector.board_turn == 0:
                status = (sector_col, sector_row) != (1, 1)
            # skończony sektor
            # print('Sector is already finished!')
            else:
                status = self.id not in Sector.symbols_written[(3, 3)]

        if status:
            Sector.next_sector = next_sector_to
        return status

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
        return self.next_sector


if __name__ == '__main__':
    pass
