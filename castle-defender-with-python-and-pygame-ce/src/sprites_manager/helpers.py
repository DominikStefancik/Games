from random import choice

from asset_manager.constants import ImageAssetGroup
from enemy.constants import EnemyType
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
    vertical_position = choice(
        [WINDOW_HEIGHT - 160, WINDOW_HEIGHT - 200, WINDOW_HEIGHT - 240]
    )

    return Enemy(
        group=group,
        animation_frames=asset_manager.graphics[map_image_group(enemy_type)],
        type=enemy_type,
        position=(-50, vertical_position),
    )


def map_image_group(enemy_type):
    match enemy_type:
        case EnemyType.KNIGHT:
            return ImageAssetGroup.KNIGHT
        case EnemyType.GOBLIN:
            return ImageAssetGroup.GOBLIN
        case EnemyType.RED_GOBLIN:
            return ImageAssetGroup.RED_GOBLIN
        case EnemyType.PURPLE_GOBLIN:
            return ImageAssetGroup.PURPLE_GOBLIN
