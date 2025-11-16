use bevy::{ecs::system::Query, transform::components::Transform};

use crate::components::Position;

/*
 * This system is for taking our defined Position and update Bevy's generic Transform to keep them in sync.
 *
 * Note: Every Query<D, F> actually has two generic arguments:
 *      QueryData: The components we want returned
 *      QueryFilter: An optional filter to only fetch components from entities that satisfy it
 *
 * With our query here we instructed Bevy:
 * "Fetch us all the Transform and Position components for entities that have a Transform AND Position component."
 */
pub fn project_positions(mut positionables: Query<(&mut Transform, &Position)>) {
    /*
     * Queries are enumerable objects that fetch our components from the game world, but only when we iterate over
     * them. That means you don't pay the cost until they fetch the data from the game world by enumerating them.
     *
     * Here we are iterating over the query to get the components from our game world
     */
    for (mut transform, position) in &mut positionables {
        // Extend is going to turn this from a Vec2 to a Vec3
        transform.translation = position.0.extend(0.);
    }
}
