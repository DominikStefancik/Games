use crate::components::Paddle;
use crate::constants::PADDLE_SPEED;
use bevy::prelude::*;

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

    let new_x =
        paddle_transform.translation.x + direction * PADDLE_SPEED * time_step.delta().as_secs_f32();

    paddle_transform.translation.x = new_x;
}
