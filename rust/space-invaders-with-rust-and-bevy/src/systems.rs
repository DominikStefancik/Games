use crate::{
    assets::{BASE_SPEED, EXPLOSION_LENGTH, TIME_STEP},
    components::{
        Enemy, Explosion, ExplosionTimer, ExplosionToSpawn, Laser, LaserFromEnemy, LaserFromPlayer,
        Movable, Player, SpriteSize, Velocity,
    },
    resources::{EnemyCount, GameTextures, PlayerState, WindowSize},
};
use bevy::{
    image::TextureAtlas,
    math::bounding::{Aabb2d, IntersectsVolume},
    prelude::{Commands, Entity, Query, Res, ResMut, Time, Transform, With},
    sprite::Sprite,
};
use std::collections::HashSet;

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
    mut enemy_count: ResMut<EnemyCount>,
    laser_query: Query<(Entity, &Transform, &SpriteSize), (With<Laser>, With<LaserFromPlayer>)>,
    enemy_query: Query<(Entity, &Transform, &SpriteSize), With<Enemy>>,
) {
    // every entity is global in the the Bevy "world"
    let mut despawned_entities: HashSet<Entity> = HashSet::new();

    // iterate through the lasers
    // for each laser shot from the player check if it hit any of the enemies
    for (laser_entity, laser_transform, laser_size) in laser_query.iter() {
        if despawned_entities.contains(&laser_entity) {
            continue;
        }

        let laser_scale = laser_transform.scale.truncate();
        let laser_position = laser_transform.translation;

        for (enemy_entity, enemy_transform, enemy_size) in enemy_query.iter() {
            if despawned_entities.contains(&enemy_entity)
                || despawned_entities.contains(&laser_entity)
            {
                continue;
            }

            let enemy_scale = enemy_transform.scale.truncate();
            let enemy_position = enemy_transform.translation;

            // determine if the enemy has a collision with a laser
            let collision =
                Aabb2d::new(laser_position.truncate(), laser_size.0 * laser_scale / 2.).intersects(
                    &Aabb2d::new(enemy_position.truncate(), enemy_size.0 * enemy_scale),
                );

            // perform logic when a collision happened
            if collision {
                // remove entity from the scene
                commands.entity(enemy_entity).despawn();
                despawned_entities.insert(enemy_entity);
                enemy_count.0 -= 1;

                // remove laser from the scene
                commands.entity(laser_entity).despawn();
                despawned_entities.insert(laser_entity);

                // spawn the ExplosionToSpawn
                // spawn the explosion at the same place where the enemy was
                commands.spawn(ExplosionToSpawn(enemy_transform.translation));
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
            .spawn((
                Sprite::from_atlas_image(
                    game_textures.explosion.clone(),
                    TextureAtlas::from(game_textures.explosion_atlas.clone()),
                ),
                Transform {
                    translation: explosion_to_spawn.0, // no clone() is needed, because Vec3 is a copy
                    ..Default::default()
                },
            ))
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
    mut query: Query<(Entity, &mut ExplosionTimer, &mut Sprite), With<Explosion>>,
) {
    for (entity, mut timer, mut sprite) in query.iter_mut() {
        timer.0.tick(time.delta());

        if timer.0.finished() {
            // when the timer cycle finished
            if let Some(texture_atlas) = &mut sprite.texture_atlas {
                texture_atlas.index += 1;
                // move to the next sprite cell in the explosions sheet
                if texture_atlas.index >= EXPLOSION_LENGTH as usize {
                    commands.entity(entity).despawn();
                }
            }
        }
    }
}

pub fn laser_from_enemy_hit_player_system(
    mut commands: Commands,
    mut player_state: ResMut<PlayerState>,
    time: Res<Time>,
    laser_query: Query<(Entity, &Transform, &SpriteSize), (With<Laser>, With<LaserFromEnemy>)>,
    player_query: Query<(Entity, &Transform, &SpriteSize), With<Player>>,
) {
    // we know we have only one player at the time
    if let Ok((player_entity, player_transform, player_size)) = player_query.single() {
        let player_scale = player_transform.scale.truncate();

        // we have to iterate through the all lasers
        for (laser_entity, laser_transform, laser_size) in laser_query.iter() {
            let laser_scale = laser_transform.scale.truncate();

            // check if a collision happened
            let collision = Aabb2d::new(
                laser_transform.translation.truncate(),
                laser_size.0 * laser_scale / 2.,
            )
            .intersects(&Aabb2d::new(
                player_transform.translation.truncate(),
                player_size.0 * player_scale / 2.,
            ));

            // perform logic when a collision happened
            if collision {
                // remove the player
                commands.entity(player_entity).despawn();
                // update the player state
                player_state.player_shot(time.elapsed_secs_f64());

                // remove the laser
                commands.entity(laser_entity).despawn();

                // spawn the ExplosionToSpawn
                commands.spawn(ExplosionToSpawn(player_transform.translation));

                // when the player is hit, break the whole game loop
                break;
            }
        }
    }
}
