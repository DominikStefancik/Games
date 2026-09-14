use bevy::{
    ecs::{
        entity::Entity,
        query::{With, Without},
        system::{Commands, Query, Single},
    },
    math::{Vec2, Vec3},
    sprite::Sprite,
    transform::components::Transform,
};

use crate::plugins::{
    Ball, Collider, GameTexture, HEART_SCALE, HEART_SIDE_OFFSET, HEART_TEXTURE_SIZE,
    HEART_TOP_OFFSET, HEARTS_GAP, Heart, LEVEL_1_MAP, LEVEL_2_MAP, Laser, MovingArea,
    PADDLE_INITIAL_SIZE, Paddle, Projectile, Upgrade, WINDOW_RESOLUTION_HALF,
    get_ball_initial_position, get_paddle_initial_position,
};

pub fn calculate_heart_horizontal_position(index: u16) -> f32 {
    WINDOW_RESOLUTION_HALF.x
        - HEART_SIDE_OFFSET
        - index as f32 * (HEART_TEXTURE_SIZE.x + HEARTS_GAP)
        - HEART_TEXTURE_SIZE.x / 2.
}

pub fn get_level_map(level: u8) -> Option<Vec<&'static str>> {
    match level {
        1 => Some(LEVEL_1_MAP.to_vec()),
        2 => Some(LEVEL_2_MAP.to_vec()),
        _ => None,
    }
}

pub fn spawn_all_hearts(commands: &mut Commands, game_texture: &GameTexture, lives: u16) {
    for index in 0..lives {
        let position = Vec2::new(
            calculate_heart_horizontal_position(index),
            WINDOW_RESOLUTION_HALF.y - HEART_TEXTURE_SIZE.y / 2. - HEART_TOP_OFFSET,
        );

        commands.spawn((
            Sprite {
                image: game_texture.heart.clone(),
                ..Default::default()
            },
            Transform::from_translation(position.extend(1.)).with_scale(Vec3::splat(HEART_SCALE)),
            Heart { index },
        ));
    }
}

pub fn reset_moving_elements(
    commands: &mut Commands,
    moving_area: &MovingArea,
    ball_query: Single<(&mut Transform, &mut Ball), (With<Ball>, Without<Paddle>)>,
    paddle_query: Single<
        (&mut Transform, &mut Collider, &mut Paddle),
        (With<Paddle>, Without<Ball>),
    >,
    laser_query: Query<Entity, With<Laser>>,
    projectile_query: Query<Entity, With<Projectile>>,
    upgrade_query: Query<Entity, With<Upgrade>>,
) {
    let (mut ball_transform, mut ball) = ball_query.into_inner();
    let (mut paddle_transform, mut paddle_collider, mut paddle) = paddle_query.into_inner();

    ball.reset();
    ball_transform.translation = get_ball_initial_position(moving_area);

    paddle.reset();
    paddle_collider.size = PADDLE_INITIAL_SIZE;
    paddle_transform.translation = get_paddle_initial_position();

    for laser_entity in laser_query {
        commands.entity(laser_entity).despawn();
    }

    for projectile_entity in projectile_query {
        commands.entity(projectile_entity).despawn();
    }

    for upgrade_entity in upgrade_query {
        commands.entity(upgrade_entity).despawn();
    }
}
