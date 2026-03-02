from random import choice

from asset_manager.constants import ImageAssetGroup
from enemy.constants import EnemyLine, EnemyType
from enemy.enemy import Enemy
from settings import WINDOW_HEIGHT


def get_random_enemy(group, asset_manager):
    enemy_type = choice(
        [
            EnemyType.KNIGHT,
            EnemyType.GOBLIN,
            EnemyType.RED_GOBLIN,
            EnemyType.PURPLE_GOBLIN,
        ]
    )
    enemy_line = choice([EnemyLine.DOWN, EnemyLine.MIDDLE, EnemyLine.UP])

    return Enemy(
        group=group,
        animation_frames=asset_manager.graphics[map_enemy_type(enemy_type)],
        type=enemy_type,
        position=(-50, enemy_line.value),
        line=enemy_line,
    )


def map_enemy_type(enemy_type):
    match enemy_type:
        case EnemyType.KNIGHT:
            return ImageAssetGroup.KNIGHT
        case EnemyType.GOBLIN:
            return ImageAssetGroup.GOBLIN
        case EnemyType.RED_GOBLIN:
            return ImageAssetGroup.RED_GOBLIN
        case EnemyType.PURPLE_GOBLIN:
            return ImageAssetGroup.PURPLE_GOBLIN
