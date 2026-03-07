import pygame


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)

        self.display_surface = pygame.display.get_surface()
        self.image = image
        self.rect = self.image.get_frect()

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)

    def draw(self):
        self.display_surface.blit(self.image, (self.rect.centerx, self.rect.centery))
