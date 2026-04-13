import math

import pygame
import pymunk

from settings import WINDOW_HEIGHT
from sprites_manager.constants import (
    BALL_DIAMETER,
    BALL_ELASTICITY,
    BALL_MASS,
    BALL_MAX_FORCE,
    BALL_RADIUS,
    CUSHION_ELASTICITY,
)


def create_balls(space) -> list[pymunk.Shape]:
    balls = []
    rows = 5

    for column in range(5):
        for row in range(rows):
            position = (
                250 + column * BALL_DIAMETER,
                267 + (row * (BALL_DIAMETER + 2)) + (column * BALL_RADIUS),
            )
            new_ball = create_ball(space, position)
            balls.append(new_ball)

        rows -= 1

    return balls


def create_ball(space, position) -> pymunk.Shape:
    # An object in PyMunk space has a body and shape
    #
    # By default a body is dynamic
    body = pymunk.Body()
    body.position = position
    shape = pymunk.Circle(body, BALL_RADIUS)
    shape.mass = BALL_MASS
    shape.elasticity = BALL_ELASTICITY

    # We need to physically attach balls to our space, so when they move, there is some kind of friction
    # which will slow their movement down after some time.
    #
    # We will use pivot joint to add friction
    pivot = pymunk.PivotJoint(
        space.static_body, body, (0, 0), (0, 0)
    )  # coordinates where joint is applied
    # disable joint correction
    pivot.max_bias = 0
    # emulate linear friction -> the higher the value the bigger the friction
    pivot.max_force = BALL_MAX_FORCE

    space.add(body, shape, pivot)

    return shape


# Create PyMunk objects representing the table cushions so balls can collide with them
# and change direction after a collision
def create_table_cushion(space, polygon_dimensions) -> None:
    # We don't want cusshions to move around. Just be static so balls can bounce of them
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (0, 0)
    # Poly = polygon
    shape = pymunk.Poly(body, polygon_dimensions)
    shape.elasticity = CUSHION_ELASTICITY

    space.add(body, shape)


# Calculates pool cue angle
def get_cue_angle(cue_ball) -> float:
    mouse_position = pygame.mouse.get_pos()
    distance_x = cue_ball.body.position[0] - mouse_position[0]
    # The value of Y-coordinate increaces as we go down, so we have to used the negative value
    distance_y = -(cue_ball.body.position[1] - mouse_position[1])
    cue_angle = math.degrees(math.atan2(distance_y, distance_x))

    return cue_angle
