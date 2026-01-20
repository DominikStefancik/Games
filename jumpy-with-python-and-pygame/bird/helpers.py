from .constants import BIRD_FRAME_SCALE, BIRD_START_FLYING_ONCE_THRESHOLD, BIRD_START_ROTATING_THRESHOLD
from .bird import Bird


def create_bird(sprite_sheet, current_score):
    if current_score > BIRD_START_ROTATING_THRESHOLD:
        return Bird(sprite_sheet, 100, BIRD_FRAME_SCALE, True)

    if current_score > BIRD_START_FLYING_ONCE_THRESHOLD:
        return Bird(sprite_sheet, 100, BIRD_FRAME_SCALE, False)
