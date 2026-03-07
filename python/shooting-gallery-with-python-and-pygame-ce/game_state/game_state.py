from enum import Enum


class GameState(Enum):
    WAITING_TO_START = "waiting_to_start"
    RUNNING = "running"
    LEVEL_FINISHED = "level_finished"
    GAME_OVER = "game_over"
