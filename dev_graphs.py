import pandas as pd
from collections import OrderedDict
import pylab
from pandas_ods_reader import read_ods
from pyexcel_ods import save_data

rows = [["turn", "t_board [ms]", "t_symbols [ms]", "t_all [ms]", "t_main [ms]", "t_check_sectors [ms]",
         "t_check_sectors + t_symbols [ms]", "sector [col:row]", "tile [col:row]"]]


def times(times_vars, main_time, check_sectors_time, turn, positions):
    t_board, t_symbols, t_all = times_vars
    print(turn)
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
    turn = df["turn"]
    t_symbols = df["t_symbols [ms]"]
    t_main = df["t_main [ms]"]
    t_check = df["t_check_sectors [ms]"]
    t_sum = df["t_check_sectors + t_symbols [ms]"]
    pylab.plot(turn, t_symbols, "c", label="t symbole")
    pylab.plot(turn, t_check, "m", label="t check sector")
    pylab.plot(turn, t_sum, "r--", label="t_check_sectors + t_symbols")
    pylab.plot(turn, t_main, "k", label="t main")

    pylab.plot(turn, t_main, "k.")

    sectors = df["sector [col:row]"]
    tiles = df["tile [col:row]"]

    for index, xy in enumerate(zip(turn, t_main)):
        pylab.annotate(f"{sectors[index]} | {tiles[index]}", color="red", xy=xy, textcoords='data',
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
