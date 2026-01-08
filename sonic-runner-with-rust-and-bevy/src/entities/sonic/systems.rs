use bevy::{
    color::Color,
    ecs::{
        children,
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        spawn::SpawnRelated,
        system::{Commands, Query, Res, ResMut, Single},
    },
    image::TextureAtlas,
    input::{ButtonInput, keyboard::KeyCode},
    math::{
        Vec3, Vec3Swizzles,
        bounding::{Aabb2d, IntersectsVolume},
    },
    sprite::{Sprite, Text2d},
    text::{TextColor, TextFont},
    time::{Time, Timer, TimerMode},
    transform::components::Transform,
};

use crate::{
    entities::{
        components::{Animation, AnimationTimer, ColliderHitBox},
        motobug::components::Motobug,
        ring::components::Ring,
        sonic::{
            components::{
                Jump, SONIC_JUMP_MAX_VELOCITY, SONIC_POSITION_MAX_LOW,
                SONIC_RUN_ANIMATION_DURATION, SONIC_SCORE_FONT_SIZE, SONIC_SPRITE_SCALE, Sonic,
                SonicAnimationKind, SonicScoreTextTimer, SonicScoreTextUi,
            },
            events::JumpStarted,
            helpers::switch_sonic_animation,
        },
    },
    plugins::default::WINDOW_RESOLUTION,
    resources::{GameFonts, GameSettings, GameSounds, GameTextures},
    scenes::game::{events::GameScoreUpdated, systems::spawn_sound},
};

pub fn spawn_sonic(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    game_fonts: Res<GameFonts>,
) {
    let run_animation = Animation::new(0, 7);

    let sonic = (
        Sprite::from_atlas_image(
            game_textures.sonic.clone(),
            TextureAtlas {
                layout: game_textures.sonic_atlas.clone(),
                index: 0,
            },
        ),
        Transform::from_xyz(
            -(WINDOW_RESOLUTION.0 as f32) / 2. + 180.,
            SONIC_POSITION_MAX_LOW,
            1.,
        )
        .with_scale(Vec3::splat(SONIC_SPRITE_SCALE)),
        run_animation,
        AnimationTimer(Timer::from_seconds(
            SONIC_RUN_ANIMATION_DURATION,
            TimerMode::Repeating,
        )),
        Sonic::new(),
        Jump::new(),
    );

    let score = (
        SonicScoreTextUi,
        Text2d::new(""),
        TextFont {
            font: game_fonts.mania.clone(),
            font_size: SONIC_SCORE_FONT_SIZE,
            ..Default::default()
        },
        TextColor(Color::srgb_u8(255, 255, 0)),
        Transform::from_xyz(30., 10., 1.),
        SonicScoreTextTimer(Timer::from_seconds(1., TimerMode::Once)),
    );

    commands.spawn((sonic, children![score]));
}

pub fn despawn_sonic(mut commands: Commands, sonic: Single<Entity, With<Sonic>>) {
    commands.entity(sonic.entity()).despawn();
}

pub fn detect_collision_sonic_with_ring(
    mut commands: Commands,
    game_sounds: Res<GameSounds>,
    mut game_settings: ResMut<GameSettings>,
    sonic: Single<(Entity, &ColliderHitBox, &Transform), With<Sonic>>,
    sonic_score: Single<(&mut Text2d, &mut SonicScoreTextTimer), With<SonicScoreTextUi>>,
    ring_query: Query<(Entity, &ColliderHitBox, &Transform), With<Ring>>,
) {
    let (sonic_entity, sonic_collider, sonic_transform) = sonic.into_inner();
    let (mut score_text, mut score_timer) = sonic_score.into_inner();
    let sonic_hit_box = Aabb2d::new(sonic_transform.translation.xy(), sonic_collider.half_size());

    for (ring_entity, ring_collider, ring_transform) in ring_query {
        let ring_hit_box = Aabb2d::new(ring_transform.translation.xy(), ring_collider.half_size());

        if sonic_hit_box.intersects(&ring_hit_box) {
            game_settings.increase_score(1);
            score_text.0 = "+1".to_string();
            // reset timet so after 1 second the score text disappears
            score_timer.0.reset();
            spawn_sound(&mut commands, &game_sounds.ring);
            commands.trigger(GameScoreUpdated(sonic_entity));
            commands.entity(ring_entity).despawn();
        }
    }
}

