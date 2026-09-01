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
    BrickDestroyed, Collider, GameTexture, LevelInfo, Paddle, Randomizer, UPGRADE_MOVEMENT_SPEED,
    UPGRADE_TEXTURE_SIZE, Upgrade, UpgradeType, WINDOW_RESOLUTION_HALF, detect_upgrade_collision,
};

pub fn spawn_upgrade(
    event: On<BrickDestroyed>,
    mut commands: Commands,
    mut randomizer: ResMut<Randomizer>,
    game_texture: Res<GameTexture>,
) {
    let upgrade_type = *UpgradeType::all_variants_array()
        .choose(&mut randomizer.rng)
        .unwrap();

    commands.spawn((
        Sprite {
            image: game_texture.get_upgrade_texture(upgrade_type),
            ..Default::default()
        },
        Transform::from_translation(event.brick_position).with_scale(Vec3::new(0.7, 0.7, 1.)),
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
    mut level_info: ResMut<LevelInfo>,
    paddle_query: Single<(&Transform, &mut Collider, &mut Paddle)>,
    upgrade_query: Query<(Entity, &Transform, &Upgrade)>,
) {
    let (paddle_transform, mut paddle_collider, mut paddle) = paddle_query.into_inner();

    for (upgrade_entity, upgrade_transform, upgrade) in upgrade_query {
        let is_colliding = detect_upgrade_collision(
            Aabb2d::new(
                upgrade_transform.translation.truncate(),
                UPGRADE_TEXTURE_SIZE / 2.,
            ),
            Aabb2d::new(paddle_transform.translation.truncate(), paddle.size / 2.),
        );

        if is_colliding {
            match upgrade.upgrade_type {
                UpgradeType::Heart => level_info.lives += 1,
                UpgradeType::Laser => paddle.laser_count += 1,
                UpgradeType::Size => {
                    paddle.size.x *= 1.1;
                    paddle_collider.size.x *= 1.1
                }
                UpgradeType::Speed => paddle.speed *= 1.1,
            }
            commands.entity(upgrade_entity).despawn();
        }
    }
}
