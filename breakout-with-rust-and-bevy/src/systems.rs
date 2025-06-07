use crate::collision::{ball_collision, Collision};
use crate::components::{Ball, BallVelocity, Brick, Collider, Paddle, ScoreBoardText};
use crate::constants::{LEFT_WALL, PADDLE_SPEED, PADDLE_WIDTH_HALF, RIGHT_WALL, WALL_THICKNESS};
use crate::resources::{CollisionSound, Scoreboard};
use bevy::math::bounding::{Aabb2d, BoundingCircle};
use bevy::prelude::{
    AudioPlayer, ButtonInput, Commands, Entity, Fixed, KeyCode, PlaybackSettings, Query, Res,
    ResMut, TextUiWriter, Time, Transform, With,
};

/* Resources in Bevy are global data that can be widely accessed; they are Singletons
 * The resource ButtonInput is added by using DefaultPlugins
 * The resource Time is added by using DefaultPlugins
 * Query - is used in ECS to find entities that match a set of components
 * With - says that we are interested in a particular component, but not in the data in it
 */
pub fn move_paddle_system(
    input: Res<ButtonInput<KeyCode>>,
    // frame time in totally elapsed time
    time_step: Res<Time<Fixed>>,
    // in this case we are looking for any entity that matches Transform and Paddle components
    mut query: Query<&mut Transform, With<Paddle>>,
) {
    // we know we have only one entity with the Paddle component, that's why we can use ".single_mut()"
    // if there were more entities, the call ".single_mut()" would crash
    let mut paddle_transform = query.single_mut().unwrap();

    let mut direction: f32 = 0.0;
    if input.pressed(KeyCode::ArrowLeft) {
        direction = -1.
    }
    if input.pressed(KeyCode::ArrowRight) {
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
            let collision = ball_collision(
                BoundingCircle::new(ball_transform.translation.truncate(), ball.diameter / 2.),
                Aabb2d::new(
                    collider_object_transform.translation.truncate(),
                    collider_object.size / 2.,
                ),
            );

            if let Some(collision) = collision {
                // Reflect the ball's velocity when it collides
                let mut reflect_x = false;
                let mut reflect_y = false;

                // Reflect only if the velocity is in the opposite direction of the collision
                // This prevents the ball from getting stuck inside the bar
                match collision {
                    Collision::Left => reflect_x = ball_velocity.x > 0.0,
                    Collision::Right => reflect_x = ball_velocity.x < 0.0,
                    Collision::Top => reflect_y = ball_velocity.y < 0.0,
                    Collision::Bottom => reflect_y = ball_velocity.y > 0.0,
                }

                // Reflect velocity on the x-axis if we hit something on the x-axis
                if reflect_x {
                    ball_velocity.x *= -1.;
                }

                // Reflect velocity on the y-axis if we hit something on the y-axis
                if reflect_y {
                    ball_velocity.y *= -1.;
                }

                // if the object we hit with the ball is a brick, remove it
                if optional_brick.is_some() {
                    commands.entity(collider_object_entity).despawn();
                    scoreboard.score += 1;
                }

                // we can play a sound by spawning an entity with the AudioPlayer
                commands.spawn((
                    AudioPlayer::new(collision_sound.0.clone()),
                    // entity is automatically cleaned up after the audio is played
                    PlaybackSettings::DESPAWN,
                ));
            }
        }
    }
}

pub fn update_scoreboard_system(
    scoreboard: Res<Scoreboard>,
    query: Query<Entity, With<ScoreBoardText>>,
    mut writer: TextUiWriter,
) {
    // we know we have only one entity with the ScoreBoardText component in our game, that's why we can use ".single()"
    let entity = query.single().unwrap();
    *writer.text(entity, 1) = scoreboard.score.to_string();
}
