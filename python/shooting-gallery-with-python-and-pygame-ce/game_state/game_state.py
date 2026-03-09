from enum import Enum


class GameState(Enum):
    WAITING_TO_START = "waiting_to_start"
    RUNNING = "running"
    ROUND_FINISHED = "round_finished"
    GAME_OVER = "game_over"
