from enum import Enum


class EnemyType(Enum):
    KNIGHT = "knight"
    GOBLIN = "goblin"
    RED_GOBLIN = "red_goblin"
    PURPLE_GOBLIN = "purple_goblin"


class EnemyAnimation(Enum):
    WALK = "walk"
    ATTACK = "attack"
    DEATH = "death"


ENEMY_FRAME_SCALE = 0.2
ENEMY_SPEED = 50
ENEMY_ANIMATION_SPEED = 10
