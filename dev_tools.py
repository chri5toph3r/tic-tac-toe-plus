
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
    columns = [1, 2, 3, 4, 5]
    dprint(str(columns)[1:-1])
