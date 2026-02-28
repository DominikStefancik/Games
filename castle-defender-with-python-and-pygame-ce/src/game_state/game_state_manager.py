from enemy.constants import EnemyType
from timer import Timer

from .constants import (
    CASTLE_STARTING_HEALTH,
    LEVEL_DIFFICULTY_MULTIPLIER,
    LEVEL_START_DELAY,
    LEVEL_WON_DELAY,
)
from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = 1
        self._level_difficulty = 0
        self._enemy_difficulty = 1000
        self._alive_enemies = 0
        self._subscribers = []
        self._start_level_timer = Timer(
            duration=LEVEL_START_DELAY, repeat=False, autostart=True
        )
        self._level_won_timer = Timer(duration=LEVEL_WON_DELAY)
        self.score = 0
        self.best_score = 0
        self.money = 0
        self.health = CASTLE_STARTING_HEALTH
        self.max_health = CASTLE_STARTING_HEALTH

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

    @level_difficulty.setter
    def level_difficulty(self, value):
        self._level_difficulty = value

    @property
    def alive_enemies(self):
        return self._alive_enemies

    @alive_enemies.setter
    def alive_enemies(self, value):
        self._alive_enemies = value

        if self.is_current_level_won():
            self._game_state = GameState.LEVEL_WON
            self._level_won_timer.activate()

    def move_to_next_level(self):
        self._current_level += 1
        self._alive_enemies = 0
        self._level_difficulty = 0
        self._enemy_difficulty *= LEVEL_DIFFICULTY_MULTIPLIER
        self.notify_all_new_level()
        self._game_state = GameState.WAITING_TO_START
        self._start_level_timer.activate()

    def update_after_enemy_died(self, enemy_type):
        self.alive_enemies -= 1

        match enemy_type:
            case EnemyType.KNIGHT:
                self.score += 100
                self.money += 100
            case EnemyType.GOBLIN:
                self.score += 100
                self.money += 100
            case EnemyType.RED_GOBLIN:
                self.score += 100
                self.money += 100
            case EnemyType.PURPLE_GOBLIN:
                self.score += 100
                self.money += 100

    def is_current_level_won(self):
        return self._alive_enemies == 0

    def is_game_won(self):
        if self.is_current_level_won():
            self._game_state = GameState.GAME_WON

    def reached_level_difficulty(self):
        return self._level_difficulty >= self._enemy_difficulty

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notify_all_new_level(self):
        for subscriber in self._subscribers:
            subscriber.new_level()

    def update(self):
        self._start_level_timer.update()
        self._level_won_timer.update()

        if (
            self._game_state == GameState.WAITING_TO_START
            and not self._start_level_timer.active
        ):
            self._game_state = GameState.RUNNING
        elif (
            self._game_state == GameState.LEVEL_WON and not self._level_won_timer.active
        ):
            self.move_to_next_level()


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
