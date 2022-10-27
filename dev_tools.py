
dev = True


def dprint(*args, **kwargs):
    if dev:
        print(*args, **kwargs)
    return dev
