
dev = True


def dprint(*args, **kwargs):
    if dev:
        print(*args, **kwargs)
    return dev


if __name__ == '__main__' and dev:
    columns = [1, 2, 3, 4, 5]
    dprint(str(columns)[1:-1])
