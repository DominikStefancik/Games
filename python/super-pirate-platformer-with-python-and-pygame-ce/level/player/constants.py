from enum import Enum

PLAYER_SPEED = 200
PLAYER_GRAVITY = 300
PLAYER_JUMP_HEIGHT = 400
PLAYER_START_HEALTH = 5


class Collision(Enum):
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"


class SurfaceContact(Enum):
    FLOOR = "floor"
    LEFT = "left"
    RIGHT = "right"


class PlayerTimerType(Enum):
    WALL_JUMP = "wall jump"
    WALL_SLIDE_BLOCK = "wall slide block"
    PLATFORM_FALL_DOWN = "platform fall down"
    ATTACK_BLOCK = "attack block"
    GET_DAMAGE = "get_damage"


class PlayerAnimation(Enum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    FALL = "fall"
    WALL = "wall"
    ATTACK = "attack"
    AIR_ATTACK = "air_attack"
