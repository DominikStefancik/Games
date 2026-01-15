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

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_velocity
        elif right:
            self.angle -= self.rotation_velocity

    def draw(self, surface):
        rotate_car_image_center(surface, self.image, (self.x, self.y), self.angle)
