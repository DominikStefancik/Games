from settings import pygame


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing sprites
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

    def update(self):
        delta_time = self.clock.tick() / 1000

        self.all_sprites.update(delta_time)

    def draw(self):
        self.all_sprites.draw(self.display_surface)
