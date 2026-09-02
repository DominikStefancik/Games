use bevy::{
    ecs::{
        entity::Entity,
        system::{Commands, Query, Res, Single},
    },
    math::bounding::{Aabb2d, BoundingCircle},
    sprite::Sprite,
    state::state::State,
    transform::components::Transform,
};

use crate::plugins::{
    BALL_RADIUS, Ball, Brick, BrickDestroyed, Collider, CollisionSide, GameState, GameTexture,
    MovingArea, Paddle, check_borders_when_moving, check_borders_when_moving_with_paddle,
    detect_ball_collision, is_game_starting_or_running,
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

pub fn move_ball(
    app_state: Res<State<GameState>>,
    moving_area: Res<MovingArea>,
    ball_query: Single<(&mut Transform, &mut Ball)>,
    paddle: Single<&Paddle>,
) {
    if !is_game_starting_or_running(app_state.get()) {
        return;
    }

    let (mut transform, mut ball) = ball_query.into_inner();

    transform.translation.x += ball.direction.x * ball.speed;
    transform.translation.y += ball.direction.y * ball.speed;

    if *app_state.get() == GameState::GameStarting {
        check_borders_when_moving_with_paddle(&moving_area, &mut transform, &mut ball, &paddle);
    } else if *app_state.get() == GameState::Running {
        check_borders_when_moving(&moving_area, &mut transform, &mut ball);
    }
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
                commands.entity(collider_entity).despawn();
                commands.trigger(BrickDestroyed {
                    brick_position: collider_transform.translation,
                });
            }
        }
    }
}
