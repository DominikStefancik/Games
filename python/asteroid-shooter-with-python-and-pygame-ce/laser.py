import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, image, position):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_frect(midbottom=position)
        self.speed = 400

    def update(self, delta_time):
        self.rect.y -= self.speed * delta_time

        if self.rect.bottom < 0:
            self.kill()
