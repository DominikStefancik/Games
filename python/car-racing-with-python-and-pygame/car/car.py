import math
import pygame

from .helpers import rotate_car_image_center


class AbstractCar:
    def __init__(self, image, starting_position, maximum_velocity, rotation_velocity):
        self.image = image
        self.starting_position = starting_position
        self.x, self.y = self.starting_position
        self.maximum_velocity = maximum_velocity
        # How quickly can a car rotate
        self.rotation_velocity = rotation_velocity
        self.velocity = 0
        self.angle = 0
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity

    def draw(self, surface):
        rotate_car_image_center(surface, self.image, (self.x, self.y), self.angle)

    def move_forward(self):
        # Increase the car's velocity until its value reaches the maximum
        self.velocity = min(self.velocity + self.acceleration, self.maximum_velocity)
        self.move()

    def move_backward(self):
        # When going backward, the car's maximum velocity cannot be the same as when the car moves forward
        # In reality, a car cannot go the same maximum speed when moving in reverse
        self.velocity = max(
            self.velocity - self.acceleration, -self.maximum_velocity / 2
        )
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical_velocity = math.cos(radians) * self.velocity
        horizontal_velocity = math.sin(radians) * self.velocity

        self.x -= horizontal_velocity
        self.y -= vertical_velocity

    # Pixel perfect collision
    #
    # Mask is an array of values representing whether or not the pixel of an image is transparent or present
    # (i.e. whether the pixel exists).
    # The point of a mask is that rather detecting colision of two objects by using their rectangles
    # (which represent their hit boxes), we can simply check if the pixels of the image, that are not transparent,
    # are overlapping in two rectangular regions.
    #
    # Calling mask
    # Mask that is being called on = the mask we want to find an offset on
    def collide(self, other_mask, other_mask_x=0, other_mask_y=0):
        car_mask = pygame.mask.from_surface(self.image)
        # Mask offset has to be an integer value, because we might get a floating value when doing the subtraction
        # The offset is relative to the calling mask
        offset = (int(self.x - other_mask_x), int(self.y - other_mask_y))
        #  The "other_mask" is the calling mask and it will dictate how we calculate the collision overlap
        point_of_intersection = other_mask.overlap(car_mask, offset)

        # The point of intersection is None, the two objects didn't collide
        return point_of_intersection

    def reset_position(self):
        self.x, self.y = self.starting_position
        self.angle = 0
        self.velocity = 0
