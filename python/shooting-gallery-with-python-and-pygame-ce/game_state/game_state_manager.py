import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from timer import Timer

from .constants import (
    LEVEL_DIFFICULTY_MULTIPLIER,
    LEVEL_FINISHED_DELAY,
    LEVEL_START_DELAY,
    LEVELS_COUNT,
    MAX_BULLETS,
)
from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = 1
        self._level_difficulty = 1
        self.static_sprites = pygame.sprite.Group()
        self.brown_duck_sprites = pygame.sprite.Group()
        self.yellow_duck_sprites = pygame.sprite.Group()
        self.score = 0
        self._remaining_bullets_count = MAX_BULLETS
        self._start_level_timer = Timer(
            duration=LEVEL_START_DELAY, repeat=False, autostart=True
        )
        self._level_finished_timer = Timer(duration=LEVEL_FINISHED_DELAY)
        self._subscribers = []

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def current_level(self):
        return self._current_level

    @property
    def level_difficulty(self):
        return self._level_difficulty

    @property
    def remaining_bullets_count(self):
        return self._remaining_bullets_count

    @remaining_bullets_count.setter
    def remaining_bullets_count(self, value):
        self._remaining_bullets_count = value

        if self.remaining_bullets_count == 0:
            if self._current_level != LEVELS_COUNT:
                self._game_state = GameState.LEVEL_FINISHED
            else:
                self._game_state = GameState.GAME_OVER
                self.static_sprites.empty()

                asset_manager = get_asset_manager()
                asset_manager.sounds[AudioAsset.FUN_FAIR].stop()
                asset_manager.sounds[AudioAsset.GAME_OVER].play()

    def move_to_next_level(self):
        self.brown_duck_sprites.empty()
        self.yellow_duck_sprites.empty()

        self._current_level += 1
        self._level_difficulty *= LEVEL_DIFFICULTY_MULTIPLIER
        self._remaining_bullets_count = MAX_BULLETS
        self.notify_all_restart()
        self._game_state = GameState.WAITING_TO_START
        self._start_level_timer.activate()

    def restart(self):
        self.brown_duck_sprites.empty()
        self.yellow_duck_sprites.empty()

        self._current_level = 1
        self._level_difficulty = 1
        self._remaining_bullets_count = MAX_BULLETS
        self.notify_all_restart()
        self._game_state = GameState.WAITING_TO_START
        self._start_level_timer.activate()

    def update(self):
        self._start_level_timer.update()
        self._level_finished_timer.update()

        pygame.mouse.set_visible(self._game_state == GameState.GAME_OVER)

        if (
            self._game_state == GameState.WAITING_TO_START
            and not self._start_level_timer.active
        ):
            self._game_state = GameState.RUNNING
        elif (
            self._game_state == GameState.LEVEL_FINISHED
            and not self._level_finished_timer.active
        ):
            self.move_to_next_level()

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all_restart(self):
        for subscriber in self._subscribers:
            subscriber.restart()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
