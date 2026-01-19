import pygame

from constants import WINDOW_HEIGHT

class Platform(pygame.sprite.Sprite):
    def __init__(self, image, position, width):
        pygame.sprite.Sprite.__init__(self)
        # For each platform, the width will be different so we can have randomness in platforms sizes
        self.image = pygame.transform.scale(image, (width, 10))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self, scroll):
        # Update platform's vertical position depending on if we scroll the window or not
        self.rect.y += scroll

        # If the platform has gone off the window screen, destroy the object and remove it from the memory.
        # By doing that, it will also be removed from the "platform_group".
        # This way we achieve there will be infinite number of platform generated, because those which
        # will go off the screen will be destroyed.
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
