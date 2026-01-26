from enum import Enum

PLAYER_SPEED = 200
PLAYER_GRAVITY = 300
PLAYER_JUMP_HEIGHT = 400

class Collision(Enum):
    VERTICAL = "vertical",
    HORIZONTAL = "horizontal"

class SurfaceContact(Enum):
    FLOOR = "floor",
    LEFT = "left"
    RIGHT = "right"

class PlayerTimerType(Enum):
    WALL_JUMP = "wall_jump"
    WALL_SLIDE_BLOCK = "wall_slide_block"
