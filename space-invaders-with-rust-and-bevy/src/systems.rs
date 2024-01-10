use crate::{
    assets::{BASE_SPEED, EXPLOSION_LENGTH, TIME_STEP},
    components::{
        Enemy, Explosion, ExplosionTimer, ExplosionToSpawn, Laser, LaserFromPlayer, Movable,
        SpriteSize, Velocity,
    },
    resources::{GameTextures, WindowSize},
};
use bevy::prelude::{
    Commands, Entity, Query, Res, SpriteSheetBundle, TextureAtlasSprite, Time, Transform, Vec2,
    With,
};
use bevy::sprite::collide_aabb::collide;

// Bevy systems are just a function
// Bevy will inject the required arguments for system functions for us

// system which is changing position/movement of any movable object depending on the input velocity
pub fn movable_system(
    // we need commands to despawn a Movable object if necessary
    mut commands: Commands,
    window_size: Res<WindowSize>,
    // the first (tuple) part of the Query says which part we just want to read and which we want to mutate
    mut query: Query<(Entity, &Velocity, &mut Transform, &Movable)>,
) {
    // "entity" is something like an index of an object in the scene
    for (entity, velocity, mut transform, movable) in query.iter_mut() {
        let translation = &mut transform.translation;
        translation.x += velocity.x * TIME_STEP * BASE_SPEED;
        translation.y += velocity.y * TIME_STEP * BASE_SPEED;

        if movable.auto_despawn {
            const MARGIN: f32 = 200.;

            // despawn if a movable object is out of screen
            if translation.x > window_size.width / 2. + MARGIN
                || translation.x < -window_size.width / 2. - MARGIN
                || translation.y > window_size.height / 2. + MARGIN
                || translation.y < -window_size.height / 2. - MARGIN
            {
                commands.entity(entity).despawn();
            }
        }
    }
}

pub fn laser_from_player_hit_enemy_system(
    mut commands: Commands,
    laser_query: Query<(Entity, &Transform, &SpriteSize), (With<Laser>, With<LaserFromPlayer>)>,
    enemy_query: Query<(Entity, &Transform, &SpriteSize), With<Enemy>>,
) {
    // iterate through the lasers
    // for each laser shot from the player check if it hit any of the enemies
    for (laser_entity, laser_transform, laser_size) in laser_query.iter() {
        let laser_scale = Vec2::from(laser_transform.scale.truncate());
        let laser_position = laser_transform.translation;

        for (enemy_entity, enemy_transform, enemy_size) in enemy_query.iter() {
            let enemy_scale = Vec2::from(enemy_transform.scale.truncate());
            let enemy_position = enemy_transform.translation;

            // determine if the enemy has a collision with a laser
            let collision = collide(
                laser_position,
                laser_size.0 * laser_scale,
                enemy_position,
                enemy_size.0 * enemy_scale,
            );

            // perform logic when a collision happened
            if let Some(_) = collision {
                // we don't care what the collision returns
                // remove entity from the scene
                commands.entity(enemy_entity).despawn();
                // remove laser from the scene
                commands.entity(laser_entity).despawn();
                // spawn the ExplosionToSpawn
                // spawn the explosion at the same place where the enemy was
                commands.spawn(ExplosionToSpawn(enemy_transform.translation.clone()));
            }
        }
    }
}

pub fn explosion_to_spawn_system(
    mut commands: Commands,
    game_textures: Res<GameTextures>,
    // here we don't need With<> part in the Query, because we will get the data which only has the ExplosionToSpawn
    query: Query<(Entity, &ExplosionToSpawn)>,
) {
    for (explosion_to_spawn_entity, explosion_to_spawn) in query.iter() {
        // spawn the explosion sprite
        commands
            .spawn(SpriteSheetBundle {
                texture_atlas: game_textures.explosion.clone(),
                transform: Transform {
                    translation: explosion_to_spawn.0, // no clone() is needed, because Vec3 is a copy
                    ..Default::default()
                },
                ..Default::default()
            })
            .insert(Explosion)
            // we add a time for an explosion, so we can animate it
            .insert(ExplosionTimer::default());

        // at the end we need to clean up and and despawn the ExplosionToSpawn entity
        commands.entity(explosion_to_spawn_entity).despawn();
    }
}

pub fn explosion_animation_system(
    mut commands: Commands,
    time: Res<Time>,
    mut query: Query<(Entity, &mut ExplosionTimer, &mut TextureAtlasSprite), With<Explosion>>,
) {
    for (entity, mut timer, mut sprite) in query.iter_mut() {
        timer.0.tick(time.delta());

        if timer.0.finished() {
            // when the timer cycle finished
            sprite.index += 1; // move to the next sprite cell in the explosions sheet
            if sprite.index >= EXPLOSION_LENGTH {
                commands.entity(entity).despawn();
            }
        }
    }
}
