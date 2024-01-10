use crate::assets::{BASE_SPEED, TIME_STEP};
use crate::components::{Enemy, Laser, LaserFromPlayer, Movable, SpriteSize, Velocity};
use crate::resources::WindowSize;
use bevy::prelude::{Commands, Entity, Query, Res, Transform, Vec2, With};
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
            }
        }
    }
}
