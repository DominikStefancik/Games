from settings import get_time

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._start_time = 0
        self._score = 0
        self._subscribers = []

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

        if self._game_state == GameState.RUNNING:
            self._start_time = get_time()
            self.notify_all()

    @property
    def score(self):
        return self._score

    def update_score(self):
        self._score = int(get_time() - self._start_time)

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all(self):
        for subscriber in self._subscribers:
            subscriber.update_items()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
