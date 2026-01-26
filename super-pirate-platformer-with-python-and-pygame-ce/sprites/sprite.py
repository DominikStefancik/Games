from settings import pygame, TILE_SIZE

class Sprite(pygame.sprite.Sprite):
    def __init__(self, groups, surface, position):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("white")
        self.rect = self.image.get_frect(topleft = position)
        self.previous_rect = self.rect.copy()
