from player.constants import PLAYER_START_HEALTH


class GameState:
    def __init__(self):
        self.subscribers = []
        self._collected_coins = 0
        self._player_health = PLAYER_START_HEALTH

    @property
    def collected_coins(self):
        return self._collected_coins

    @collected_coins.setter
    def collected_coins(self, value):
        self._collected_coins = value

        if self._collected_coins >= 100:
            self._player_health += 1
            self._collected_coins -= 100

        self.notify_all()

    @property
    def player_health(self):
        return self._player_health

    @player_health.setter
    def player_health(self, value):
        self._player_health = value
        self.notify_all()

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def notify_all(self):
        for subscriber in self.subscribers:
            subscriber.refresh(self)


GAME_STATE = GameState()


def get_game_state():
    return GAME_STATE
