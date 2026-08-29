use bevy::{
    ecs::system::{Commands, Res, Single},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BALL_RADIUS, Ball, GameTexture, MovingArea, check_borders_when_moving,
    check_borders_when_moving_with_paddle,
};

pub fn spawn_ball(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    moving_area: Res<MovingArea>,
) {
    let ball_y = moving_area.lower_border + BALL_RADIUS;

    commands.spawn((
        Sprite {
            image: game_texture.ball.clone(),
            ..Default::default()
        },
        Transform::from_xyz(0., ball_y, 1.),
        Ball::new(),
    ));
}

pub fn move_ball(moving_area: Res<MovingArea>, ball_query: Single<(&mut Transform, &mut Ball)>) {
    let (mut transform, mut ball) = ball_query.into_inner();

    transform.translation.x += ball.direction.x * ball.speed;
    transform.translation.y += ball.direction.y * ball.speed;

    if ball.is_stuck_to_paddle {
        check_borders_when_moving_with_paddle(&moving_area, &mut transform, &mut ball);
    } else {
        check_borders_when_moving(&moving_area, &mut transform, &mut ball);
    }
}
