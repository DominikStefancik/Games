from settings import pygame, Z_Layer


class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position, z_index=Z_Layer.MAIN.value):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft=position)
        self.previous_rect = self.rect.copy()
        self.z_index = z_index
