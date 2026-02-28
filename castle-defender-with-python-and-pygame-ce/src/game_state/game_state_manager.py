from enemy.constants import EnemyType

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self._current_level = 1
        self._last_level = 1
        self._level_difficulty = 0
        self._enemy_difficulty = 1000
        self.score = 0
        self.money = 0

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

    def move_to_next_level(self):
        pass

    def update_after_enemy_dead(self, enemy_type):
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
        level_is_won = False

        return level_is_won

    def is_game_won(self):
        if self._current_level == self._last_level:
            if self.is_current_level_won():
                self._game_state = GameState.GAME_WON

    def reached_level_difficulty(self):
        return self._level_difficulty >= self._enemy_difficulty


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
