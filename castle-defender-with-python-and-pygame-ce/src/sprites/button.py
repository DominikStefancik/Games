from helpers import scale_image
from settings import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, position, scale):
        super().__init__(group)

        self.image = scale_image(image, scale)
        self.rect = self.image.get_frect(topleft=position)
        self.is_clicked = False

    def detect_collisions(self):
        if pygame.mouse.get_pressed()[0] == 1:
            mouse_position = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_position):
                self.is_clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.is_clicked = False

    def update(self):
        self.detect_collisions()
