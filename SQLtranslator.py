import sqlite3
from dev_tools import dprint


class DBMSTranslator:
    def __init__(self):
        self.conn = None
        self.cur = None

    def open(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        dprint("database opened")
        return True

    def close(self, commit=True):
        if commit:
            self.conn.commit()
        self.conn.close()
        dprint("database closed")
        return True

    # manipulate tables
    def create_tables(self, **kwargs: list[str]):
        """
        Examples of passing keys:\n
        create_tables("table1"=["col1 INTEGER", "col2 TEXT"])\n
        or\n
        table = "table1"\n
        create_tables(**{table: ["col1 INTEGER", "col2 TEXT"])

        :param kwargs: table name as a key, columns data in a list[str]
        :return: True if successfully created, False otherwise
        """
        try:
            for table, data in kwargs.items():
                columns = ", "
                columns = columns.join(data)

                command = f"CREATE TABLE {table} ({columns});"
                dprint(command)
                self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def clear_table(self, table, condition=None, delete_table=False):
        """
        Clear whole table, values by condition or delete whole table.

        :param table: table the operation should be performed on
        :param condition: if given, adds "WHERE {condition}" to the command (default None)
        :param delete_table: if True, deletes targeted table (default False)
        :return: True if successfully created, False otherwise
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
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    # manipulate columns
    def add_column(self, table, column, default=""):
        """
        ALTER TABLE <table> ADD <column>, default <default>;\n

        :param table: table the operation should be performed on
        :param column: name of the column to add
        :param default: default value of the column (optional)
        :return:True if successfully created, False otherwise
        """
        try:
            if default != "":
                default = f"default {default}"
            command = f"ALTER TABLE {table} ADD {column}{default};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def rename_column(self, table, old_col_name, new_col_name):
        """
        ALTER TABLE <table> RENAME COLUMN <old_col_name> TO <new_col_name>;\n

        :param table: table the operation should be performed on
        :param old_col_name: current table name
        :param new_col_name: new table name
        :return: True if successfully created, False otherwise
        """
        try:
            command = f"ALTER TABLE {table} RENAME COLUMN {old_col_name} TO {new_col_name};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def change_column_data_type(self, table, col_data):
        """
        ALTER TABLE {table} ALTER COLUMN {col_data};

        :param table: table the operation should be performed on
        :param col_data: column and desired data type after a space
        :return: True if successfully created, False otherwise
        """
        try:
            command = f"ALTER TABLE {table} ALTER COLUMN {col_data};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def delete_column(self, table, column):
        """
        ALTER TABLE <table> DROP COLUMN <column>;\n

        :param table: table the operation should be performed on
        :param column: column to delete
        :return: True if successfully created, False otherwise
        """

        try:
            command = f"ALTER TABLE {table} DROP COLUMN {column};"
            dprint(command)
            self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    # manipulate values
    def insert_values(self, **kwargs):
        """
        table=[values]\n
        or\n
        table={columns: values}\n
        column names syntax: "column_name"\n
        values syntax: "'text_value'", "
        :return: True if successfully created, False otherwise
        """
        try:
            for table, data in kwargs.items():
                columns = ""
                values = ", "
                if type(data) is dict:
                    columns = "(" + values.join(data.keys()) + ") "
                    values = values.join(data.values())
                elif type(data) is list:
                    values = values.join(data)
                else:
                    dprint("Wrong data type")
                    break
                command = f"INSERT INTO {table} {columns}VALUES({values});"
                dprint(command)
                self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def update_columns_values(self, **kwargs: tuple[str, str]):
        """

        :param kwargs: table name as a key, columns data in a list[str]
        :return: True if successfully created, False otherwise
        """
        try:
            for table, data in kwargs.items():
                column, value = data
                self.cur.execute(f"UPDATE {table} SET {column} = '{value}';")
                dprint(f"UPDATE {table} SET {column} = '{value}';")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False


if __name__ == '__main__':
    data_base = DBMSTranslator()
    data_base.open("D:/_Programming/python/TicTacToe+/tic-tac-toe-plus.db")

    data_base.insert_values(user={
        "username": "'Chris'",
        "first_name": "'Krzysztof'",
        "last_name": "'Kulak'",
        "password": "'qwerty'",
        "active": "1"})

    data_base.close()
