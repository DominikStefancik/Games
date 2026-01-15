from .car import AbstractCar

class PlayerCar(AbstractCar):
    # The car's speed is reduced by the half of the acceleration
    def reduce_speed(self):
        # If reducing the speed produces a negative value, we don't want to use that one
        # because the car would go backwards while slowing down.
        # Instead, we want it to stop, that's why we limit it with 0
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.move()

    # The method called when the car hits (i.e. collides with) the track border.
    # When that happens, we want the car to bounce of the track border.
    def bounce(self):
        # The car will bounce off with the same velocity which it had when it hit the border
        self.velocity = -self.velocity
        self.move()
