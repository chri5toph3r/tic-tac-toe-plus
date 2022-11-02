import sqlite3
import time
from dev_tools import dprint, dev


class DataGetter:
    def __init__(self):
        self.timer = 0
        self.times_sum = 0
        self.log_list = []

    # timer features
    def set_timer(self):
        self.timer = time.time()
        return self.timer

    def timestamp(self, *args):
        t = time.time() - self.timer - self.times_sum
        t = round(t, 4)
        self.log_list.append(args + (t,))
        self.times_sum += t

        dprint(f"{self.log_list[-1]}")
        if dev:
            for item in self.log_list:
                dprint(item)

        return t


class DataBase(DataGetter):
    def __init__(self):
        super().__init__()
        self.conn = None
        self.cur = None

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

    def set_columns_value(self, table, *args: tuple[str, str]):
        try:
            for item in args:
                column, value = item[0], item[1]
                self.cur.execute(f"UPDATE {table} SET {column} = '{value}';")
                dprint(f"UPDATE {table} SET {column} = '{value}';")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def add_table(self):
        """
        ALTER TABLE <table> ADD <value>, default <default>;\n

        :return:
        """
        value = f"{value} default {default}"

    def rename_table(self):
        """
        ALTER TABLE <table> RENAME COLUMN <value[0]> TO <value[1]>;\n

        :return:
        """
        value = f"{value[0]} TO {value[1]}"

    def delete_column(self, table, column):
        """
        ALTER TABLE <table> DROP COLUMN <column>;\n

        :param column:
        :param table:
        :return: None if error occurred, command otherwise
        """

        try:
            command = f"ALTER TABLE {table} DROP COLUMN {column};"
            dprint(command)
            self.cur.execute(command)
            return command
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def change_column_data_type(self, table, col_data):
        """
        Use this method to change targeted column's data type.\n
        ALTER TABLE {table} ALTER COLUMN {col_data};

        :param table: table the operation should be performed on
        :param col_data: column and desired data type after a space
        :return: None if error occurred, command otherwise
        """
        try:
            command = f"ALTER TABLE {table} ALTER COLUMN {col_data};"
            dprint(command)
            self.cur.execute(command)
            return command
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def clear_table(self, table, condition=None, delete_table=False):
        """
        Clear whole table, values by condition or delete whole table.

        :param table: table the operation should be performed on
        :param condition: if given, adds "WHERE {condition}" to the command (default None)
        :param delete_table: if True, deletes targeted table (default False)
        :return: None if error occurred, command otherwise
        """
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
            return command
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def create_tables(self, **kwargs: list[str]):
        """
        Examples of passing keys:\n
        create_tables("table1"=["col1 INTEGER", "col2 TEXT"])\n
        or\n
        table = "table1"\n
        create_tables(**{table: ["col1 INTEGER", "col2 TEXT"])

        :param kwargs: table name as a key, columns data in a list[str]
        :return: True if successfully created, False otherwise (doesn't return command bcs uses for loop)
        """
        try:
            for table in kwargs.keys():
                columns = " "
                columns = columns.join(kwargs[table])

                command = f"CREATE TABLE {table} ({columns});"
                dprint(command)
                self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def open(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        dprint("database opened")
        return True

    def close(self):
        self.conn.commit()
        self.conn.close()
        dprint("database closed")
        return True


if __name__ == '__main__':
    data_base = DataBase()
    data_base.open("D:/_Programming/python/TicTacToe+/tic-tac-toe-plus.db")
    tbl = "user"
    # data_base.clear_table(tbl, delete_table=True)
    data_base.create_tables(**{tbl: ["turn INTEGER", "username TEXT", "sector TEXT", "time REAL"]})

    # data_base.add_columns(tbl, ["annotations TEXT"])

    data_base.close()
