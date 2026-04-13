import pygame
import pymunk
import pymunk.pygame_util

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from input_manager import get_input_manager
from settings import FPS, WINDOW_HEIGHT
from sprites_manager.constants import CUE_BALL_IMPULSE_X, CUSHIONS_DIMENSIONS
from sprites_manager.cue import Cue
from sprites_manager.helpers import (
    create_ball,
    create_balls,
    create_table_cushion,
    get_cue_angle,
)


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()
        self.asset_manager = get_asset_manager()
        self.input_manager = get_input_manager()

        # Space is an environment where PyMunk adds objects and applies physics on them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        for dimension in CUSHIONS_DIMENSIONS:
            create_table_cushion(self.space, dimension)

        self.balls = create_balls(self.space)
        self.cue_ball = create_ball(self.space, (888, WINDOW_HEIGHT / 2))
        self.cue = Cue(
            self.asset_manager.graphics[ImageAsset.CUE], self.cue_ball.body.position
        )

    def restart(self):
        pass

    def update(self):
        self.space.step(1 / FPS)

        self.cue.update(self.cue_ball.body.position, get_cue_angle(self.cue_ball))

        if self.input_manager.left_mouse_clicked:
            # We can apply Force or Impulse to a ball
            #
            # The fist argument is impulse in the X and Y directions
            # The second argument are X and Y coordinates relative to the center of the body
            # (the value (0, 0) refers to the middle of the body)
            self.cue_ball.body.apply_impulse_at_local_point(
                (CUE_BALL_IMPULSE_X, 0), (0, 0)
            )

    def draw(self):
        self.display_surface.blit(self.asset_manager.graphics[ImageAsset.TABLE], (0, 0))
        self.space.debug_draw(self.draw_options)

        for index, ball in enumerate(self.balls):
            self.display_surface.blit(
                self.asset_manager.graphics[ImageAsset.get_ball(index + 1)],
                (
                    ball.body.position[0] - ball.radius,
                    ball.body.position[1] - ball.radius,
                ),
            )

        self.display_surface.blit(
            self.asset_manager.graphics[ImageAsset.CUE_BALL],
            (
                self.cue_ball.body.position[0] - self.cue_ball.radius,
                self.cue_ball.body.position[1] - self.cue_ball.radius,
            ),
        )

        self.cue.draw(self.display_surface)
