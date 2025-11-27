use bevy::{
    ecs::{
        entity::{ContainsEntity, Entity},
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    image::TextureAtlas,
    math::{
        Vec3, Vec3Swizzles,
        bounding::{Aabb2d, IntersectsVolume},
    },
    sprite::Sprite,
    time::{Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::components::{Animation, AnimationTimer, ColliderHitBox},
    game::{events::ScoreUpdated, systems::spawn_sound},
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameSettings, GameSounds, GameTextures},
    ring::components::Ring,
    sonic::components::{SONIC_SPRITE_SCALE, Sonic},
};

pub fn spawn_sonic(mut commands: Commands, game_textures: Res<GameTextures>) {
    let run_animation = Animation::new(0, 7);

    commands.spawn((
        Sprite::from_atlas_image(
            game_textures.sonic.clone(),
            TextureAtlas {
                layout: game_textures.sonic_atlas.clone(),
                index: 0,
            },
        ),
        Transform::from_xyz(-(WINDOW_RESOLUTION.0 as f32) / 2. + 180., -185., 1.)
            .with_scale(Vec3::splat(SONIC_SPRITE_SCALE)),
        run_animation,
        AnimationTimer(Timer::from_seconds(0.04, TimerMode::Repeating)),
        Sonic,
    ));
}

pub fn despawn_sonic(mut commands: Commands, sonic: Single<Entity, With<Sonic>>) {
    commands.entity(sonic.entity()).despawn();
}

pub fn detect_collision_sonic_with_ring(
    mut commands: Commands,
    game_sounds: Res<GameSounds>,
    mut game_settings: ResMut<GameSettings>,
    sonic: Single<(&ColliderHitBox, &Transform), With<Sonic>>,
    ring_query: Query<(Entity, &ColliderHitBox, &Transform), With<Ring>>,
) {
    let (sonic_collider, sonic_transform) = sonic.into_inner();
    let sonic_hit_box = Aabb2d::new(sonic_transform.translation.xy(), sonic_collider.half_size());

    for (ring_entity, ring_collider, ring_transform) in ring_query {
        let ring_hit_box = Aabb2d::new(ring_transform.translation.xy(), ring_collider.half_size());

        if sonic_hit_box.intersects(&ring_hit_box) {
            game_settings.increase_score(1);
            spawn_sound(&mut commands, &game_sounds.ring);
            commands.trigger(ScoreUpdated(ring_entity));
            commands.entity(ring_entity).despawn();
        }
    }
}
