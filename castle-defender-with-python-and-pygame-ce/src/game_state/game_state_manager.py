from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
