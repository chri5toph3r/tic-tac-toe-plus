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
        return t


class DataBase(DataGetter):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect('tic-tac-toe-plus.db')
        self.cur = self.conn.cursor()

    @staticmethod
    def convert_to_sql_str(values):
        col_str = ""
        for column in values[:-1]:
            col_str += str(column) + ", "
        col_str += str(values[-1])
        dprint(col_str)
        return col_str

    def insert_values(self, table, values: tuple, columns: tuple = ""):
        """
        :param table: table on which the function should operate
        :param values: if columns not given, values are added left to right
        :param columns: dictates how values are being added
        :return: True if executed without Operational Error
        """
        try:
            if columns != "":
                columns = f"{columns} "
            command = f"INSERT INTO {table} {columns}VALUES {values};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def set_columns_value(self, table, *args):
        try:
            for item in args:
                column, value = item
                self.cur.execute(f"UPDATE {table} SET {column} = '{value}';")
                dprint(f"UPDATE {table} SET {column} = '{value}';")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def column_operate(self, table, value, default="NULL", operation="ADD"):
        try:
            command = f"ALTER TABLE {table} {operation} {self.convert_to_sql_str(value)}"
            if operation == "ADD":
                command += f", default {default}"
            command += ";"
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def create_table(self, table, columns):
        try:
            self.cur.execute(f"CREATE TABLE {table} ({self.convert_to_sql_str(columns)});")
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
    data_base.set_columns_value(tbl, ("annotations", "No annotation added"))

    data_base.close()
