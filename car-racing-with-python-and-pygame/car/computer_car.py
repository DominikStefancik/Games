import math
import pygame

from .car import AbstractCar


class ComputerCar(AbstractCar):
    def __init__(
        self, image, starting_position, maximum_velocity, rotation_velocity, path=[]
    ):
        super().__init__(image, starting_position, maximum_velocity, rotation_velocity)
        # The path is a list of coordinates we want the car to move to
        self.path = path
        self.current_path_point_index = 0
        # The computer car doesn't have acceleration and it always moves at maximum velocity
        self.velocity = maximum_velocity

    def draw_points(self, surface):
        for point in self.path:
            pygame.draw.circle(surface, (255, 0, 0), point, 5)

    def draw(self, surface):
        super().draw(surface)
        # Uncomment drawing points when testing the game
        # self.draw_points(surface)

    def move(self):
        if self.current_path_point_index >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point_index()
        super().move()

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_path_point_index]
        difference_x = target_x - self.x
        difference_y = target_y - self.y

        # If "difference_y == 0" the car is in a vertical position
        if difference_y == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(difference_x / difference_y)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_velocity, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_velocity, abs(difference_in_angle))

    def update_path_point_index(self):
        target = self.path[self.current_path_point_index]
        rectangle = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height()
        )

        if rectangle.collidepoint(*target):
            # If the car collided with the target point update index to the next one
            self.current_path_point_index += 1

    def update_parameters(self, level):
        self.reset_position()
        # We need to make sure that the computer car's velocity will not be higher than the player's car velocity.
        # Otherwise the player will not be able to beat the computer, because its car will be simply faster
        self.velocity = self.maximum_velocity + (level - 1) * 0.2
        self.current_path_point_index = 0
