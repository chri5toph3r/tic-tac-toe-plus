import time
from dev_tools import dprint, dev
from SQLtranslator import DBMSTranslator


class Timer:
    def __init__(self):
        super().__init__()
        self.timer = 0
        self.times_sum = 0
        self.log_list = []

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


class Statistics(DBMSTranslator, Timer):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    pass
