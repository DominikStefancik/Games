import time


class GameInfo:
    ROUNDS = 10

    def __init__(self, round=1):
        self.round = round
        self.round_started = False
        self.round_start_time = 0

    def next_round(self):
        self.round += 1
        self.round_started = False

    def reset_game(self):
        self.round = 1
        self.round_started = False
        self.round_start_time = 0

    def is_game_finished(self):
        return self.round > self.ROUNDS

    def start_round(self):
        self.round_started = True
        self.round_start_time = time.time()

    def get_round_time(self):
        if not self.round_started:
            return 0

        return round(time.time() - self.round_start_time)
