from level.player.constants import PLAYER_START_HEALTH

from .constants import GameStage


class GameState:
    def __init__(self):
        self._current_stage = GameStage.LEVEL
        self._collected_coins = 0
        self._player_health = PLAYER_START_HEALTH
        self._current_level = 0
        self._unlocked_level = 0

        self._stage_subscribers = []
        self._ui_subscribers = []

    @property
    def current_stage(self):
        return self._current_stage

    def switch_stage(self, target, unlocked_level=0):
        if target == GameStage.OVERWORLD:
            if unlocked_level > 0:
                self._unlocked_level = unlocked_level
            else:
                self._player_health -= 1
            self._current_stage = GameStage.OVERWORLD
        else:
            self._current_stage = GameStage.LEVEL

        self.notify_all_stage()
        self.notify_all_ui()

    @property
    def collected_coins(self):
        return self._collected_coins

    @collected_coins.setter
    def collected_coins(self, value):
        self._collected_coins = value

        if self._collected_coins >= 100:
            self._player_health += 1
            self._collected_coins -= 100

        self.notify_all_ui()

    @property
    def player_health(self):
        return self._player_health

    @player_health.setter
    def player_health(self, value):
        self._player_health = value
        self.notify_all_ui()

    @property
    def current_level(self):
        return self._current_level

    @player_health.setter
    def current_level(self, value):
        self._current_level = value

    @property
    def unlocked_level(self):
        return self._unlocked_level

    def subscribe_ui(self, subscriber):
        self._ui_subscribers.append(subscriber)

    def notify_all_ui(self):
        for subscriber in self._ui_subscribers:
            subscriber.refresh(self)

    def subscribe_stage(self, subscriber):
        self._stage_subscribers.append(subscriber)

    def notify_all_stage(self):
        for subscriber in self._stage_subscribers:
            subscriber.update_stage()


GAME_STATE = GameState()


def get_game_state():
    return GAME_STATE
