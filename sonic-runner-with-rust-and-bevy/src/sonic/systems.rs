use bevy::{
    asset::{AssetServer, Assets},
    ecs::{
        entity::{ContainsEntity, Entity},
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    image::{TextureAtlas, TextureAtlasLayout},
    math::{
        UVec2, Vec3, Vec3Swizzles,
        bounding::{Aabb2d, IntersectsVolume},
    },
    sprite::Sprite,
    time::{Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::components::{Animation, AnimationTimer, ColliderHitBox},
    plugins::default::WINDOW_RESOLUTION,
    ring::components::Ring,
    sonic::components::{SONIC_SPRITE_FRAME_SIZE, SONIC_SPRITE_SCALE, Sonic},
};

pub fn spawn_sonic(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut texture_atlas_layouts: ResMut<Assets<TextureAtlasLayout>>,
) {
    let texture = asset_server.load("graphics/sonic.png");
    let layout = TextureAtlasLayout::from_grid(
        UVec2::new(
            SONIC_SPRITE_FRAME_SIZE.0 as u32,
            SONIC_SPRITE_FRAME_SIZE.1 as u32,
        ),
        8,
        2,
        None,
        None,
    );
    let texture_atlas_layout = texture_atlas_layouts.add(layout);

    let run_animation = Animation::new(0, 7);

    commands.spawn((
        Sprite::from_atlas_image(
            texture.clone(),
            TextureAtlas {
                layout: texture_atlas_layout.clone(),
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
    sonic: Single<(&ColliderHitBox, &Transform), With<Sonic>>,
    ring_query: Query<(Entity, &ColliderHitBox, &Transform), With<Ring>>,
) {
    let (sonic_collider, sonic_transform) = sonic.into_inner();
    let sonic_hit_box = Aabb2d::new(sonic_transform.translation.xy(), sonic_collider.half_size());

    for (ring_entity, ring_collider, ring_transform) in ring_query {
        let ring_hit_box = Aabb2d::new(ring_transform.translation.xy(), ring_collider.half_size());

        if sonic_hit_box.intersects(&ring_hit_box) {
            commands.entity(ring_entity).despawn();
        }
    }
}
