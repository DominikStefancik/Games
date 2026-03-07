import pygame

from .constants import MAX_BULLETS
from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = 1
        self.all_sprites = pygame.sprite.Group()
        self.brown_duck_sprites = pygame.sprite.Group()
        self.yellow_duck_sprites = pygame.sprite.Group()
        self.score = 0
        self.remaining_bullets_count = MAX_BULLETS

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

    @property
    def current_level(self):
        return self._current_level

    def move_to_next_level(self):
        pass

    def is_current_level_won(self):
        pass

    def restart(self):
        pass

    def update(self):
        is_mouse_cursor_visible = self._game_state in [
            GameState.GAME_WON,
            GameState.GAME_OVER,
        ]
        pygame.mouse.set_visible(is_mouse_cursor_visible)


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
