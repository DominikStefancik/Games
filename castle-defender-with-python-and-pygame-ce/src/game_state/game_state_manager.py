from enemy.constants import EnemyType

from .game_state import GameState


class GameStateManager:
    def __init__(self):
        self._game_state = GameState.WAITING_TO_START
        self.score = 0
        self.money = 0

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, value):
        self._game_state = value

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


GAME_STATE_MANAGER = GameStateManager()


def get_game_state_manager():
    return GAME_STATE_MANAGER