pub fn detect_collision_sonic_with_motobug(
    mut commands: Commands,
    game_sounds: Res<GameSounds>,
    mut game_settings: ResMut<GameSettings>,
    sonic: Single<(Entity, &mut Sonic, &ColliderHitBox, &Transform, &mut Jump), With<Sonic>>,
    sonic_score: Single<(&mut Text2d, &mut SonicScoreTextTimer), With<SonicScoreTextUi>>,
    motobug_query: Query<(Entity, &ColliderHitBox, &Transform), With<Motobug>>,
) {
    let (sonic_entity, mut sonic, sonic_collider, sonic_transform, mut sonic_jump) =
        sonic.into_inner();
    let (mut score_text, mut score_timer) = sonic_score.into_inner();
    let sonic_hit_box = Aabb2d::new(sonic_transform.translation.xy(), sonic_collider.half_size());

    for (motobug_entity, motobug_collider, motobug_transform) in motobug_query {
        let motobug_hit_box = Aabb2d::new(
            motobug_transform.translation.xy(),
            motobug_collider.half_size(),
        );

        if sonic_hit_box.intersects(&motobug_hit_box) {
            if !sonic_jump.is_in_progress {
                sonic.is_dead = true;
                spawn_sound(&mut commands, &game_sounds.hurt);
                return;
            }

            if sonic_jump.is_going_down {
                sonic_jump.is_restarted = true;
            }

            let score = 10 * game_settings.score_multiplier;
            game_settings.increase_score(score as u32);
            score_text.0 = format!("+{}", score);
            // reset timet so after 1 second the score text disappears
            score_timer.0.reset();

            if sonic_jump.is_restarted {
                game_settings.increment_score_multiplier();
            }

            spawn_sound(&mut commands, &game_sounds.hyper_ring);
            spawn_sound(&mut commands, &game_sounds.destroy);

            commands.trigger(GameScoreUpdated(sonic_entity));
            commands.entity(motobug_entity).despawn();
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
        sonic_jump.velocity = 0.;
        spawn_sound(&mut commands, &game_sounds.jump);
    }
}

pub fn jump(
    mut commands: Commands,
    mut game_settings: ResMut<GameSettings>,
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

        // Sonic just started to jump, he is going up
        if sonic_jump.velocity >= 0.
            && sonic_jump.velocity < SONIC_JUMP_MAX_VELOCITY
            && !sonic_jump.is_going_down
        {
            sonic_jump.velocity += delta_v;
            sonic_jump.is_going_down = false;
        // Sonic jump reached the maximum high, he is starting to fall down
        } else if sonic_jump.velocity == SONIC_JUMP_MAX_VELOCITY {
            sonic_jump.velocity -= delta_v;
            sonic_jump.is_going_down = true;
        // Sonic continues to fall down
        } else if sonic_jump.velocity >= -SONIC_JUMP_MAX_VELOCITY
            && sonic_jump.velocity < SONIC_JUMP_MAX_VELOCITY
            && sonic_jump.is_going_down
        {
            sonic_jump.velocity -= delta_v;
        }

        sonic_transform.translation.y += sonic_jump.velocity;

        /*
         * If "sonic_jump.is_restarted == true" that means Sonic was falling down and collided with a motobug.
         * In that case, we don't want him to land on the platform, but make another jump ("restarted" jump) going up.
         */
        if sonic_jump.is_restarted {
            sonic_jump.velocity = 0.;
            sonic_jump.is_going_down = false;
            // we have to immediately set "is_restarted" to false, otherwise the "velocity" would be kept set to 0
            sonic_jump.is_restarted = false;
        }

        if sonic_transform.translation.y < SONIC_POSITION_MAX_LOW {
            /*
             * after sonic lands, the Y-position of the sprite is lower than the platform
             * therefore we have to adjust it, so it look it landed on the platform and not slightly below it
             */
            sonic_transform.translation.y = SONIC_POSITION_MAX_LOW;
            sonic_jump.is_in_progress = false;
            sonic_jump.is_going_down = false;
            sonic_jump.is_restarted = false;
            game_settings.reset_score_multiplier();

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

pub fn reset_sonic_score_text(
    time: Res<Time>,
    sonic_score: Single<(&mut Text2d, &mut SonicScoreTextTimer), With<SonicScoreTextUi>>,
) {
    let (mut score_text, mut timer) = sonic_score.into_inner();

    timer.tick(time.delta());

    if timer.just_finished() {
        score_text.0 = "".to_string();
    }
}
