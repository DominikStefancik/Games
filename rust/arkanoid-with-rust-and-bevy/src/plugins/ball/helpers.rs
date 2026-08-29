use bevy::transform::components::Transform;

use crate::plugins::{BALL_RADIUS, Ball, HALF_PADDLE, MovingArea};

pub fn check_borders_when_moving_with_paddle(
    moving_area: &MovingArea,
    transform: &mut Transform,
    ball: &mut Ball,
) {
    let MovingArea {
        left_border,
        right_border,
        ..
    } = moving_area;

    if transform.translation.x - HALF_PADDLE <= *left_border {
        ball.direction.x = 0.;
        transform.translation.x = left_border + HALF_PADDLE;
    }

    if transform.translation.x + HALF_PADDLE >= *right_border {
        ball.direction.x = 0.;
        transform.translation.x = right_border - HALF_PADDLE;
    }
}

pub fn check_borders_when_moving(
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

    if transform.translation.y - BALL_RADIUS <= *lower_border {
        ball.direction.y = 1.;
    }
}
