use bevy::{
    color::Color,
    ecs::system::{Commands, Single},
    math::Vec2,
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BOTTOM_OFFSET, HALF_PADDLE, PADDLE_MOVEMENT_SPEED, PADDLE_SIZE, WINDOW_RESOLUTION,
    paddle::Paddle,
};

pub fn spawn_paddle(mut commands: Commands) {
    commands.spawn((
        Sprite::from_color(Color::WHITE, Vec2::new(PADDLE_SIZE.0, PADDLE_SIZE.1)),
        Transform::from_xyz(0., -((WINDOW_RESOLUTION.1 / 2 - BOTTOM_OFFSET) as f32), 1.),
        Paddle {
            direction: 0.,
            speed: PADDLE_MOVEMENT_SPEED,
        },
    ));
}

pub fn move_paddle(paddle_query: Single<(&mut Transform, &Paddle)>) {
    let (mut transform, paddle) = paddle_query.into_inner();

    transform.translation.x += paddle.direction * paddle.speed;

    let left_border = -((WINDOW_RESOLUTION.0 / 2) as f32);
    let right_border = (WINDOW_RESOLUTION.0 / 2) as f32;

    if transform.translation.x - HALF_PADDLE <= left_border {
        transform.translation.x = left_border + HALF_PADDLE;
    }

    if transform.translation.x + HALF_PADDLE >= right_border {
        transform.translation.x = right_border - HALF_PADDLE
    }
}
