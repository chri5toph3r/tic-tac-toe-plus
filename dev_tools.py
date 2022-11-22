
dev = True
command_help = True


def dprint(*args, **kwargs):
    if dev:
        print(*args, **kwargs)
    return dev


def cprint(*args, **kwargs):
    if command_help:
        print(*args, **kwargs)
    return command_help


if __name__ == '__main__' and dev:
    help_menu = {
        "help": ("!h", "{} for !commands help"),
        "method_info": ("!i", "{} method_name for info about method"),
        "clear": ("!c", "{} to switch terminal window clearing"),
        "exit": ("!e", "{} to exit"),
        "start_space": ("!s", "{} to switch a whitespace before each line")
    }
    dprint()
    for command in help_menu.values():
        dprint(command[0])
