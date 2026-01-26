from settings import pygame, vector, TILE_SIZE

from .constants import PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")
        self.rect = self.image.get_frect(topleft = position)

        self.direction = vector()
        self.speed = PLAYER_SPEED

    def process_key_input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if keys[pygame.K_LEFT]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        if keys[pygame.K_UP]:
            input_vector.y -= 1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1

        # Normalise the vector only if one of its values is not zero
        self.direction = input_vector.normalize() if input_vector else input_vector

    def move(self, delta_time):
        self.rect.topleft += self.direction * self.speed * delta_time

    def update(self, delta_time):
        self.process_key_input()
        self.move(delta_time)
