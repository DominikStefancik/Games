import time


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.level_started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        self.level_started = False

    def reset_game(self):
        self.level = 1
        self.level_started = False
        self.level_start_time = 0

    def is_game_finished(self):
        return self.level > self.LEVELS

    def start_level(self):
        self.level_started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.level_started:
            return 0

        return round(time.time() - self.level_start_time)
