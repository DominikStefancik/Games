from helpers import scale_image
from settings import pygame

from .constants import ButtonEvent


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, position, scale, event):
        super().__init__(group)

        self.image = scale_image(image, scale)
        self.rect = self.image.get_frect(topleft=position)
        self.event = event

    def detect_collisions(self):
        if pygame.mouse.get_just_pressed()[0] == 1:
            mouse_position = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_position):
                pygame.event.post(pygame.event.Event(self.event.value))

    def update(self):
        self.detect_collisions()
