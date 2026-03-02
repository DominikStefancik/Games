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
        # We need to make sure that the car is not trying to move towards a point which doesn't exist
        if self.current_path_point_index >= len(self.path):
            return

        # First we need to figure out the car's angle depending on which part of the path the car is
        # because we want it to shift towards the right direction following a particular target point of the path.
        self.calculate_angle()
        self.update_path_point_index()
        super().move()

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_path_point_index]
        difference_x = target_x - self.x
        difference_y = target_y - self.y

        # If "difference_y == 0" the car is in a vertical position
        if difference_y == 0:
            # The "desired_radian_angle" represents an angle between car's current position and the target point
            # (the same in the "else" branch)
            desired_radian_angle = math.pi / 2
        else:
            # The method "atan()" calculates an inverse tangent function
            desired_radian_angle = math.atan(difference_x / difference_y)

        # The "desired_radian_angle" will always be an accute angle, which means it will be less than 90 degrees.
        # But if the current target point is positioned lower than the car's current position
        # the turn which the car would have to take is more extreme than the angle we have calculated.
        if target_y > self.y:
            desired_radian_angle += math.pi

        # Based on whether the desired angle is positive or negative, the car will turn left or right.
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)

        # If the difference is larger than 180 degrees, the car will be taking an inefficient direction
        # to get to the angle.
        # To fix this, we need to subtract 360 from the difference. Then the car will take
        # the opposite (efficient) direction to the target point.
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        # If the car goes left, it increaces its angle.
        # So if the car's current angle is bigger than the desired angle, we want the car to turn the opposite way.
        if difference_in_angle > 0:
            # If the difference in angle is less than the car's rotation velocity, we move by that difference,
            # so we snap precisely on the angle. Otherwise the car would repeatedly go above and below the angle.
            self.angle -= min(self.rotation_velocity, abs(difference_in_angle))
        else:
            self.angle += min(self.rotation_velocity, abs(difference_in_angle))

    # Checks if the car collided with a target point of the path.
    # If it did, we need to update the next point as a new target.
    def update_path_point_index(self):
        target = self.path[self.current_path_point_index]
        car_rectangle = pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height()
        )

        # The method "collidepoint" expects X and Y coordinates,
        # that's why we have to use "*" when passing the parameter which is a tuple value.
        if car_rectangle.collidepoint(*target):
            # If the car collided with the target point update index to the next one
            self.current_path_point_index += 1

    def update_parameters(self, level):
        self.reset_position()
        # We need to make sure that the computer car's velocity will not be higher than the player's car velocity.
        # Otherwise the player will not be able to beat the computer, because its car will be simply faster
        self.velocity = self.maximum_velocity + (level - 1) * 0.2
        self.current_path_point_index = 0
