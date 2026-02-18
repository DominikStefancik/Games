from levels.constants import Level
from levels.level1.layout import level1_layout
from levels.level1.config import LEVEL_1_CONFIG


class GameStateManager:
    def __init__(self):
        self._current_level = Level.LEVEL_1
        self.score = 0
        self.lives = 3

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


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
