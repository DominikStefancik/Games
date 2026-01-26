from enum import Enum

PLAYER_SPEED = 200
PLAYER_GRAVITY = 300

class Collision(Enum):
    VERTICAL = "vertical",
    HORIZONTAL = "horizontal"
