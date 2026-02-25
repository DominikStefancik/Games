from enum import Enum


class GameState(Enum):
    WAITING_TO_START = "waiting_to_start"
    RUNNING = "running"
    GAME_WON = "game_won"
    GAME_OVER = "game_over"
