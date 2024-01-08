use crate::components::{Movable, Velocity};
use crate::resources::WindowSize;
use bevy::prelude::{Commands, Entity, Query, Res, Transform};

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
    for (entity, velocity, mut transform, movable) in query.iter_mut() {
        let translation = &mut transform.translation;
        translation.x += velocity.x;
        translation.y += velocity.y;
    }
}
