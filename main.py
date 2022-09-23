from TicTacToePlus import *
import WinMg
import pygame

# TODO: kwadraty nie wygrywają
# TODO: przy wygranej stawiają się 2 symbole więc jedna kolejka wypada
# TODO: wygrana sektorów - duże symbole

window = WinMg.Pen()
window.draw_default_board()

board = Board()
sectors_obj = {}

for col in range(3):
    for row in range(3):
        name = col, row
        sectors_obj[name] = Sector()


# wywoływanie odpowiedniego sektora
def main():
    global sectors_obj, board

    return_status = 0

    positions = window.pos_translate(pygame.mouse.get_pos())

    if positions is None:
        return return_status

    board_col, board_row = positions
    board_col, board_row = int(board_col), int(board_row)
    # print(f'board{board_col, board_row}')

    sector_col, sector_row = board_col // 3, board_row // 3
    # print(f'sector{sector_col, sector_row}')

    tile_col, tile_row = board_col % 3, board_row % 3
    # print(f'tile{tile_col, tile_row}')

    # czy odpowiedni sektor?
    if not board.check_sector(sector_col, sector_row, (tile_col, tile_row)):
        print('1. incorrect sector')
        return return_status

    # czy odpowiednie pole?
    if not sectors_obj[sector_col, sector_row].write_symbol(tile_col, tile_row):
        print('2. incorrect tile')
        return return_status

    # jeśli tak, to
    # narysuj symbol
    window.draw_symbol(Sector.turn_symbol)
    # dodaj nowe otoczenie
    # window.draw_symbol('outline')
    print('2.5 symbol drawn')

    # czy ktoś wygrał sektor?
    sector_status = sectors_obj[sector_col, sector_row].check_winner()  # 3 możliwe wartości zwrotne
    if sector_status:
        sectors_obj[sector_col, sector_row].write_board()
        # jeśli tak, narysuj symbol, lub wpisz 'draw'
        if sector_status == 1:
            board.write_symbol(sector_col, sector_row)
            window.draw_symbol(Sector.turn_symbol, 'sector', (sector_col, sector_row))
        else:
            board.write_symbol(sector_col, sector_row, 'draw')

        # czy ktoś wygrał grę?
        return_status = board.check_winner()
        if return_status:
            return return_status
        else:
            print('4. no one won the game')

    else:
        print('3. no one won the sector')

    board.next_turn(tile_col, tile_row)
    return return_status


if __name__ == '__main__':
    flag = True
    ctrl = 0
    while flag:
        for event in pygame.event.get():
            flag = event.type != pygame.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and not ctrl:
                if ctrl == 0:
                    ctrl = main()
                if ctrl == 1:
                    fin_msg = f'{Sector.turn_symbol} won'
                    window.fin_msg(fin_msg)
                elif ctrl == -1:
                    fin_msg = 'draw'
                    window.fin_msg(fin_msg)
