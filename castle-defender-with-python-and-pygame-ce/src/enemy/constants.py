from enum import Enum

from settings import Vector2, WINDOW_HEIGHT


class EnemyType(Enum):
    KNIGHT = "knight"
    GOBLIN = "goblin"
    RED_GOBLIN = "red_goblin"
    PURPLE_GOBLIN = "purple_goblin"


class EnemyAnimation(Enum):
    WALK = "walk"
    ATTACK = "attack"
    DEATH = "death"


class EnemyLine(Enum):
    UP = WINDOW_HEIGHT - 240
    MIDDLE = WINDOW_HEIGHT - 200
    DOWN = WINDOW_HEIGHT - 160


class EnemyLineOffset(Enum):
    UP = 0
    MIDDLE = 10
    DOWN = 20


ENEMY_FRAME_SCALE = 0.2
ENEMY_SPEED = 50
ENEMY_ANIMATION_SPEED = 10
ENEMY_DRAW_OFFSET = Vector2(-10, -12)
ENEMY_ATTACK_DAMAGE = 25
ENEMY_ATTACK_COOLDOWN_INTERVAL = 1000
