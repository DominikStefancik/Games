import math

from .helpers import rotate_car_image_center

class AbstractCar:
    def __init__(self, image, starting_position, maximum_velocity, rotation_velocity):
        self.image = image
        self.maximum_velocity = maximum_velocity
        # How quickly can a car rotate
        self.rotation_velocity = rotation_velocity
        self.velocity = 0
        self.angle = 0
        self.x, self.y = starting_position
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

    def move(self):
        radians = math.radians(self.angle)
        vertical_velocity = math.cos(radians) * self.velocity
        horizontal_velocity = math.sin(radians) * self.velocity

        self.x -= horizontal_velocity
        self.y -= vertical_velocity

    # The car's speed is reduced by the half of the acceleration
    def reduce_speed(self):
        # If reducing the speed produces a negative value, we don't want to use that one
        # because the car would go backwards while slowing down.
        # Instead, we want it to stop, that's why we limit it with 0
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.move()
