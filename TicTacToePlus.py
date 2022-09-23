
class Sector:
    symbols = ['o', 'x', '-']
    turn_symbol = symbols[0]
    blank = symbols[2]

    board_turn = 0

    def __init__(self):
        self.tiles_list = [[Sector.blank, Sector.blank, Sector.blank],
                           [Sector.blank, Sector.blank, Sector.blank],
                           [Sector.blank, Sector.blank, Sector.blank]]
        self.turn = 0
        # last potrzebny do skróconego sprawdzania, czy ktoś wygrał
        self.last_col = 0
        self.last_row = 0

    def write_board(self):
        for row in range(len(self.tiles_list)):
            for tile in range(len(self.tiles_list[row])):
                print(self.tiles_list[row][tile], end=' ')
            print()
        return True

    def write_symbol(self, col, row, symbol=None):
        if symbol is None:
            symbol = Sector.turn_symbol
            print(f'\n{self} symbol {symbol}')

        col = int(col)
        row = int(row)

        if self.tiles_list[row][col] != Sector.blank:
            return False

        self.tiles_list[row][col] = symbol
        self.turn += 1
        self.last_col, self.last_row = col, row
        return True

    def check_winner(self):
        # dla planszy, jeśli w sektorze był remis
        nie_remis = self.tiles_list[self.last_row][self.last_col] != 'draw'
        status = 0

        # sprawdź tylko dla rzędu i kolumny, w których został ostatnio postawiony znak
        row_win = \
            self.tiles_list[self.last_row][0] == self.tiles_list[self.last_row][1] == self.tiles_list[self.last_row][2]
        if row_win and nie_remis:
            status = 1

        col_win = \
            self.tiles_list[0][self.last_col] == self.tiles_list[1][self.last_col] == self.tiles_list[2][self.last_col]
        if col_win and nie_remis:
            status = 1

        # sprawdzanie skosów
        if self.tiles_list[1][1] != Sector.blank and nie_remis:
            print(self.tiles_list[0][0] == self.tiles_list[1][1] == self.tiles_list[2][2])
            if self.tiles_list[0][0] == self.tiles_list[1][1] == self.tiles_list[2][2]:
                status = 1
            if self.tiles_list[0][2] == self.tiles_list[1][1] == self.tiles_list[2][0]:
                status = 1

        # remis dla pełnej planszy
        if self.turn == 9:
            status = -1

        # zwróć status: 0 = nikt nie wygrał; 1 = ktoś wygrał; -1 = remis
        return status


class Board(Sector):
    def __init__(self):
        super().__init__()
        # next_sector -> sektor wskazany przez ostatnio wybrane pole
        # potrzebny do sprawdzenia zgodności aktualnie wybranego sektora
        # TODO: sprawdzanie nie chce działać, sprawdzić co jest 5
        self.next_sector = 3, 3

    def check_sector(self, sector_col, sector_row, next_sector_to):
        if self.next_sector != (3, 3):
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
            if self.tiles_list[sector_row][sector_col] is not Sector.blank:
                print('Sector is already finished!')
                return False
        Sector.next_sector = next_sector_to
        return True

    def next_turn(self, tile_col, tile_row):
        Sector.board_turn += 1
        Sector.turn_symbol = Sector.symbols[Sector.board_turn % 2]
        print(f'board turn: {Sector.board_turn}')

        if self.tiles_list[tile_row][tile_col] != Sector.blank:
            self.next_sector = 3, 3
        else:
            self.next_sector = tile_col, tile_row
        return


if __name__ == '__main__':
    pass
