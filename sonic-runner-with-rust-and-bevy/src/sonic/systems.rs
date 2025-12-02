use bevy::{
    ecs::{
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    image::TextureAtlas,
    input::{ButtonInput, keyboard::KeyCode},
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
    sonic::{
        components::{
            Jump, SONIC_JUMP_MAX_HIGH, SONIC_POSITION_MAX_LOW, SONIC_RUN_ANIMATION_DURATION,
            SONIC_SPRITE_SCALE, Sonic, SonicAnimationKind,
        },
        events::JumpStarted,
        helpers::switch_sonic_animation,
    },
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
        AnimationTimer(Timer::from_seconds(
            SONIC_RUN_ANIMATION_DURATION,
            TimerMode::Repeating,
        )),
        Sonic::new(),
        Jump::new(),
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

pub fn trigger_jump(
    mut commands: Commands,
    keyboard_input: Res<ButtonInput<KeyCode>>,
    sonic: Single<(Entity, &mut Jump), With<Sonic>>,
) {
    let (sonic_entity, sonic_jump) = sonic.into_inner();

    if keyboard_input.just_pressed(KeyCode::Space) && !sonic_jump.is_in_progress {
        commands.trigger(JumpStarted(sonic_entity));
    }
}

pub fn start_jump(
    _: On<JumpStarted>,
    mut commands: Commands,
    game_sounds: Res<GameSounds>,
    sonic_query: Single<&mut Jump, With<Sonic>>,
) {
    let mut sonic_jump = sonic_query.into_inner();

    if !sonic_jump.is_in_progress {
        sonic_jump.is_in_progress = true;
        spawn_sound(&mut commands, &game_sounds.jump);
    }
}

pub fn jump(
    mut commands: Commands,
    sonic_query: Single<
        (
            Entity,
            &mut Transform,
            &mut Jump,
            &mut Sprite,
            &mut AnimationTimer,
        ),
        With<Sonic>,
    >,
) {
    let (sonic_entity, mut sonic_transform, mut sonic_jump, mut sprite, mut animation_timer) =
        sonic_query.into_inner();

    if sonic_jump.is_in_progress {
        let delta_v = 0.5;

        // when Sonic is jumping, change the animation
        switch_sonic_animation(
            SonicAnimationKind::Jump,
            &mut commands,
            sonic_entity,
            &mut animation_timer,
        );

        if sonic_transform.translation.y < SONIC_JUMP_MAX_HIGH {
            sonic_jump.velocity += delta_v;
        } else {
            sonic_jump.velocity -= delta_v;
        }

        sonic_transform.translation.y += sonic_jump.velocity;

        if sonic_transform.translation.y <= SONIC_POSITION_MAX_LOW {
            sonic_jump.is_in_progress = false;

            // after Sonic landed on the platform, change the animation back to running
            sprite.texture_atlas.as_mut().unwrap().index = 0;
            switch_sonic_animation(
                SonicAnimationKind::Run,
                &mut commands,
                sonic_entity,
                &mut animation_timer,
            );
        }
    }
}
