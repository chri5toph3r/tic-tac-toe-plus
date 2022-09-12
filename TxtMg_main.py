from TicTacToePlus import *

symbols = ['◯', '✘', '▢']


def write_board(tiles_list):
    for row in range(len(tiles_list)):
        for tile in range(len(tiles_list[row])):
            print(tiles_list[row][tile], end=' ')
        print()
    return True


def tictactoe_main(symbols_list):
    board = Sector(symbols_list)
    flag = 0
    while not flag:
        choice = input('ColRow: ')
        if board.write_symbol(choice[0], choice[1]):
            flag = board.check_winner()
        write_board(board.tiles_list)
    if flag == 1:
        print(f'{board.turn_symbol} won')
    else:
        print('draw')


if __name__ == '__main__':
    tictactoe_main(symbols)
