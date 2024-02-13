use crate::components::{Ball, BallVelocity, Brick, Collider, Paddle};
use crate::constants::{LEFT_WALL, PADDLE_SPEED, PADDLE_WIDTH_HALF, RIGHT_WALL, WALL_THICKNESS};
use crate::resources::{CollisionSound, Scoreboard};
use bevy::prelude::*;
use bevy::sprite::collide_aabb::{collide, Collision};

/* Resources in Bevy are global data that can be widely accessed; they are Singletons
 * The resource Input is added by using DefaultPlugins
 * The resource Time is added by using DefaultPlugins
 * Query - is used in ECS to find entities that match a set of components
 * With - says that we are interested in a particular component, but not in the data in it
 */
pub fn move_paddle_system(
    input: Res<Input<KeyCode>>,
    // frame time in totally elapsed time
    time_step: Res<Time<Fixed>>,
    // in this case we are looking for any entity that matches Transform and Paddle components
    mut query: Query<&mut Transform, With<Paddle>>,
) {
    // we know we have only one entity with the Paddle component, that's why we can use ".single_mut()"
    // if there were more entities, the call ".single_mut()" would crash
    let mut paddle_transform = query.single_mut();

    let mut direction: f32 = 0.0;
    if input.pressed(KeyCode::Left) {
        direction = -1.
    }
    if input.pressed(KeyCode::Right) {
        direction = 1.;
    }

    let mut new_x =
        paddle_transform.translation.x + direction * PADDLE_SPEED * time_step.delta().as_secs_f32();

    // check the collision of the paddle with the wall
    new_x = new_x.max(LEFT_WALL + WALL_THICKNESS / 2. + PADDLE_WIDTH_HALF);
    new_x = new_x.min(RIGHT_WALL - WALL_THICKNESS / 2. - PADDLE_WIDTH_HALF);

    paddle_transform.translation.x = new_x;
}

pub fn ball_velocity_system(
    time_step: Res<Time<Fixed>>,
    // in this case we are looking for any entity that matches Transform and BallVelocity components
    mut query: Query<(&mut Transform, &BallVelocity)>,
) {
    let delta = time_step.delta().as_secs_f32();
    for (mut transform, ball_velocity) in query.iter_mut() {
        transform.translation.x += ball_velocity.x * delta;
        transform.translation.y += ball_velocity.y * delta;
    }
}

// Checks if a ball collided with (touched) any other object (e.g. wall, paddle, brick)
pub fn check_ball_collisions_system(
    mut commands: Commands,
    mut scoreboard: ResMut<Scoreboard>,
    collision_sound: Res<CollisionSound>,
    // this query will return any entity that matches BallVelocity, Transform and Ball components
    mut ball_query: Query<(&mut BallVelocity, &Transform, &Ball)>,
    // this query will return any entity that matches Transform and Collider components,
    // and optionally it could or couldn't have a Brick component
    collider_query: Query<(Entity, &Transform, &Collider, Option<&Brick>)>,
) {
    for (mut ball_velocity, ball_transform, ball) in ball_query.iter_mut() {
        for (collider_object_entity, collider_object_transform, collider_object, optional_brick) in
            collider_query.iter()
        {
            /*
             * Important:
             *  The resulting "Collision" enum will depend on the order of the entities passed to
             *  the "collide" function. It will always gonna return the sides of the first object
             *  that is in the collision.
             */
            let collision = collide(
                ball_transform.translation,
                ball.size,
                collider_object_transform.translation,
                collider_object.size,
            );

            if let Some(collision) = collision {
                match collision {
                    Collision::Left | Collision::Right => ball_velocity.x *= -1.,
                    Collision::Top | Collision::Bottom => ball_velocity.y *= -1.,
                    Collision::Inside => { /* Do nothing */ }
                }

                // if the object we hit with the ball is a brick, remove it
                if optional_brick.is_some() {
                    commands.entity(collider_object_entity).despawn();
                    scoreboard.score += 1;
                }

                // we can play a sound by spawning an entity with the AudioBundle
                commands.spawn(AudioBundle {
                    source: collision_sound.clone(),
                    // entity is automatically cleaned up after the audio is played
                    settings: PlaybackSettings::DESPAWN,
                });
            }
        }
    }
}

pub fn update_scoreboard_system(scoreboard: Res<Scoreboard>, mut query: Query<&mut Text>) {
    // we know we have only one entity with the Text component in our game, that's why we can use ".single_mut()"
    let mut text = query.single_mut();
    text.sections[1].value = scoreboard.score.to_string();
}
