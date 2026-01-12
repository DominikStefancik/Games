import math

import pygame
from pygame.math import Vector2
from .constants import ENEMY_DATA


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, images, waypoints) -> None:
        # We have to call the superclass' init method
        pygame.sprite.Sprite.__init__(self)
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.angle = 0
        self.waypoints = waypoints
        self.current_position = Vector2(self.waypoints[0])
        self.original_image = images.get(enemy_type)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.current_position
        self.target_waypoint_index = 1

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Define a target waypoint
        if self.target_waypoint_index < len(self.waypoints):
            self.target_position = Vector2(self.waypoints[self.target_waypoint_index])
            self.movement = self.target_position - self.current_position
        else:
            # The enemy has reached the end of the path
            # The method "kill" is inheriied from the Sprite superclass. It will automatically remove the sprite
            # from the sprite group
            self.kill()

        # Every step the enemy moves we need to calculate how much distance is left to target
        # so later we can adjust the movement so it doesn't get overshot
        distance = self.movement.length()

        # Check if remaining distance is greater than the enemy speed
        if distance >= self.speed:
            # The method "normalize()" on the Vector calculates trigonometrically
            # how the enemy should move from his current position to his target position
            self.current_position += self.movement.normalize() * self.speed
        else:
            # Once an enemy gets closer to the waypoint, and it is closer then speed,
            # it means it will move closer just a tiny bit.
            # The result will will that the enemy will land exactly on the waypoint
            if distance != 0:
                self.current_position += self.movement.normalize() * distance

            # When enemy reaches his target, the "self.movement" (which is the distance between a current position
            # and the target) is 0. However, the zero cannot be normalised, so we have to change the target.
            # A new target will be next waypoint
            self.target_waypoint_index += 1

    # Rotates the enemy depending on which part of the way he is
    #
    # Note: if we keep rotating the image over and over, we slowly lose the quality of the image.
    # That's why we have declared the property "original_image" which we will use for the rotation
    def rotate(self):
        # Calculate distance to the next waypoint
        distance = self.target_position - self.current_position
        # Use distance to calculate angle
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))

        # Rotate image and update rectangle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.current_position
