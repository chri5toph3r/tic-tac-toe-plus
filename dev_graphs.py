import pandas as pd
from collections import OrderedDict
import pylab
from pandas_ods_reader import read_ods
from pyexcel_ods import save_data

turn_col = "turn"
t_board_col = "t_board [ms]"
t_symbols_col = "t_symbols [ms]"
t_drawing_col = "t_drawing [ms]"
t_main_col = "t_main [ms]"
t_check_symbols_col = "t_check_sectors [ms]"
t_sum_col = "t_check_sectors + t_symbols [ms]"
sector_col = "sector [col:row]"
tile_col = "tile [col:row]"

rows = [[turn_col, t_board_col, t_symbols_col, t_drawing_col, t_main_col, t_check_symbols_col,
         t_sum_col, sector_col, tile_col]]


def times(times_vars, main_time, check_sectors_time, turn, positions):
    t_board, t_symbols, t_all = times_vars
    print(turn)
    print(f"czas sprawdzania czy ktoś wygrał: {check_sectors_time}ms")
    print(f"czas wykonywania main: {main_time}ms")
    print(f"czas rysowania planszy: {t_board}ms")
    print(f"czas rysowania symboli: {t_symbols}ms")
    print(f"cały czas rysowania: {t_all}ms")
    print()
    rows.append([turn, t_board, t_symbols, t_all, main_time, check_sectors_time,
                 t_symbols + check_sectors_time, f"{positions[0]}:{positions[1]}", f"{positions[2]}:{positions[3]}"])
    return


def generate(res_file, res_sheet):
    data = OrderedDict()
    data.update({res_sheet: rows})
    save_data(res_file, data)

    df = read_ods(res_file)
    turn = df[turn_col]
    t_symbols = df[t_symbols_col]
    t_main = df[t_main_col]
    pylab.plot(turn, t_symbols, "c", label="drawing symboles time")

    pylab.plot(turn, t_symbols, "b.")

    sectors = df["sector [col:row]"]
    tiles = df["tile [col:row]"]

    for index, xy in enumerate(zip(turn, t_symbols)):
        pylab.annotate(f"{sectors[index]} | {tiles[index]}", color="black", xy=xy, textcoords='data',
                       ha="right", va="bottom")

    pylab.legend()
    pylab.grid()
    pylab.show()
    return


def sample():
    df = pd.read_ods(r'https://analityk.edu.pl/wp-content/uploads/2020/12/data.csv')
    df['date'] = pd.to_datetime(df.date, format='%d/%m/%Y')
    x = df['date']
    y = df['Close']
    pylab.plot(x, y)
    pylab.show()


if __name__ == '__main__':
    sample()
