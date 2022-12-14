import os
import sqlite3
from dev_tools import dprint
import inspect


class DBMSTranslator:
    def __init__(self):
        self.database = None
        self.hidden_methods = [
            "open",
            "close",
            "conn",
            "get_methods",
            "get_method_info"
        ]
        self.conn = None
        self.cur = None
        self.methods_list = []
        self.methods_help_dic = {
            "create_tables":
            """
            \033[1;3m
            takes kwargs
            columns syntax: "col_name DATA_TYPE etc"
            tables=[columns]
            > CREATE TABLE table (columns);
            \033[0m
            """,

            "clear_tables":
            """
            \033[1;3m
            takes kwargs
            tables=""
            > DELETE FROM table;
            tables=expressions
            > DELETE FROM table WHERE expression;
            tables=None
            > DROP TABLE table;
            \033[0m
            """,

            "add_columns":
            """
            \033[1;3m
            takes kwargs
            columns syntax: "col_name DATA_TYPE etc"
            default_values syntax: "'text_value'", "123", "1.23"
            tables=([columns], {columns: default_values})
            > ALTER TABLE table ADD col_name DATA_TYPE etc;
            > ALTER TABLE table ADD col_name DATA_TYPE etc, DEFAULT default_value;
            \033[0m
            """,

            "rename_columns":
            """
            \033[1;3m
            takes kwargs\n
            tables={old_names: new_names}
            > ALTER TABLE table RENAME COLUMN old_name TO new_name;
            \033[0m
            """,

            "delete_columns":
            """
            \033[1;3m
            takes kwargs
            tables=[columns_names]
            > ALTER TABLE table DROP COLUMN column_name;
            \033[0m
            """,

            "insert_values":
            """
            \033[1;3m
            takes kwargs
            values syntax: "'text_value'", "123", "1.23"
            *if not AI col, values in order of columns:
            tables=[values]
            > INSERT INTO table VALUES(values);
            *assign value to specific column:
            tables={column: value}
            > INSERT INTO table columns VALUES(values);
            \033[0m
            """,

            "update_columns_values":
            """
            \033[1;3m
            takes kwargs
            values syntax: "'text_value'", "123", "1.23"
            tables={columns: values}
            > UPDATE table SET column = value;
            \033[0m
            """,

            "get_tables_names":
            """
            \033[1;3m
            takes no arguments
            > SELECT name FROM sqlite_master WHERE type='table';
            returns a list of tables from connected database
            \033[0m
            """,

            "get_columns_names":
            """
            \033[1;3m
            takes args
            > SELECT * FROM table;
            returns a dictionary {table: [columns],...}
            \033[0m
            """
        }
        # using triple quoted string includes redundant tabs
        # so texts have to be formatted before they are ready to be displayed
        self.methods_help_dic = {key: inspect.cleandoc(value)
                                 for key, value in self.methods_help_dic.items()}

    def get_methods(self):
        self.methods_list = [attrib + "()" for attrib in dir(self)
                             if callable(getattr(self, attrib)) and
                             not attrib.startswith("__") and
                             attrib not in self.hidden_methods]
        return self.methods_list

    def get_method_info(self, method):
        return self.methods_help_dic.get(method, "No info for this method.")

    def open(self, database):
        if not self.database:
            self.database = database
        self.conn = sqlite3.connect(self.database)
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
    def create_tables(self, **kwargs: list[str]) -> list | None:
        """
        > CREATE TABLE {table} ({columns});\n
        create_tables(table=["col1 INTEGER", "col2 TEXT"])\n
        or\n
        table_name = "table"\n
        create_tables(**{table_name: ["col1 INTEGER", "col2 TEXT"])

        :return: list of executed commands or None
        """

        try:
            commands = []
            for table, data in kwargs.items():
                columns = ", "
                columns = columns.join(data)

                command = f"CREATE TABLE {table} ({columns});"
                dprint(command)
                self.cur.execute(command)
                commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def clear_tables(self, **kwargs: str) -> list | None:
        """
        if not value but is not None, column is cleared\n
        > DELETE FROM {table}\n
        if value is given and is not None, condition is added\n
        > WHERE {value} (optional);\n
        if value is None, the column is deleted:\n
        > DROP TABLE {table};

        :return: list of executed commands or None
        """
        try:
            commands = []
            for table, value in kwargs.items():
                command = f"DELETE FROM {table}"
                if value:
                    command += f" WHERE {value}"
                elif value is None:
                    command = f"DROP TABLE {table}"
                command += ";"

                dprint(command)
                self.cur.execute(command)
                commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    # manipulate columns
    def add_columns(self, **kwargs) -> list | None:
        """
        > ALTER TABLE {table} ADD {column}, default {default};\n
        table=(["col_name DATA_TYPE"], {"col_name DATA_TYPE": "default_value"})

        :return: list of executed commands or None
        """
        try:
            commands = []
            for table, value in kwargs.items():
                for column in value:
                    command = f"ALTER TABLE {table} ADD {column}"
                    if type(value) is dict:
                        command += f" default {value[column]}"
                    command += ";"

                    dprint(command)
                    self.cur.execute(command)
                    commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None
    # list for columns with no default value, dictionary otherwise

    def rename_columns(self, **kwargs: dict[str: str]) -> list | None:
        """
        > ALTER TABLE {table} RENAME COLUMN {old_col_name} TO {new_col_name};\n
        table={"old_col_name": "new_col_name"}

        :return: list of executed commands or None
        """
        try:
            commands = []
            for table, columns in kwargs.items():
                for old_col_name, new_col_name in columns:
                    command = f"ALTER TABLE {table} RENAME COLUMN {old_col_name} TO {new_col_name};"
                    dprint(command)
                    self.cur.execute(command)
                    commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    # different approach to deleting more than one column
    # https://blog.niklasottosson.com/databases/how-to-drop-a-column-in-sqlite-3/
    def delete_columns(self, **kwargs: list[str]) -> list | None:
        """
        > ALTER TABLE {table} DROP COLUMN {column};\n
        table=[columns]

        :return: list of executed commands or None
        """
        try:
            commands = []
            for table, columns in kwargs.items():
                for column in columns:
                    command = f"ALTER TABLE {table} DROP COLUMN {column};"
                    dprint(command)
                    self.cur.execute(command)
                    commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    # manipulate values
    def insert_values(self, **kwargs) -> list | None:
        """
        > INSERT INTO {table} {columns}VALUES({values});\n
        table=[values]\n
        or\n
        table={columns: values}\n
        column names syntax: "column_name"\n
        values syntax: "'text_value'"

        :return: list of executed commands or None
        """
        # dictionary if you specify column, list in order of columns otherwise
        # you cannot use list if there is AI column in table
        try:
            commands = []
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
                commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    # for more complex updating (with where, order, etc)
    # TODO: one command for multiple columns in one table
    # https://www.sqlitetutorial.net/sqlite-update/

    def update_columns_values(self, **kwargs: dict[str: str]) -> list | None:
        """
        > UPDATE {table} SET {column} = {value};\n
        table={"column": "'value'"}

        :return: list of executed commands or None
        """
        try:
            commands = []
            for table, columns in kwargs.items():
                for column, value in columns.items():
                    command = f"UPDATE {table} SET {column} = {value};"
                    dprint(command)
                    self.cur.execute(command)
                    commands.append(command)
            return commands
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    # read data, print if commmand_help
    # TODO: documentation and help for getters
    def get_tables_names(self) -> list | None:
        """
        :return: tables list or None
        """
        try:
            tables = []
            command = f"SELECT name FROM sqlite_master WHERE type='table';"
            self.cur.execute(command)
            for table in self.cur.fetchall():
                tprint(table[0])
                tables.append(table[0])
            return tables
        except sqlite3.OperationalError as err:
            dprint(err)
        return None

    def get_columns_names(self, *args) -> dict | None:
        """
        :param args: table name
        :return: tables dictionary with columns lists as values or None
        """
        try:
            tables = {}
            for table in args:
                columns = []
                command = f"SELECT * FROM {table};"
                self.cur = self.conn.execute(command)
                for column in list(map(lambda x: x[0], self.cur.description)):
                    tprint(column)
                    columns.append(column)
                tables[table] = columns
            return tables
        except sqlite3.OperationalError as err:
            dprint(err)
        return None


