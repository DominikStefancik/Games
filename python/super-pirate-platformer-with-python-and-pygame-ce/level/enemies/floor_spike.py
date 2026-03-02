from settings import pygame
from sprites.animated_sprite import AnimatedSprite


class FloorSpike(AnimatedSprite):
    def __init__(self, groups, position, animation_frames, is_inverted):
        if is_inverted:
            frames = [
                pygame.transform.flip(surface, False, True)
                for surface in animation_frames
            ]
        else:
            frames = animation_frames

        super().__init__(groups, position, frames)
