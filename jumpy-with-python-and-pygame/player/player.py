import pygame

from constants import WHITE, WINDOW_WIDTH
from .constants import JUMPY_IMAGE_SCALE, JUMPY_MOVEMENT_DISTANCE


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
        self.flip_image = False

    def move(self):
        # Reset variables
        delta_x = 0
        delta_y = 0

        # Process key presses
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            delta_x = -JUMPY_MOVEMENT_DISTANCE
            self.flip_image = True
        if key[pygame.K_RIGHT]:
            delta_x = JUMPY_MOVEMENT_DISTANCE
            self.flip_image = False

        # Make sure that before we update the player's position he doesn't go off the edge of the window
        if self.rectangle.left + delta_x < 0:
            delta_x = -self.rectangle.left
        if self.rectangle.right + delta_x > WINDOW_WIDTH:
            delta_x = WINDOW_WIDTH - self.rectangle.right

        # Update rectangle position
        self.rectangle.x += delta_x
        self.rectangle.y += delta_y


    def draw(self, surface):
        surface.blit(pygame.transform.flip(self.image, self.flip_image, False), (self.rectangle.x - 8, self.rectangle.y - 5))
        pygame.draw.rect(surface, WHITE, self.rectangle, 2)
