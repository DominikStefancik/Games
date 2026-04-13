from enum import Enum


class GameState(Enum):
    WAITING_TO_START = "waiting_to_start"
    TAKING_SHOT = "taking_shot"
    BALLS_MOVING = "balls_moving"
    GAME_FINISHED = "game_finished"
