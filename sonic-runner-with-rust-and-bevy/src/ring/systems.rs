use bevy::{
    asset::{AssetServer, Assets},
    ecs::{
        entity::Entity,
        query::With,
        system::{Commands, Query, Res, ResMut},
    },
    image::{TextureAtlas, TextureAtlasLayout},
    math::{UVec2, Vec3},
    sprite::Sprite,
    time::{Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::components::{Animation, AnimationTimer},
    game::resources::GameSettings,
    plugins::default::WINDOW_RESOLUTION,
    ring::components::{RING_SPRITE_FRAME_SIZE, RING_SPRITE_SCALE, Ring},
};

pub fn spawn_ring(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let texture = asset_server.load("graphics/ring.png");
    let layout = TextureAtlasLayout::from_grid(
        UVec2::new(
            RING_SPRITE_FRAME_SIZE.0 as u32,
            RING_SPRITE_FRAME_SIZE.1 as u32,
        ),
        16,
        1,
        None,
        None,
    );
    let texture_atlas_layout = texture_atlas_layouts.add(layout);

    let run_animation = Animation::new(0, 15);

    commands.spawn((
        Sprite::from_atlas_image(
            texture.clone(),
            TextureAtlas {
                layout: texture_atlas_layout.clone(),
                index: 0,
            },
        ),
        Transform::from_xyz((WINDOW_RESOLUTION.0 as f32) / 2. - 30., -205., 1.)
            .with_scale(Vec3::splat(RING_SPRITE_SCALE)),
        run_animation,
        AnimationTimer(Timer::from_seconds(0.04, TimerMode::Repeating)),
        Ring,
    ));
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
