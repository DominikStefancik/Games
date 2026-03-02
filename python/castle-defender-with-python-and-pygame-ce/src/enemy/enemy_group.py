from settings import pygame, Vector2

from .constants import ENEMY_DRAW_OFFSET


# We created this class so we can ovewrite the "draw" method and define
# how all sprites should be drawn.
class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def draw(self):
        # Because this class inherits from "pygame.sprite.Group",
        # the "self" returns all sprites contained in this group
        for sprite in self:
            draw_position = sprite.rect.topleft + ENEMY_DRAW_OFFSET
            self.display_surface.blit(sprite.image, draw_position)
