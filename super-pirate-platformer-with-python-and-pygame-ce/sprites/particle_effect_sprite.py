from settings import pygame, Z_Layer

from .animated_sprite import AnimatedSprite


class ParticleEffectSprite(AnimatedSprite):
    def __init__(self, groups, position, animation_frames):
        super().__init__(groups, position, animation_frames)

        self.rect.center = position
        self.z_index = Z_Layer.FOREGROUND.value

    # For this sprite type we want the animation play only once and after it is finished,
    # we want to destroy the sprite
    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time

        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

    def update(self, delta_time):
        self.animate(delta_time)
