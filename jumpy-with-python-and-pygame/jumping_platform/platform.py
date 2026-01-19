import pygame


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
