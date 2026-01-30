from game_state import get_game_state
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
            self.activate()
            # When the player collides with the item, we want to create a particle effect first
            ParticleEffectSprite(
                groups=self.particle_groups,
                position=self.rect.center,
                animation_frames=self.particle_effect_animation_frames,
            )
            self.kill()

    def activate(self):
        game_state = get_game_state()

        if self.type == ItemType.SILVER:
            game_state.collected_coins += 1
        if self.type == ItemType.GOLD:
            game_state.collected_coins += 5
        if self.type == ItemType.DIAMOND:
            game_state.collected_coins += 20
        if self.type == ItemType.SKULL:
            game_state.collected_coins += 50
        if self.type == ItemType.POTION:
            game_state.player_health += 1

    def update(self, delta_time):
        self.detect_collision()
