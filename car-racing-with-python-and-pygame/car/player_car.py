from .car import AbstractCar

class PlayerCar(AbstractCar):
    # The car's speed is reduced by the half of the acceleration
    def reduce_speed(self):
        # If reducing the speed produces a negative value, we don't want to use that one
        # because the car would go backwards while slowing down.
        # Instead, we want it to stop, that's why we limit it with 0
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.move()
