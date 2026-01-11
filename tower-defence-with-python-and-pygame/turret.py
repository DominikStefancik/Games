import constants
import pygame


class Turret(pygame.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y) -> None:
        # We have to call the superclass' init method
        pygame.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y
        # The calculation of X and Y coordinates is done so the turret is placed
        # in the middle of a tile
        self.x = (self.tile_x + 0.5) * constants.TILE_SIZE
        self.y = (self.tile_y + 0.5) * constants.TILE_SIZE
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
