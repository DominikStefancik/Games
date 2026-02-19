from levels.constants import Level
from levels.level1.layout import level1_layout
from levels.level1.config import LEVEL_1_CONFIG

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = Level.LEVEL_1
        self.score = 0
        self.lives = 3
        self._subscribers = []

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

        if self._game_state == GameState.WAITING_TO_START:
            self.notify_all()

    def get_level_config(self):
        config = LEVEL_1_CONFIG

        match self._current_level:
            case Level.LEVEL_1:
                config = LEVEL_1_CONFIG

        return config

    def get_level_layout(self):
        layout = level1_layout

        match self._current_level:
            case Level.LEVEL_1:
                layout = level1_layout

        return layout

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all(self):
        for subscriber in self._subscribers:
            subscriber.update_state()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
