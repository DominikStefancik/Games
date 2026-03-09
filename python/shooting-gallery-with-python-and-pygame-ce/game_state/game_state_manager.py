import pygame

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import AudioAsset
from timer import Timer

from .constants import (
    MAX_BULLETS,
    ROUND_DIFFICULTY_MULTIPLIER,
    ROUND_FINISHED_DELAY,
    ROUND_START_DELAY,
    ROUNDS_COUNT,
)
from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_round = 1
        self._round_difficulty = 1
        self.static_sprites = pygame.sprite.Group()
        self.brown_duck_sprites = pygame.sprite.Group()
        self.yellow_duck_sprites = pygame.sprite.Group()
        self.score = 0
        self._remaining_bullets_count = MAX_BULLETS
        self._start_round_timer = Timer(
            duration=ROUND_START_DELAY, repeat=False, autostart=True
        )
        self._round_finished_timer = Timer(duration=ROUND_FINISHED_DELAY)
        self._subscribers = []

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def current_round(self):
        return self._current_round

    @property
    def round_difficulty(self):
        return self._round_difficulty

    @property
    def remaining_bullets_count(self):
        return self._remaining_bullets_count

    @remaining_bullets_count.setter
    def remaining_bullets_count(self, value):
        self._remaining_bullets_count = value

        if self.remaining_bullets_count == 0:
            if self._current_round != ROUNDS_COUNT:
                self._game_state = GameState.ROUND_FINISHED
                self._round_finished_timer.activate()
            else:
                self._game_state = GameState.GAME_OVER
                self.static_sprites.empty()

                asset_manager = get_asset_manager()
                asset_manager.sounds[AudioAsset.FUN_FAIR].stop()
                asset_manager.sounds[AudioAsset.GAME_OVER].play()

    def move_to_next_level(self):
        self.brown_duck_sprites.empty()
        self.yellow_duck_sprites.empty()

        self._current_round += 1
        self._round_difficulty *= ROUND_DIFFICULTY_MULTIPLIER
        self._remaining_bullets_count = MAX_BULLETS
        self.notify_all_restart()
        self._game_state = GameState.WAITING_TO_START
        self._start_round_timer.activate()

    def restart(self):
        self.brown_duck_sprites.empty()
        self.yellow_duck_sprites.empty()

        self._current_round = 1
        self._round_difficulty = 1
        self._remaining_bullets_count = MAX_BULLETS
        self.notify_all_restart()
        self._game_state = GameState.WAITING_TO_START
        self._start_round_timer.activate()

    def update(self):
        self._start_round_timer.update()
        self._round_finished_timer.update()

        pygame.mouse.set_visible(self._game_state == GameState.GAME_OVER)

        if (
            self._game_state == GameState.WAITING_TO_START
            and not self._start_round_timer.active
        ):
            self._game_state = GameState.RUNNING
        elif (
            self._game_state == GameState.ROUND_FINISHED
            and not self._round_finished_timer.active
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
