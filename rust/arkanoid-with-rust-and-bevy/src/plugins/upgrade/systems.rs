use bevy::{
    ecs::{
        entity::Entity,
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut},
    },
    math::Vec3,
    sprite::Sprite,
    transform::components::Transform,
};
use rand::seq::IndexedRandom;

use crate::plugins::{
    BrickDestroyed, GameTexture, Randomizer, UPGRADE_MOVEMENT_SPEED, UPGRADE_TEXTURE_SIZE, Upgrade,
    UpgradeType, WINDOW_RESOLUTION_HALF,
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
