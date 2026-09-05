use bevy::{
    ecs::{
        entity::Entity,
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    math::{Vec3, bounding::Aabb2d},
    sprite::Sprite,
    transform::components::Transform,
};
use rand::seq::IndexedRandom;

use crate::plugins::{
    BrickCollided, Collider, GameInfo, GameTexture, HeartUpgradeDestroyed, LaserUpgradeDestroyed,
    PADDLE_LENGTH_INCREASE, Paddle, Randomizer, UPGRADE_MOVEMENT_SPEED, UPGRADE_TEXTURE_SIZE,
    Upgrade, UpgradeType, WINDOW_RESOLUTION_HALF, detect_rectangle_collision,
};

pub fn spawn_upgrade(
    event: On<BrickCollided>,
    mut commands: Commands,
    mut randomizer: ResMut<Randomizer>,
    game_texture: Res<GameTexture>,
    transform_query: Query<&Transform>,
) {
    // Get the Transform component out of given brick entity
    let Ok(brick_position) = transform_query.get(event.brick_entity) else {
        return;
    };

    let upgrade_type = *UpgradeType::all_variants_array()
        .choose(&mut randomizer.rng)
        .unwrap();

    commands.spawn((
        Sprite {
            image: game_texture.get_upgrade_texture(upgrade_type),
            ..Default::default()
        },
        Transform::from_translation(brick_position.translation).with_scale(Vec3::new(0.7, 0.7, 1.)),
        Upgrade { upgrade_type },
    ));
}

pub fn move_upgrade(mut commands: Commands, query: Query<(Entity, &mut Transform), With<Upgrade>>) {
    for (entity, mut transform) in query {
        transform.translation.y -= UPGRADE_MOVEMENT_SPEED;

        if transform.translation.y <= -WINDOW_RESOLUTION_HALF.y - UPGRADE_TEXTURE_SIZE.y / 2. {
            commands.entity(entity).despawn();
        }
    }
}

pub fn check_upgrade_collision(
    mut commands: Commands,
    mut game_info: ResMut<GameInfo>,
    paddle_query: Single<(&Transform, &mut Collider, &mut Paddle)>,
    upgrade_query: Query<(Entity, &Transform, &Upgrade)>,
) {
    let (paddle_transform, mut paddle_collider, mut paddle) = paddle_query.into_inner();

    for (upgrade_entity, upgrade_transform, upgrade) in upgrade_query {
        let is_colliding = detect_rectangle_collision(
            Aabb2d::new(
                upgrade_transform.translation.truncate(),
                UPGRADE_TEXTURE_SIZE / 2.,
            ),
            Aabb2d::new(paddle_transform.translation.truncate(), paddle.size / 2.),
        );

        if is_colliding {
            match upgrade.upgrade_type {
                UpgradeType::Heart => {
                    game_info.lives += 1;
                    commands.trigger(HeartUpgradeDestroyed);
                }
                UpgradeType::Laser => {
                    commands.trigger(LaserUpgradeDestroyed);
                }
                UpgradeType::Size => {
                    paddle.size.x += PADDLE_LENGTH_INCREASE;
                    paddle_collider.size = paddle.size;
                }
                UpgradeType::Speed => paddle.speed *= 1.1,
            }
            commands.entity(upgrade_entity).despawn();
        }
    }
}
