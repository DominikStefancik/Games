import pygame

from constants import WHITE
from .constants import JUMPY_IMAGE_SCALE


class Player:
    def __init__(self, image, starting_position):
        self.image = pygame.transform.scale(image, JUMPY_IMAGE_SCALE)
        self.rectangle_width = 30
        self.rectangle_height = 40
        # Pygame uses image rectangle for setting up image's starting_position
        # and also to detect collision of the image with other objects
        #
        # Rather than creating a rectangle from the image, we create it manually.
        # The reason is if we created it from the image with "self.image.get_rect()" Pygame would create a rectangle
        # in which the whole image would fit.
        # However, it would be too big and there would be a lot of empty space between the image and
        # some rectangle's edges. This would cause problems when detecting collisions of the image and other
        # objects.
        # The collision would be detected, even though the image and an object didn't directly visibly touched.
        self.rectangle = pygame.Rect(0, 0, self.rectangle_width, self.rectangle_height)
        self.rectangle.center = starting_position

    def draw(self, surface):
        surface.blit(self.image, (self.rectangle.x - 8, self.rectangle.y - 5))
        pygame.draw.rect(surface, WHITE, self.rectangle, 2)
