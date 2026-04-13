import math
import pygame
import pymunk
import pymunk.pygame_util

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from game_state.game_state import GameState
from game_state.game_state_manager import get_game_state_manager
from settings import BACKGROUND_COLOR, BOTTOM_PANEL, FPS, WINDOW_HEIGHT, WINDOW_WIDTH
from sprites_manager.ball import Ball
from sprites_manager.constants import CUE_BALL_STARTING_POSITION, CUSHIONS_DIMENSIONS
from sprites_manager.cue import Cue
from sprites_manager.helpers import (
    are_balls_moving,
    check_potted_balls,
    create_ball,
    create_balls,
    create_power_bar,
    create_table_cushion,
    get_cue_angle,
    get_cue_impulse,
    is_cue_ball_potted,
)


class SpritesManager:
    def __init__(self):
        # The main surface on which we will be drawing elements
        self.display_surface = pygame.display.get_surface()
        self.asset_manager = get_asset_manager()
        self.game_state_manager = get_game_state_manager()

        # Space is an environment where PyMunk adds objects and applies physics on them
        self.space = pymunk.Space()
        self.static_body = self.space.static_body
        self.draw_options = pymunk.pygame_util.DrawOptions(self.display_surface)

        for dimension in CUSHIONS_DIMENSIONS:
            create_table_cushion(self.space, dimension)

        self.balls = create_balls(self.space)
        self.cue_ball = Ball(
            create_ball(self.space, CUE_BALL_STARTING_POSITION),
            self.asset_manager.graphics[ImageAsset.CUE_BALL],
        )
        self.cue = Cue(
            self.asset_manager.graphics[ImageAsset.CUE],
            self.cue_ball.shape.body.position,
        )
        self.potted_balls = []

    def restart(self):
        pass

    def update(self):
        self.space.step(1 / FPS)

        cue_angle = get_cue_angle(self.cue_ball)
        self.cue.update(self.cue_ball.shape.body.position, cue_angle)

        if self.game_state_manager.game_state == GameState.POWERING_UP:
            self.cue.power_up()
        elif self.game_state_manager.game_state == GameState.TAKING_SHOT:
            cue_impulse = get_cue_impulse(cue_angle)

            # We can apply Force or Impulse to a ball
            #
            # The fist argument is impulse in the X and Y directions
            # The second argument are X and Y coordinates relative to the center of the body
            # (the value (0, 0) refers to the middle of the body)
            self.cue_ball.shape.body.apply_impulse_at_local_point(
                (self.cue.force * -cue_impulse[0], self.cue.force * cue_impulse[1]),
                (0, 0),
            )
            self.cue.reset_force()

        check_potted_balls(self.space, self.balls, self.potted_balls)

        if is_cue_ball_potted(self.cue_ball):
            self.cue_ball.shape.body.velocity = (0.0, 0.0)
            # First hide the ball
            self.cue_ball.shape.body.position = (-100, -100)

            # Then wait after all ball stop moving
            # And only after they all stop, place the cue ball onto the starting position
            if not are_balls_moving(self.balls, self.cue_ball):
                self.cue_ball.shape.body.position = CUE_BALL_STARTING_POSITION

    def draw_balls(self):
        for ball in self.balls:
            ball.draw(self.display_surface)

        self.cue_ball.draw(self.display_surface)

    def draw_potted_balls(self):
        for index, ball in enumerate(self.potted_balls):
            self.display_surface.blit(ball.image, (10 + index * 50, WINDOW_HEIGHT + 10))

    def draw(self):
        self.display_surface.blit(self.asset_manager.graphics[ImageAsset.TABLE], (0, 0))
        self.space.debug_draw(self.draw_options)

        self.draw_balls()

        if self.game_state_manager.game_state != GameState.WAITING_TO_START:
            if are_balls_moving(self.balls, self.cue_ball):
                self.game_state_manager.game_state = GameState.BALLS_MOVING
            elif self.game_state_manager.game_state != GameState.POWERING_UP:
                self.game_state_manager.game_state = GameState.PREPARING_SHOT

            if self.game_state_manager.game_state in [
                GameState.PREPARING_SHOT,
                GameState.POWERING_UP,
            ]:
                self.cue.draw(self.display_surface)

            if self.game_state_manager.game_state == GameState.POWERING_UP:
                # Create power bars to visually show how hard the cue ball will be hit
                power_bar = create_power_bar()
                for bar in range(math.ceil(self.cue.force / 1250)):
                    self.display_surface.blit(
                        power_bar,
                        (
                            self.cue_ball.shape.body.position[0] - 30 + (bar * 15),
                            self.cue_ball.shape.body.position[1] + 30,
                        ),
                    )

            # Draw bottom panel
            pygame.draw.rect(
                self.display_surface,
                BACKGROUND_COLOR,
                (0, WINDOW_HEIGHT, WINDOW_WIDTH, BOTTOM_PANEL),
            )

            self.draw_potted_balls()
