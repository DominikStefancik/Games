import pygame

from input_manager import get_input_manager
from timer import Timer

from game_state.constants import GAME_FINISHED_DELAY, GAME_START_DELAY

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self.input_manager = get_input_manager()
        self._game_state = GameState.WAITING_TO_START
        self._start_game_timer = Timer(
            duration=GAME_START_DELAY, repeat=False, autostart=True
        )
        self._game_finished_timer = Timer(duration=GAME_FINISHED_DELAY)

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    def restart(self):
        pass

    def update(self):
        self._start_game_timer.update()
        self._game_finished_timer.update()

        pygame.mouse.set_visible(self._game_state == GameState.GAME_FINISHED)

        if (
            self._game_state == GameState.WAITING_TO_START
            and not self._start_game_timer.active
        ):
            self._game_state = GameState.PREPARING_SHOT

        if (
            self._game_state == GameState.PREPARING_SHOT
            and self.input_manager.left_mouse_clicked
        ):
            self._game_state = GameState.POWERING_UP

        if (
            self._game_state == GameState.POWERING_UP
            and self.input_manager.left_mouse_released
        ):
            self._game_state = GameState.TAKING_SHOT


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
