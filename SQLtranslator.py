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
        > CREATE TABLE {table} ({columns});\n
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

    def clear_table(self, **kwargs):
        """
        if not value but is not None, column is cleared\n
        > DELETE FROM {table}\n
        if value is given and is not None, condition is added\n
        > WHERE {value} (optional)\n
        if value is None, the column is deleted:\n
        > DROP TABLE {table}

        :return: True if successfully created, False otherwise
        """
        try:
            for table, value in kwargs.items():
                command = f"DELETE FROM {table}"
                if value:
                    command += f" WHERE {value}"
                elif value is None:
                    command = f"DROP TABLE {table}"
                command += ";"

                dprint(command)
                self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    # manipulate columns
    def add_columns(self, **kwargs):
        """
        > ALTER TABLE <table> ADD <column>, default <default>;\n
        table=(["col_name DATA_TYPE"], {"col_name DATA_TYPE": "default_value"})

        :return:True if successfully created, False otherwise
        """
        try:
            for table, value in kwargs.items():
                for column in value:
                    default = ""
                    if type(value) is dict:
                        default = f" default {value[column]}"
                    command = f"ALTER TABLE {table} ADD {column}{default};"
                    dprint(command)
                    self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def rename_columns(self, **kwargs: dict[str: str]):
        """
        > ALTER TABLE <table> RENAME COLUMN <old_col_name> TO <new_col_name>;\n
        table={"old_col_name": "new_col_name"}

        :return: True if successfully created, False otherwise
        """
        try:
            for table, columns in kwargs.items():
                for old_col_name, new_col_name in columns:
                    command = f"ALTER TABLE {table} RENAME COLUMN {old_col_name} TO {new_col_name};"
                    dprint(command)
                    self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def change_columns_data_type(self, **kwargs: list[str]):
        """
        > ALTER TABLE {table} ALTER COLUMN {col_data};\n
        table=["col_name DATA_TYPE"]

        :return: True if successfully created, False otherwise
        """
        try:
            for table, cols_data in kwargs.items():
                for col_datum in cols_data:
                    command = f"ALTER TABLE {table} ALTER COLUMN {col_datum};"
                    dprint(command)
                    self.cur.execute(command)
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False

    def delete_columns(self, **kwargs: list[str]):
        """
        > ALTER TABLE <table> DROP COLUMN <column>;\n
        table=[columns]\n

        :return: True if successfully created, False otherwise
        """

        try:
            for table, columns in kwargs.items():
                for column in columns:
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
        > INSERT INTO {table} {columns}VALUES({values});\n
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
        > UPDATE {table} SET {column} = '{value}';

        :param kwargs: table name as a key, columns data in a list[str]
        :return: True if successfully created, False otherwise
        """
        try:
            for table, data in kwargs.items():
                column, value = data
                dprint(f"UPDATE {table} SET {column} = '{value}';")
                self.cur.execute(f"UPDATE {table} SET {column} = '{value}';")
            return True
        except sqlite3.OperationalError as err:
            dprint(err)
        return False


if __name__ == '__main__':
    data_base = DBMSTranslator()
    data_base.open("tic-tac-toe-plus.db")

    flag = True
    while flag:
        exec(input("> "))

    data_base.close()
