from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from copy import deepcopy
from levels.constants import BoardTile, Level
from levels.level1.config import LEVEL_1_CONFIG
from levels.level1.layout import LEVEL_1_LAYOUT
from levels.level2.config import LEVEL_2_CONFIG
from levels.level2.layout import LEVEL_2_LAYOUT

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = Level.LEVEL_1
        self._last_level = Level.LEVEL_2
        self.score = 0
        self.lives = 3
        self._subscribers = []
        self._level_layouts = {Level.LEVEL_1: None, Level.LEVEL_2: None}

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

        if self._game_state == GameState.WAITING_TO_START:
            self.notify_all_restart()

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value

        if self._lives < 0:
            self._game_state = GameState.GAME_OVER
            asset_manager = get_asset_manager()
            asset_manager.sounds[AudioAsset.GAME_OVER].play()

    @property
    def current_level(self):
        return self._current_level

    def move_to_next_level(self):
        if self._current_level != self._last_level:
            match self._current_level:
                case Level.LEVEL_1:
                    self._current_level = Level.LEVEL_2

            self.game_state = GameState.WAITING_TO_START
            self.notify_all_recreate()

    def get_level_config(self):
        config = LEVEL_1_CONFIG

        match self._current_level:
            case Level.LEVEL_1:
                config = LEVEL_1_CONFIG
            case Level.LEVEL_2:
                config = LEVEL_2_CONFIG

        return config

    def get_level_layout(self):
        layout = None

        match self._current_level:
            case Level.LEVEL_1:
                if self._level_layouts[Level.LEVEL_1] == None:
                    self._level_layouts[Level.LEVEL_1] = deepcopy(LEVEL_1_LAYOUT)

                layout = self._level_layouts[Level.LEVEL_1]
            case Level.LEVEL_2:
                if self._level_layouts[Level.LEVEL_2] == None:
                    self._level_layouts[Level.LEVEL_2] = deepcopy(LEVEL_2_LAYOUT)

                layout = self._level_layouts[Level.LEVEL_2]

        return layout

    def restart_game(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = Level.LEVEL_1
        self.score = 0
        self.lives = 3

        for key in self._level_layouts.keys():
            self._level_layouts[key] = None

        self.notify_all_recreate()

    def is_current_level_won(self):
        level_is_won = True

        for row in self._level_layouts[self._current_level]:
            if BoardTile.DOT.value in row or BoardTile.BIG_DOT.value in row:
                level_is_won = False

        return level_is_won

    def is_game_won(self):
        if (
            self._current_level == self._last_level
            and self._level_layouts[self._current_level]
        ):
            if self.is_current_level_won():
                self._game_state = GameState.GAME_WON

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all_restart(self):
        for subscriber in self._subscribers:
            subscriber.restart_all()

    def notify_all_recreate(self):
        for subscriber in self._subscribers:
            subscriber.recreate_all()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
