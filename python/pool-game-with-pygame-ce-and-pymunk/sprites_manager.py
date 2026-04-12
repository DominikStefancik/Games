import pygame
import pymunk
import pymunk.pygame_util

from input_manager import get_input_manager
from settings import FPS


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()
        self.input_manager = get_input_manager()

        # Space is an environment where PyMunk adds objects and applies physics on them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        self.ball = self.create_ball(25, (300, 200))
        self.cue_ball = self.create_ball(25, (600, 215))

    def create_ball(self, radius, position):
        # An object in PyMunk space has a body and shape
        body = pymunk.Body()
        body.position = position
        shape = pymunk.Circle(body, radius)
        shape.mass = 5

        # We need to physically attach balls to our space, so when they move, there is some kind of friction
        # which will slow their movement down after some time.
        #
        # We will use pivot joint to add friction
        pivot = pymunk.PivotJoint(
            self.static_body, body, (0, 0), (0, 0)
        )  # coordinates where joint is applied
        # disable joint correction
        pivot.max_bias = 0
        # emulate linear friction -> the higher the value the bigger the friction
        pivot.max_force = 1000

        self.space.add(body, shape, pivot)

        return shape

    def restart(self):
        pass

    def update(self):
        self.space.step(1 / FPS)

        if self.input_manager.left_mouse_clicked:
            # We can apply Force or Impulse to a ball
            #
            # The fist argument is impulse in the X and Y directions
            # The second argument are X and Y coordinates relative to the center of the body
            # (the value (0, 0) refers to the middle of the body)
            self.cue_ball.body.apply_impulse_at_local_point((-500, 0), (0, 0))

    def draw(self):
        self.space.debug_draw(self.draw_options)
