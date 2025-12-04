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
        motobug::{
            components::{MOTOBUG_SPRITE_SCALE, Motobug},
            resources::MotobugGenerationTimer,
        },
    },
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameSettings, GameTextures},
};

pub fn spawn_motobug(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    time: Res<Time>,
    mut timer: ResMut<MotobugGenerationTimer>,
) {
    timer.tick(time.delta());

    if timer.just_finished() {
        let animation = Animation::new(0, 4);

        commands.spawn((
            Sprite::from_atlas_image(
                game_textures.motobug.clone(),
                TextureAtlas {
                    layout: game_textures.motobug_atlas.clone(),
                    index: 0,
                },
            ),
            Transform::from_xyz((WINDOW_RESOLUTION.0 as f32) / 2. - 35., -205., 1.)
                .with_scale(Vec3::splat(MOTOBUG_SPRITE_SCALE)),
            animation,
            AnimationTimer(Timer::from_seconds(0.1, TimerMode::Repeating)),
            Motobug,
        ));

        /*
         * Every time we spawn a motobug, we set the MotobugGenerationTimer to a random value
         * so we can simulate spawning other motobugs in random time intervals
         */
        timer.set_random();
    }
}

pub fn move_motobug(
    game_settings: Res<GameSettings>,
    ring_query: Query<&mut Transform, With<Motobug>>,
) {
    for mut ring_tranform in ring_query {
        ring_tranform.translation.x -= game_settings.motobug_speed;
    }
}

pub fn despawn_all_motobugs(mut commands: Commands, ring_query: Query<Entity, With<Motobug>>) {
    for entity in ring_query {
        commands.entity(entity).despawn();
    }
}

pub fn despawn_motobug_out_of_screen(
    mut commands: Commands,
    ring_query: Query<(Entity, &Transform), With<Motobug>>,
) {
    for (entity, transform) in ring_query {
        if transform.translation.x < -(WINDOW_RESOLUTION.0 as f32) / 2. {
            commands.entity(entity).despawn();
        }
    }
}
