from settings import pygame, Z_Layer

from .animated_sprite import AnimatedSprite
from .constants import ItemType
from .particle_effect_sprite import ParticleEffectSprite


class Item(AnimatedSprite):
    def __init__(
        self,
        groups,
        item_type,
        position,
        animation_frames,
        particle_groups,
        particle_effect_animation_frames,
        player,
    ):
        super().__init__(groups, position, animation_frames)

        self.rect.center = position
        self.type = ItemType.from_str(item_type)
        self.particle_groups = particle_groups
        self.particle_effect_animation_frames = particle_effect_animation_frames
        self.player = player
        self.z_index = Z_Layer.FOREGROUND.value

    def detect_collision(self):
        if pygame.sprite.collide_mask(self, self.player):
            # When the player collides with the item, we want to create a particle effect first
            ParticleEffectSprite(
                groups=self.particle_groups,
                position=self.rect.center,
                animation_frames=self.particle_effect_animation_frames,
            )
            self.kill()

    def update(self, delta_time):
        self.detect_collision()
