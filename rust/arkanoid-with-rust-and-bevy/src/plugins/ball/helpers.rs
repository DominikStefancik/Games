use bevy::{
    ecs::system::Commands,
    math::{
        Vec3,
        bounding::{Aabb2d, BoundingCircle, IntersectsVolume},
    },
    transform::components::Transform,
};

use crate::plugins::{BALL_RADIUS, Ball, BallFallenDown, CollisionSide, MovingArea, Paddle};

pub fn check_borders_when_moving_with_paddle(
    moving_area: &MovingArea,
    transform: &mut Transform,
    ball: &mut Ball,
    paddle: &Paddle,
) {
    let MovingArea {
        left_border,
        right_border,
        ..
    } = moving_area;
    let paddle_half_size = paddle.size / 2.;

    if transform.translation.x - paddle_half_size.x <= *left_border {
        ball.direction.x = 0.;
        transform.translation.x = left_border + paddle_half_size.x;
    }

    if transform.translation.x + paddle_half_size.x >= *right_border {
        ball.direction.x = 0.;
        transform.translation.x = right_border - paddle_half_size.x;
    }
}

pub fn check_borders_when_moving(
    commands: &mut Commands,
    moving_area: &MovingArea,
    transform: &mut Transform,
    ball: &mut Ball,
) {
    let MovingArea {
        left_border,
        right_border,
        upper_border,
        lower_border,
    } = moving_area;

    if transform.translation.x - BALL_RADIUS <= *left_border {
        ball.direction.x = 1.;
    }

    if transform.translation.x + BALL_RADIUS >= *right_border {
        ball.direction.x = -1.;
    }

    if transform.translation.y + BALL_RADIUS >= *upper_border {
        ball.direction.y = -1.;
    }

    if transform.translation.y <= *lower_border {
        commands.trigger(BallFallenDown);
    }
}

/*
 * Returns `Some` if `ball` collides with `bounding_box`.
 * The returned `CollisionSide` is the side of `bounding_box` that `ball` hit.
 */
pub fn detect_ball_collision(
    bounding_cirle: BoundingCircle,
    bounding_rectangle: Aabb2d,
) -> Option<CollisionSide> {
    if !bounding_cirle.intersects(&bounding_rectangle) {
        return None;
    }

    let closest_point = bounding_rectangle.closest_point(bounding_cirle.center);
    let offset = bounding_cirle.center - closest_point;
    let side = if offset.x.abs() > offset.y.abs() {
        if offset.x < 0. {
            CollisionSide::Left
        } else {
            CollisionSide::Right
        }
    } else if offset.y > 0. {
        CollisionSide::Top
    } else {
        CollisionSide::Bottom
    };

    Some(side)
}

pub fn get_ball_initial_position(moving_area: &MovingArea) -> Vec3 {
    let ball_y = moving_area.lower_border + BALL_RADIUS;

    Vec3::new(0., ball_y, 1.)
}
