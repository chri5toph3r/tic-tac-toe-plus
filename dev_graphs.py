import pandas as pd
from collections import OrderedDict
import pylab
from pandas_ods_reader import read_ods
from pyexcel_ods import save_data


rows = [["turn", "t_board [ms]", "t_symbols [ms]", "t_all [ms]", "t_main [ms]",
         "sector [col:row]", "tile [col:row]"]]


def times(times_vars, main_time, turn, positions):
    t_board, t_symbols, t_all = times_vars
    print(turn)
    print(f"czas rysowania planszy: {t_board}ms")
    print(f"czas rysowania symboli: {t_symbols}ms")
    print(f"cały czas rysowania: {t_all}ms")
    print()
    rows.append([turn, t_board, t_symbols, t_all, main_time,
                 f"{positions[0]}:{positions[1]}", f"{positions[2]}:{positions[3]}"])
    return


def generate(res_file, res_sheet):
    data = OrderedDict()
    data.update({res_sheet: rows})
    save_data(res_file, data)

    df = read_ods(res_file)
    turn = df["turn"]
    t_symbols = df["t_symbols [ms]"]
    t_main = df["t_main [ms]"]
    pylab.plot(turn, t_symbols, label="t symbole")
    pylab.plot(turn, t_main, label="t main")
    pylab.legend()
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
