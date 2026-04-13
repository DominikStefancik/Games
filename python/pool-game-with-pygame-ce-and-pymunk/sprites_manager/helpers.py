import math

import pygame
import pymunk

from asset_manager.asset_manager import get_asset_manager
from asset_manager.constants import ImageAsset
from settings import RED_COLOR
from sprites_manager.ball import Ball
from sprites_manager.constants import (
    BALL_DIAMETER,
    BALL_ELASTICITY,
    BALL_MASS,
    BALL_MAX_FORCE,
    BALL_RADIUS,
    BLACK_POCKET_RADIUS,
    CUSHION_ELASTICITY,
    POCKETS_COORDINATES,
)


def create_balls(space) -> list[Ball]:
    asset_manager = get_asset_manager()
    shapes = []
    balls = []
    rows = 5

    # First create Pymunk shapes
    for column in range(5):
        for row in range(rows):
            position = (
                250 + column * BALL_DIAMETER,
                267 + (row * (BALL_DIAMETER + 2)) + (column * BALL_RADIUS),
            )
            new_ball = create_ball(space, position)
            shapes.append(new_ball)

        rows -= 1

    # Then create balls with images
    for index, shape in enumerate(shapes, start=1):
        image = asset_manager.graphics[ImageAsset.get_ball(index)]
        ball = Ball(shape, image)
        balls.append(ball)

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
    distance_x = cue_ball.shape.body.position[0] - mouse_position[0]
    # The value of Y-coordinate increaces as we go down, so we have to used the negative value
    distance_y = -(cue_ball.shape.body.position[1] - mouse_position[1])
    cue_angle = math.degrees(math.atan2(distance_y, distance_x))

    return cue_angle


def get_cue_impulse(cue_angle):
    impulse_x = math.cos(math.radians(cue_angle))
    impulse_y = math.sin(math.radians(cue_angle))

    return (impulse_x, impulse_y)


def create_power_bar():
    power_bar = pygame.Surface((10, 20))
    power_bar.fill(RED_COLOR)

    return power_bar


def are_balls_moving(balls, cue_ball):
    # velocity[0] is ball speed in horizontal direction
    # velocity[1] is ball speed in vertical direction
    #
    # Sometimes the velocity stops not exactly on 0, but 0.0000000001, that's why we need to convert it to an integer
    if (
        int(cue_ball.shape.body.velocity[0]) != 0
        or int(cue_ball.shape.body.velocity[1]) != 0
    ):
        return True

    for ball in balls:
        if (
            int(ball.shape.body.velocity[0]) != 0
            or int(ball.shape.body.velocity[1]) != 0
        ):
            return True

    return False


def check_potted_balls(space, balls, potted_balls):
    for ball in balls:
        for pocket in POCKETS_COORDINATES:
            ball_distance_x = abs(ball.shape.body.position[0] - pocket[0])
            ball_distance_y = abs(ball.shape.body.position[1] - pocket[1])
            # the distance between the center of th ball and the center of the pocket
            ball_distance = math.sqrt((ball_distance_x**2) + (ball_distance_y**2))

            if ball_distance <= BLACK_POCKET_RADIUS:
                # remove the ball from the Pymunk space
                space.remove(ball.shape.body)
                balls.remove(ball)
                potted_balls.append(ball)


def is_cue_ball_potted(cue_ball) -> bool:
    is_potted = False

    for pocket in POCKETS_COORDINATES:
        ball_distance_x = abs(cue_ball.shape.body.position[0] - pocket[0])
        ball_distance_y = abs(cue_ball.shape.body.position[1] - pocket[1])
        # the distance between the center of th ball and the center of the pocket
        ball_distance = math.sqrt((ball_distance_x**2) + (ball_distance_y**2))

        if ball_distance <= BLACK_POCKET_RADIUS:
            is_potted = True
            break

    return is_potted
