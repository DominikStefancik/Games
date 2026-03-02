from helpers import scale_image

from .constants import ENEMY_FRAME_SCALE, EnemyType


def get_enemy_health(enemy_type):
    match enemy_type:
        case EnemyType.KNIGHT:
            return 75
        case EnemyType.GOBLIN:
            return 100
        case EnemyType.RED_GOBLIN:
            return 125
        case EnemyType.PURPLE_GOBLIN:
            return 150


def scale_animation_frames(animation_frames):
    scaled_animation_frames = {}

    for key in animation_frames.keys():
        original_frames = animation_frames[key]
        scaled_frames = []

        for frame in original_frames:
            scaled_frame = scale_image(frame, ENEMY_FRAME_SCALE)
            scaled_frames.append(scaled_frame)

        scaled_animation_frames[key] = scaled_frames

    return scaled_animation_frames
