use bevy::{
    ecs::{
        entity::Entity,
        query::With,
        system::{Commands, Query, Res, Single},
    },
    math::bounding::{Aabb2d, BoundingCircle},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    BALL_RADIUS, Ball, BallFallenDown, Brick, BrickCollided, Collider, CollisionSide, GameTexture,
    MovingArea, Paddle, WINDOW_RESOLUTION_HALF, check_borders_when_moving,
    check_borders_when_moving_with_paddle, detect_ball_collision, get_ball_initial_position,
};

pub fn spawn_ball(
    mut commands: Commands,
    game_texture: Res<GameTexture>,
    moving_area: Res<MovingArea>,
) {
    commands.spawn((
        Sprite {
            image: game_texture.ball.clone(),
            ..Default::default()
        },
        Transform::from_translation(get_ball_initial_position(moving_area.into_inner())),
        Ball::new(),
    ));
}

pub fn move_ball_when_game_starts(
    moving_area: Res<MovingArea>,
    ball_query: Single<(&mut Transform, &mut Ball)>,
    paddle: Single<&Paddle>,
) {
    let (mut transform, mut ball) = ball_query.into_inner();

    transform.translation.x += ball.direction.x * ball.speed;

    check_borders_when_moving_with_paddle(&moving_area, &mut transform, &mut ball, &paddle);
}

pub fn move_ball_when_game_runs(
    moving_area: Res<MovingArea>,
    ball_query: Single<(&mut Transform, &mut Ball)>,
) {
    let (mut transform, mut ball) = ball_query.into_inner();

    transform.translation.x += ball.direction.x * ball.speed;
    transform.translation.y += ball.direction.y * ball.speed;

    check_borders_when_moving(&moving_area, &mut transform, &mut ball);
}

pub fn check_ball_collision(
    mut commands: Commands,
    ball_query: Single<(&Transform, &mut Ball)>,
    // this query will return any entity that matches Transform and Collider components,
    // and optionally it could or couldn't have a Brick component
    collider_query: Query<(Entity, &Transform, &Collider, Option<&Brick>)>,
) {
    let (ball_transform, mut ball) = ball_query.into_inner();

    for (collider_entity, collider_transform, collider, optional_brick) in collider_query {
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

            if optional_brick.is_some() {
                commands.trigger(BrickCollided {
                    brick_entity: collider_entity,
                    brick_position: collider_transform.translation,
                });
            }
        }
    }
}

pub fn check_ball_out_of_bounds(
    mut commands: Commands,
    ball_query: Single<&mut Transform, With<Ball>>,
) {
    let ball_transform = ball_query.into_inner();

    if ball_transform.translation.y <= -WINDOW_RESOLUTION_HALF.y {
        commands.trigger(BallFallenDown);
    }
}
