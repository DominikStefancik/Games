import pygame
import pymunk
import pymunk.pygame_util

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from input_manager import get_input_manager
from settings import FPS
from sprites_manager.constants import CUE_BALL_IMPULSE_X, CUSHIONS_DIMENSIONS
from sprites_manager.helpers import create_ball, create_table_cushion


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

        self.ball = create_ball(self.space, 25, (300, 200))
        self.cue_ball = create_ball(self.space, 25, (600, 215))

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
            self.cue_ball.body.apply_impulse_at_local_point(
                (CUE_BALL_IMPULSE_X, 0), (0, 0)
            )

    def draw(self):
        self.display_surface.blit(self.asset_manager.graphics[ImageAsset.TABLE], (0, 0))
        self.space.debug_draw(self.draw_options)
