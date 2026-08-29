use bevy::{
    ecs::system::{Commands, Query, Res, Single},
    math::bounding::{Aabb2d, BoundingCircle},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BALL_RADIUS, Ball, Collider, CollisionSide, GameTexture, MovingArea, check_borders_when_moving,
    check_borders_when_moving_with_paddle, detect_ball_collision,
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

pub fn check_ball_collision(
    ball_query: Single<(&Transform, &mut Ball)>,
    collider_query: Query<(&Transform, &Collider)>,
) {
    let (ball_transform, mut ball) = ball_query.into_inner();

    if ball.is_stuck_to_paddle {
        return;
    }

    for (collider_transform, collider) in collider_query {
        let collision_side = detect_ball_collision(
            BoundingCircle::new(ball_transform.translation.truncate(), BALL_RADIUS),
            Aabb2d::new(
                collider_transform.translation.truncate(),
                collider.size / 2.,
            ),
        );

        if let Some(side) = collision_side {
            match side {
                CollisionSide::Left => ball.direction.x = -1.,
                CollisionSide::Right => ball.direction.x = 1.,
                CollisionSide::Top => ball.direction.y = 1.,
                CollisionSide::Bottom => ball.direction.y = -1.,
            }
        }
    }
}
