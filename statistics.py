import sqlite3
import time
from dev_tools import dprint, dev


class DataGetter:
    def __init__(self):
        self.timer = 0
        self.log_list = []

    # timer features
    def set_timer(self):
        self.timer = time.time()
        return self.timer

    def timestamp(self, turn, symbol, timer_reset=True):
        t = time.time() - self.timer
        self.log_list.append((turn, symbol, t))

        dprint(f"{turn} | {symbol} | {t}")
        if dev:
            for item in self.log_list:
                dprint(item)

        if timer_reset:
            self.set_timer()
        return turn, symbol, t


class DataBase(DataGetter):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('tic-tac-toe-plus.db')
        self.cur = self.conn.cursor()

    def insert_values(self, table, values: tuple, columns: tuple = ""):
        """
        :param table: table on which the function should operate
        :param values: if columns not given, values are added left to right
        :param columns: dictates how values are being added
        :return: True if executed without Operational Error
        """
        try:
            if columns != "":
                if len(columns) != len(values):
                    dprint(f" len{columns} != len{values}")
                    return False
                columns = f"{columns} "
            command = f"INSERT INTO {table} {columns}VALUES {values};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def set_columns_value(self, table, *args: tuple):
        try:
            for item in args:
                column, value = item[0], item[1]
                self.cur.execute(f"UPDATE {table} SET {column} = '{value}';")
                dprint(f"UPDATE {table} SET {column} = '{value}';")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def column_operate(self, table, value, default="NULL", operation="ADD"):
        try:
            if type(value) is not str:
                value = str(value)[1:-1]
            command = f"ALTER TABLE {table} {operation} {value}"
            if operation == "ADD":
                command += f", default {default}"
            command += ";"

            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def clear_table(self, table, condition=None, delete_table=False):
        try:
            if delete_table:
                command = f"DROP TABLE {table};"
            else:
                command = f"DELETE FROM {table}"
                if condition is not None:
                    command += f" WHERE {condition}"
                command += ";"

            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def create_table(self, table, columns):
        try:
            if type(columns) is not str:
                columns = str(columns)[1:-1]
            self.cur.execute(f"CREATE TABLE {table} ({columns});")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def close(self):
        self.conn.commit()
        self.conn.close()
        return True


if __name__ == '__main__':
    data_base = DataBase()
    tbl = "Input_times"
    # data_base.create_table(tbl, [
    #     "turn INTEGER",
    #     "username TEXT",
    #     "time REAL"
    # ])
    # data_base.add_columns(tbl, ["annotations TEXT"])
    data_base.insert_values(tbl, (4.1023, 3, "Markus", "comment"), ("time", "turn", "username", "annotations"))
    data_base.insert_values(tbl, (1, "Krzysztof", 9.1203, "do not delete"))
    data_base.clear_table(tbl, "annotations!='do not delete'")
    data_base.column_operate(tbl, "annotations", operation="DROP COLUMN")

    data_base.close()
