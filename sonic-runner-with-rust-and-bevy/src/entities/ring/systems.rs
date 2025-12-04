use bevy::{
    ecs::{
        entity::Entity,
        query::With,
        system::{Commands, Query, Res, ResMut},
    },
    image::TextureAtlas,
    math::Vec3,
    sprite::Sprite,
    time::{Time, Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::{
        components::{Animation, AnimationTimer},
        ring::{
            components::{RING_SPRITE_SCALE, Ring},
            resources::RingGenerationTimer,
        },
    },
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameSettings, GameTextures},
};

pub fn spawn_ring(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    time: Res<Time>,
    mut timer: ResMut<RingGenerationTimer>,
) {
    timer.tick(time.delta());

    if timer.just_finished() {
        let animation = Animation::new(0, 15);

        commands.spawn((
            Sprite::from_atlas_image(
                game_textures.ring.clone(),
                TextureAtlas {
                    layout: game_textures.ring_atlas.clone(),
                    index: 0,
                },
            ),
            Transform::from_xyz((WINDOW_RESOLUTION.0 as f32) / 2. - 30., -205., 1.)
                .with_scale(Vec3::splat(RING_SPRITE_SCALE)),
            animation,
            AnimationTimer(Timer::from_seconds(0.04, TimerMode::Repeating)),
            Ring,
        ));

        /*
         * Every time we spawn a ring, we set the RingGenerationTimer to the random value
         * so we can simulate spawning other rings in random time intervals
         */
        timer.set_random();
    }
}

pub fn move_ring(game_settings: Res<GameSettings>, ring_query: Query<&mut Transform, With<Ring>>) {
    for mut ring_tranform in ring_query {
        ring_tranform.translation.x -= game_settings.speed;
    }
}

pub fn despawn_all_rings(mut commands: Commands, ring_query: Query<Entity, With<Ring>>) {
    for entity in ring_query {
        commands.entity(entity).despawn();
    }
}

pub fn despawn_ring_out_of_screen(
    mut commands: Commands,
    ring_query: Query<(Entity, &Transform), With<Ring>>,
) {
    for (entity, transform) in ring_query {
        if transform.translation.x < -(WINDOW_RESOLUTION.0 as f32) / 2. {
            commands.entity(entity).despawn();
        }
    }
}
