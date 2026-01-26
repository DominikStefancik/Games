from settings import pygame, vector, TILE_SIZE

from .constants import Collision, PLAYER_GRAVITY, PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, position, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill("red")
        # Represents a rectangle to figure out where the player will be drawn in a current frame
        self.rect = self.image.get_frect(topleft = position)
        # Represents a rectangle to figure out where the player was drawn in a previous frame
        self.previous_rect = self.rect.copy()

        self.direction = vector()
        self.speed = PLAYER_SPEED

        self.collision_sprites = collision_sprites

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
        self.direction.x = input_vector.normalize().x if input_vector else input_vector.x

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.detect_collision(Collision.HORIZONTAL)

        # Process vertical change
        # The longer the player keeps falling, the bigger the gravity is and the faster he falls
        self.direction.y += PLAYER_GRAVITY / 2 * delta_time
        self.rect.y += self.direction.y * delta_time
        self.direction.y += PLAYER_GRAVITY / 2 * delta_time
        self.detect_collision(Collision.VERTICAL)


    def detect_collision(self, collision_axis):
        # For processing collisions we want to separate horizontal and vertical axes
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if collision_axis == Collision.HORIZONTAL:
                    # Collision happened from the left side of the player to the right side of the sprite
                    # where the player was on the right side of the sprite before the collision
                    if self.rect.left <= sprite.rect.right and self.previous_rect.left >= sprite.previous_rect.right:
                        self.rect.left = sprite.rect.right

                    # Collision happened from the right side of the player to the left side of the sprite
                    # where the player was on the left side of the sprite before the collision
                    if self.rect.right >= sprite.rect.left and self.previous_rect.right <= sprite.previous_rect.left:
                        self.rect.right = sprite.rect.left

                if collision_axis == Collision.VERTICAL:
                    # Collision happened from the top side of the player to the bottom side of the sprite
                    # where the player was on the bottom side of the sprite before the collision
                    if self.rect.top <= sprite.rect.bottom and self.previous_rect.top >= sprite.previous_rect.bottom:
                        self.rect.top = sprite.rect.bottom

                    # Collision happened from the bottom side of the player to the top side of the sprite
                    # where the player was on the top side of the sprite before the collision
                    if self.rect.bottom >= sprite.rect.top and self.previous_rect.bottom <= sprite.previous_rect.top:
                        self.rect.bottom = sprite.rect.top

                    # If a vertical collision happened, we want to reset the vertical direction
                    # otherwise, the gravity would keep applying even though the player is not falling
                    self.direction.y = 0

    def update(self, delta_time):
        # Before updating the movement, store the position of the current rectangle
        # This will be then used for a collision detection
        self.previous_rect = self.rect.copy()
        self.process_key_input()
        self.move(delta_time)
