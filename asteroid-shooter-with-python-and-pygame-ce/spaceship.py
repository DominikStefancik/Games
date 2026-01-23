import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, groups, image):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(groups)
        self.image = image
        # The method "get_frect()" gets "FRect" out of the image.
        # The "FRect" is very similar to the rectangle "Rect". The onl difference is that its sizes are measured
        # in the floating points.
        # The method parameter sasys that the center of the rectangle will be in the middle of the screen
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        # If we don't provide any arguments, the initial Vector2 values will be 0, 0
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, delta_time):
        # The method "get_pressed()" constantly (every frame) checks for pressed buttons
        # Whereas the method "get_just_pressed()" checks only for most recent button presses
        keys = pygame.key.get_pressed()

        # The expression "keys[pygame.K_RIGHT]" returns a boolean value
        # The expression "int(boolean)" returns 1 (for True) or 0 (for False)
        # Then the direction will be either
        #   0 (if we didn't press right or left key)
        #   1 (if we pressed the right key)
        #   -1 (if we pressed the left key)
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        # We cannot normalise the direction vector, if both of its values is 0
        # The one-liner IF says:
        #   "if vector is (0,1), (1,0) or (1,1), then call the method normalize, otherwise keep it as it is"
        self.direction = self.direction.normalize() if self.direction else self.direction

        # With adding the delta time as a multiplier,
        # we are independent of how many frame rates are defined in the clock's tick method
        self.rect.center += self.direction * self.speed * delta_time

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