start_space = ""
def tprint(*args, **kwargs):
    print(start_space, end="")
    print(*args, **kwargs)
    return


if __name__ == '__main__':

    data_base = DBMSTranslator()
    data_base.open("tic-tac-toe-plus.db")
    methods_menu_list = [f"{index}. {method}" for index, method in enumerate(data_base.get_methods(), 1)]

    symbols = {
        "left": "[",
        "right": "]",
        "sep": "-",
        "info_left": "<",
        "info_right": ">"
    }

    menu_title = symbols['info_left'] + " {} " + symbols['info_right']
    menu_header = symbols['left'] + "{}" + symbols['right']

    menu_info = menu_title.format("METHODS")
    help_info = menu_title.format("HELP")

    help_menu = {
        "help": ("!h", "{} for !commands help"),
        "method_info": ("!i", "{} method_name for info about method"),
        "clear": ("!c", "{} to switch terminal window clearing"),
        "exit": ("!e", "{} to exit"),
        "start_space": ("!s", "{} to switch a whitespace before each line")
    }

    spaces = ["", " ", "\t"]

    run_flag = True
    clear_flag = False
    help_flag = False
    start_space_index = 0
    start_space = spaces[start_space_index]

    while run_flag:
        if clear_flag:
            os.system('cls')

        if help_flag:
            help_menu_list = [help_menu[option][1].format(help_menu[option][0]) for option in help_menu]
            max_width = max(len(indexed_method) for indexed_method in methods_menu_list + help_menu_list)
        else:
            max_width = max(len(indexed_method) for indexed_method in methods_menu_list)

        tprint(menu_header.format(menu_info.center(max_width - 2, symbols['sep'])))
        for indexed_method in methods_menu_list:
            tprint(indexed_method)
        if help_flag:
            tprint(menu_header.format(help_info.center(max_width - 2, symbols['sep'])))
            for option in help_menu:
                tprint(help_menu[option][1].format(help_menu[option][0]))
            help_flag = False
        else:
            tprint(f"{len(methods_menu_list) + 1}. {help_menu['help'][1].format(help_menu['help'][0])}")

        cmd = input(f"{start_space}> ")
        try:
            if cmd:
                if cmd.lower() in list(zip(*help_menu.values()))[0]:  # is recognized as menu command
                    if cmd.lower() == help_menu["help"][0]:
                        help_flag = True
                    elif cmd.lower() == help_menu["exit"][0]:
                        run_flag = False
                    elif cmd.lower() == help_menu["clear"][0]:
                        if clear_flag:
                            clear_flag = False
                        else:
                            clear_flag = True
                    elif cmd.lower() == help_menu["start_space"][0]:
                        start_space_index = (start_space_index + 1) % len(spaces)
                        start_space = spaces[start_space_index]
                elif cmd.lower().startswith(help_menu['method_info'][0]):
                    method_name = cmd.lower().strip(help_menu["method_info"][0]).strip("()").strip()
                    tprint(data_base.get_method_info(method_name))
                else:  # is not recognized as menu command
                    exec("data_base." + cmd)

        except sqlite3.OperationalError as oper:
            tprint(oper)
        except AttributeError as atrer:
            tprint(atrer)
        except SyntaxError as stxer:
            tprint(stxer)
        except TypeError as tper:
            tprint(tper)
        if run_flag:
            if clear_flag:
                if not help_flag:
                    input(f"{start_space}...")
            else:
                print()
    data_base.delete_columns(user=["user_00"])

    data_base.close()
