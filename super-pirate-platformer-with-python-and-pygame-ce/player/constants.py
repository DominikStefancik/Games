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
    WALL_JUMP = "wall jump"
    WALL_SLIDE_BLOCK = "wall slide block"
    PLATFORM_FALL_DOWN = "platform fall down"
