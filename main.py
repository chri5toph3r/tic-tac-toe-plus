from TicTacToePlus import *
import WinMg
import statistics
from dev_tools import dprint
import pygame


window = WinMg.Pen()
window.draw_default_board()

board = Board()
sectors_obj = {}

data_base = statistics.DataBase()

for col in range(3):
    for row in range(3):
        name = col, row
        sectors_obj[name] = Sector(name)


# wywoływanie odpowiedniego sektora
def main():
    global sectors_obj, board

    return_status = 0

    positions = window.pos_system_translate(window.pos_translate(pygame.mouse.get_pos()))
    if positions is None:
        return return_status

    sector_col, sector_row, tile_col, tile_row = positions

    # czy odpowiedni sektor?
    if not board.check_sector(sector_col, sector_row, (tile_col, tile_row)):
        return return_status

    # czy odpowiednie pole?
    if not sectors_obj[sector_col, sector_row].write_symbol(tile_col, tile_row):
        return return_status

    # czy ktoś wygrał sektor?
    sector_status = sectors_obj[sector_col, sector_row].check_winner()  # 3 możliwe wartości zwrotne
    if sector_status:
        # jeśli tak, narysuj symbol, lub wpisz 'draw'
        if sector_status == 1:
            board.write_symbol(sector_col, sector_row)
        else:
            board.write_symbol(sector_col, sector_row, 'draw')
        # czy ktoś wygrał grę?
        return_status = board.check_winner()

    data_base.timestamp(board.board_turn + 1, board.turn_symbol)

    cursor_change = False
    next_sector = None
    if return_status == 0:
        cursor_change = True
        next_sector = board.next_turn(tile_col, tile_row)

    window.refresh(Sector.symbols_written, next_sector, change_cur=cursor_change)
    return return_status


if __name__ == '__main__':
    flag = True
    ctrl = 0
    data_base.set_timer()

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
