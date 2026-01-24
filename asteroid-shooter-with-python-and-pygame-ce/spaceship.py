import pygame

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, all_groups, lasers_group, image, laser_image):
        # Initialise the parent class
        # When passing sprite groups to the parent class Pygame automatically adds this custom Sprite class to them
        super().__init__(all_groups)
        self.all_groups = all_groups
        self.lasers_group = lasers_group
        self.laser_image = laser_image
        self.image = image
        # The method "get_frect()" gets "FRect" out of the image.
        # The "FRect" is very similar to the rectangle "Rect". The onl difference is that its sizes are measured
        # in the floating points.
        # The method parameter sasys that the center of the rectangle will be in the middle of the screen
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        # If we don't provide any arguments, the initial Vector2 values will be 0, 0
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # Create a custom timer to track time after a certain event happened, i.e a certain key was pressed.
        # We get a starting point and then measure the time passed since that starting point.
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

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

        if keys[pygame.K_SPACE] and self.can_shoot:
            Laser((self.all_groups, self.lasers_group), self.laser_image, self.rect.midtop)
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.update_laser_timer()

    def update_laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()

            # Allow shooting a laser only if the cooldown time passed after the last shot
            if current_time - self.laser_shoot_time > self.cooldown_duration:
                self.can_shoot = True
